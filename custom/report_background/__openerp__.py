# -*- coding: utf-8 -*-
{
    'name': "Report Background",

    'summary': """
        Add a background to your reports""",

    'description': """
        Allows to define a report background.\n
        Usually you'd want to change the following reports:\n
        - account.report_invoice_document
    """,

    'author': "LeeuwIT",
    'website': "http://www.leeuwit.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Advanced Reporting',
    'version': '0.1',
    #'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'report'],

    # always loaded
    'data': [
        'views/menu.xml',
    ],
}