from openerp.osv import fields, osv

class res_users(osv.Model):
    """ Update of res.users class
        - add link to the FIS partner account
    """
    _name = 'res.users'
    _inherit = ['res.users']

    _columns = {
        'fis_partner_id': fields.many2one('res.partner', string='FIS Account'),
        }
