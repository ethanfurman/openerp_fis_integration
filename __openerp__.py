{
   'name': 'FIS Integration',
    'version': '0.9',
    'category': 'Generic Modules',
    'description': """\
            """,
    'author': 'Emile van Sebille',
    'maintainer': 'Emile van Sebille',
    'website': 'www.openerp.com',
    'depends': [
            "base",
            "crm",
            "fnx",
            "product",
            "stock",
            ],
    'init_xml': [
            'security/ir.model.access.csv',
        ],
    'update_xml': [
            'res_config_view.xml',
            'res_partner_view.xml',
            'product_view.xml',
        ],
    'test': [],
    'installable': True,
    'active': False,
}
