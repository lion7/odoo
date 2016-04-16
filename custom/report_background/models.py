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

class ir_actions_report(osv.Model):
    _inherit = 'ir.actions.report.xml'

    _columns = {
        'background': fields.binary('Background'),
    }

class Report(osv.Model):
    _inherit = 'report'

    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None, context=None):
        # Get the PDF content of the report
        content = super(Report, self).get_pdf(cr, uid, ids, report_name, html, data, context)
        # Get the ir.actions.report.xml record we are working on.
        report = super(Report, self)._get_report_from_name(cr, uid, report_name)
        # Add the background
        if report.background:
            content = self._add_background(cr, uid, content, report.background, context)
        return content

    def _add_background(self, cr, uid, content, background, context=None):
        # Create a temporary file containing the image data.
        image = tempfile.SpooledTemporaryFile(suffix='.img', prefix='background.tmp.', mode='w+b')
        image.write(background.decode('base64'))
        image.seek(0)
        image_reader = ImageReader(image)

        # Create a temporary PDF file containing the background.
        background_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', prefix='background.tmp.', mode='w+b')
        c = canvas.Canvas(background_pdf, pagesize=[a4_width, a4_height])
        c.drawImage(image_reader, 0, 0, a4_width, a4_height)
        c.save()
        image.close()

        # Write the report to a temporary PDF file.
        pdfreport = tempfile.SpooledTemporaryFile(suffix='.pdf', prefix='report.tmp.', mode='w+b')
        pdfreport.write(content)

        # Merge the PDF documents and return the merged content.
        pdfdocuments = [background_pdf, pdfreport]
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
