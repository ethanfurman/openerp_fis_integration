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
    'update_xml': [
            'res_config_view.xaml',
            'res_partner_view.xaml',
            'product_view.xaml',
            'crm_lead_view.xaml',
            'security/fis_security.xaml',
            'security/ir.model.access.csv',
        ],
    'test': [],
    'installable': True,
    'active': False,
}
