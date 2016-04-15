# -*- coding: utf-8 -*-
{
    'name': "report_business_paper",

    'summary': """
        Report business paper""",

    'description': """
        Allows to define report business paper.
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
        'views/templates.xml',
        'views/report.xml',
        'views/menu.xml',
    ],
}