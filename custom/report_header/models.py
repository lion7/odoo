# -*- coding: utf-8 -*-

from functools import partial

from openerp import SUPERUSER_ID
from openerp.osv import osv, fields


class res_company(osv.Model):
    _inherit = 'res.company'

    _columns = {
        'custom_header': fields.boolean("Custom header",
                                        help='Check this to define the report header manually. '
                                             'Otherwise it will be filled in automatically.'),
        'rml_header_custom': fields.text("Report header", help='Header text displayed at the top of all reports.'),
    }

    def init(self, cr):
        ids = self.search(cr, SUPERUSER_ID, [('custom_header', '=', False)])
        for company in self.browse(cr, SUPERUSER_ID, ids):
            company.write({'custom_header': False, 'rml_header_custom': ''})

        sup = super(res_company, self)
        if hasattr(sup, 'init'):
            sup.init(cr)

    def onchange_footer(self, cr, uid, ids, custom_footer, phone, fax, email, website, vat, company_registry, bank_ids,
                        context=None):
        res = super(res_company, self).onchange_footer(cr, uid, ids, custom_footer, phone, fax, email, website, vat,
                                                       company_registry, bank_ids, context)
        value = res.get('value')
        if value:
            for key in value:
                value[key] += '\n<br/>\n' \
                              '<ul class="list-inline">\n' \
                              '<li>Page:</li>\n' \
                              '<li><span class="page"/></li>\n' \
                              '<li>/</li>\n' \
                              '<li><span class="topage"/></li>\n' \
                              '</ul>'
        return res
