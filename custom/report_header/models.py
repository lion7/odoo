# -*- coding: utf-8 -*-

from functools import partial

from openerp import SUPERUSER_ID
from openerp.osv import osv, fields


class res_company(osv.Model):
    _inherit = 'res.company'

    _columns = {
        'custom_header': fields.boolean("Custom Header",
                                        help='Check this to define the report header manually.  Otherwise it will be filled in automatically.'),
        'rml_header_custom': fields.text("Report Header", help='Header text displayed at the top of all reports.'),
    }

    def init(self, cr):
        ids = self.search(cr, SUPERUSER_ID, [('custom_header', '=', False)])
        for company in self.browse(cr, SUPERUSER_ID, ids):
            company.write({'custom_header': False, 'rml_header_custom': 'Example header'})

        sup = super(res_company, self)
        if hasattr(sup, 'init'):
            sup.init(cr)
