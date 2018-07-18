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
    _name_rec = 'abbr'

    _columns = {
        'xml_id': fields.char('FIS Code', size=3),
        'module': fields.char('FIS Module', size=4),
        'fis_name': fields.char('FIS Name', size=128, readonly=True),
        'user_id': fields.many2one('res.users', 'Salesperson'),
        }

