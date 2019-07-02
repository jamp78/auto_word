# -*- coding: utf-8 -*-
{
    'name': "auto_word",

    'summary': """
        This is an auto write program for wind.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Zhirun Company",
    'website': "http://www.cr-power.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/auto_word_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/project/project_view.xml',
        'views/project/project_null_view.xml',
        'views/wind/wind_turbines_view.xml',
        'views/wind/wind_view.xml',
        'views/wind/wind_res_view.xml',
        'views/electrical/electrical_view.xml',
        'views/civil/civil_view.xml',
        'views/civil/civil_database_view.xml',
        'views/civil/civil_design_safety_standard_view.xml',
        'views/wind/wind_turbines_compare_view.xml',
        'views/wind/wind_turbine_selection_view.xml',
        'views/economy/economy_view.xml',
        'views/electrical/electrical_firstsec_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}