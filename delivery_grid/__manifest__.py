# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Delivery grid',
    'version': '0.1',
    'category': 'Delivery',
    'summary': 'Delivery import pricing grid',
    'description': """
This module contains the features for delivery including the prices grid import

    """,
    'depends': ['delivery'],
    'external_dependencies': {'python': ['xlrd']},

    'data': [
    	"security/ir.model.access.csv",
        "views/delivery_carrier.xml",
    	"wizard/import_grid_prices_wizard.xml",

    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False
}
