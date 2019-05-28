from openerp.osv import fields, osv

class res_company(osv.Model):
    _inherit = "res.company"
    _columns = {
            'traffic_followers_ids': fields.many2many('res.users', 'fal_rescompany_rel', 'fal_tf_cid', 'fal_tf_uid', string='Traffic Report Auto-Followers'),
            }
res_company()
