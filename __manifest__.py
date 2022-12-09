# -*- coding: utf-8 -*-
{
    'name': "midocean_connector",
    'summary': """Midocean connector for Odoo""",
    'description': """Connect to midocean product platform to fetch product and store in your system""",
    'author': "DERICK TEMFACK",
    'website': "https://github.com/tderick/midocean_connector",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['stock'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        # 'security/ir.model.access.csv',
        'data/cron.xml',
        'views/views.xml',
    ]
}

