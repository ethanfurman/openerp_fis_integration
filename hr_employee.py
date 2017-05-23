import logging
from osv import osv, fields
from fnx.xid import xmlid

_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id'


class hr_employee(xmlid, osv.Model):
    """
    Add fields being mirrored from FIS.
    """
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'hire_date': fields.date('Date Hired'),
        'fire_date': fields.date('Date Terminated'),
        'status_flag': fields.char('Status Flag', size=1),
        'pay_type': fields.selection([('hourly','Hourly'),('salary','Salary')], 'Pay Type'),
        'federal_exemptions': fields.integer('Federal Exemptions'),
        'state_exemptions': fields.integer('State Exemptions'),
        'hourly_rate': fields.float('Hourly Rate'),
        'race': fields.selection([
            ('white', 'White'),
            ('black', 'Black / African American'),
            ('latino', 'Hispanic / Latino'),
            ('indian', 'American Indian / Alaskan Native'),
            ('asian', 'Asian'),
            ('islander', 'Native Hawaiian / Pacific Islander'),
            ('multiple', 'Two or more races'),
            ],
            'Race/Ethnicity',
            sort_order='definition',
            ),
        # TODO: make agency a many2one field
        'agency': fields.char('Agency', size=128),
        }

    fields.apply_groups(
            _columns,
            {'base.group_hr_manager': ['.*']},
            )
