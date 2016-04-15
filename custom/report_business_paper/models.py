# -*- coding: utf-8 -*-

import cStringIO
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pyPdf.pdf import PdfFileReader
from pyPdf.pdf import PdfFileWriter

from openerp import SUPERUSER_ID
from openerp.osv import osv, fields

point = 1
mm = 2.83464567
inch = 72

a4_width = 210 * mm
a4_height = 297 * mm


class res_company(osv.Model):
    _inherit = 'res.company'

    _columns = {
        'business_paper': fields.binary("Business Paper", help='Business paper image'),
    }

    def init(self, cr):
        ids = self.search(cr, SUPERUSER_ID, [('business_paper', '=', False)])
        for company in self.browse(cr, SUPERUSER_ID, ids):
            company.write({'business_paper': None})

        sup = super(res_company, self)
        if hasattr(sup, 'init'):
            sup.init(cr)

class Report(osv.Model):
    _inherit = 'report'

    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None, context=None):
        content = super(Report, self).get_pdf(cr, uid, ids, report_name, html, data, context)
        if report_name == u'report_business_paper.report_business_paper_invoice':
            content = self._add_business_paper(cr, uid, content)
        return content

    def _add_business_paper(self, cr, uid, content):
        # Get the current user record.
        context = {}
        users = self.pool.get('res.users')
        current_user = users.browse(cr, uid, uid, context)

        # Retrieve the business paper image data.
        company = current_user.company_id
        image_data = company.business_paper

        # Create a temporary file containing the image data and draw it on the PDF.
        image = tempfile.SpooledTemporaryFile(suffix='.img', prefix='business_paper.tmp.', mode='w+b')
        image.write(image_data.decode('base64'))
        image.seek(0)
        image_reader = ImageReader(image)

        # Create a temporary PDF file containing the image.
        business_paper_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', prefix='business_paper.tmp.', mode='w+b')
        c = canvas.Canvas(business_paper_pdf, pagesize=[a4_width, a4_height])
        c.drawImage(image_reader, 0, 0, a4_width, a4_height, mask=[254, 255, 254, 255, 254, 255])
        c.save()
        image.close()

        # Write the report to a temporary PDF file.
        pdfreport = tempfile.SpooledTemporaryFile(suffix='.pdf', prefix='report.tmp.', mode='w+b')
        pdfreport.write(content)

        # Merge the PDF documents and return the merged content.
        pdfdocuments = [business_paper_pdf, pdfreport]
        content = self._merge_pdf_pages(pdfdocuments)
        return content

    def _merge_pdf_pages(self, documents):
        """Merge PDF files into one.

        :param documents: list of pdf files
        :returns: string containing the merged pdf
        """
        writer = PdfFileWriter()
        for document in documents:
            document.seek(0)
            reader = PdfFileReader(document)
            for pageNumber in range(0, reader.getNumPages()):
                if writer.getNumPages() <= pageNumber:
                    writer.addPage(reader.getPage(pageNumber))
                else:
                    page = writer.getPage(pageNumber)
                    page.mergePage(reader.getPage(pageNumber))

        merged = cStringIO.StringIO()
        writer.write(merged)
        merged.seek(0)
        content = merged.read()
        merged.close()

        for document in documents:
            document.close()

        return content
