import logging
from osv import osv, fields
from fnx.xid import xmlid

_logger = logging.getLogger(__name__)


class fis_account_customer_terms(xmlid, osv.Model):
    """
    Track FIS customer terms.
    """
    _name = 'fis.account.customer_terms'
    _rec_name = 'description'

    _columns = {
        'xml_id': fields.char('FIS Code', size=1),
        'module': fields.char('FIS Module', size=4),
        'description': fields.char('Description', size=64),
        }


class fis_account_salesperson(xmlid, osv.Model):
    """
    Mapping of abbreviations with salespeople.
    """
    _name = 'fis.account.salesperson'
    _rec_name = 'xml_id'

    _columns = {
        'xml_id': fields.char('FIS Code', size=3, readonly=True),
        'module': fields.char('FIS Module', size=4, readonly=True),
        'fis_name': fields.char('FIS Name', size=128, readonly=True),
        'ordered_by_no': fields.char('FIS Ordered By #', size=2, readonly=True),
        'user_id': fields.many2one(
                'res.users',
                'Salesperson',
                domain=[('groups_id','=',fields.ref('base.group_sale_salesman'))],
                ),
        }

    def write(self, cr, uid, ids, values, context=None):
        # each id represents one sales rep
        # if user_id changes:
        # - find current res.partner records linked to that sales rep
        # - update them to the new res.users id of the now current sales rep
        if not ids or 'user_id' not in values:
            return super(fis_account_salesperson, self).write(cr, uid, ids, values, context=context)
        #
        # get current mapping of FIS sales rep to user login
        #
        old_salesreps = dict([
            (r['id'], r['user_id'])
            for r in self.read(cr, uid, ids, fields=['id', 'user_id'], context=context)
            ])
        result = super(fis_account_salesperson, self).write(cr, uid, ids, values, context=context)
        if not result:
            return result
        #
        # get new mapping of FIS sales rep to user login
        #
        new_salesreps = dict([
            (r['id'], r['user_id'])
            for r in self.read(cr, uid, ids, fields=['id', 'user_id'], context=context)
            ])
        res_partner = self.pool.get('res.partner')
        for id in ids:
            old_user_id = old_salesreps[id]
            if not old_user_id:
                # do not change records with no assigned sales rep
                continue
            old_user_id = old_user_id[0]
            new_user_id = new_salesreps[id] and new_salesreps[id][0] or False
            customer_ids = res_partner.search(cr, uid, [('user_id','=',old_user_id)], context=context)
            if not res_partner.write(cr, uid, customer_ids, {'user_id': new_user_id}, context=context):
                return False
        return result
