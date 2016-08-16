import logging
from osv import osv, fields

_logger = logging.getLogger(__name__)

class crm_lead(osv.osv):
    _name = "crm.lead"
    _inherit = 'crm.lead'

    _columns = {
        'category_ids': fields.many2many(
            'res.partner.category',
            'crm_lead_partner_category', 'partner_id', 'category_id',
            'Tags'),
        'keyword_ids': fields.many2many(
            'res.partner.keyword',
            'crm_lead_res_partner_keyword', 'lead_id', 'keyword_id',
            'Keywords',
            ),
        }
