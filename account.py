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

