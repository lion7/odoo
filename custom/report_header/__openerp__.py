# -*- coding: utf-8 -*-
{
    'name': "Report customization - header",

    'summary': """
        Add a custom header to your reports""",

    'description': """
        Allows to define the report header manually.
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
        'views/templates.xml',
    ],
}