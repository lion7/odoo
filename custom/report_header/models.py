# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _


class res_company(osv.Model):
    _inherit = 'res.company'

    _columns = {
        'rml_header_custom': fields.text('Report Header', help="Header text displayed at the top of all reports."),
        'rml_header_custom_readonly': fields.related('rml_header_custom', type='text', string='Report Header',
                                                     readonly=True),
        'custom_header': fields.boolean("Custom Header",
                                        help='Check this to define the report header manually. '
                                             'Otherwise it will be filled in automatically.'),
    }

    def onchange_header(self, cr, uid, ids, custom_header, phone, fax, email, website, vat, company_registry, bank_ids,
                        context=None):
        if custom_header:
            return {}

        # first line (notice that missing elements are filtered out before the join)
        res = ' | '.join(filter(bool, [
            phone            and '%s: %s' % (_('Phone'), phone),
            fax              and '%s: %s' % (_('Fax'), fax),
            email            and '%s: %s' % (_('Email'), email),
            website          and '%s: %s' % (_('Website'), website),
            vat              and '%s: %s' % (_('TIN'), vat),
            company_registry and '%s: %s' % (_('Reg'), company_registry),
            ]))
        # second line: bank accounts
        res_partner_bank = self.pool.get('res.partner.bank')
        account_data = self.resolve_2many_commands(cr, uid, 'bank_ids', bank_ids, context=context)
        account_names = res_partner_bank._prepare_name_get(cr, uid, account_data, context=context)
        if account_names:
            title = _('Bank Accounts') if len(account_names) > 1 else _('Bank Account')
            res += '\n%s: %s' % (title, ', '.join(name for id, name in account_names))

        return {'value': {'rml_header_custom': res, 'rml_header_custom_readonly': res}}
