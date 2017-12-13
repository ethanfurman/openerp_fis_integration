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
            "hr",
            "product",
            "project",
            "sample",
            ],
    'data': [
            'hr_employee_view.xaml',
            'res_config_view.xaml',
            'res_partner_view.xaml',
            'product_view.xaml',
            'project_view.xaml',
            'crm_lead_view.xaml',
            'security/fis_security.xaml',
            'security/ir.model.access.csv',
            'wizard/merge_view.xaml',
            ],
    'css': [
            'static/src/css/fis.css',
            ],
    'js': [
            'static/src/js/fis.js',
            ],
    'test': [],
    'installable': True,
    'active': False,
}
