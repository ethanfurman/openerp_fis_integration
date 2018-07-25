import logging
from osv import osv, fields
from fnx.xid import xmlid
from fnx_fs.fields import files
from hr.selections import EmploymentType as ET

_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id'


class hr_employee(xmlid, osv.Model):
    """
    Add fields being mirrored from FIS.
    """
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'fnx_fs.fs']

    _fnxfs_path = 'human_resources/documents'
    _fnxfs_path_fields = ['xml_id', 'name']

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
        'last_raise': fields.date('Last Raise'),
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
        'pension_plan': fields.boolean('Pension Plan'),
        # XXX: moved into hr
        'agency': fields.char('Agency', size=128),
        'relations_fnxfs_files': files('', string='Relations Documents'),
        'fleet_fnxfs_files': files('', string='Fleet Documents'),
        'insurance_fnxfs_files': files('', string='Insurance Documents'),
        'workers_comp_fnxfs_files': files('', string='Workers Comp Documents'),
        }

    fields.apply_groups(
            _columns,
            {
                'base.group_user': ['xml_id', 'module'],
                'base.group_hr_manager': ['.*'],
                })

    def change_employment_type(self, cr, uid, ids, employment, xml_id, context=None):
        res = {}
        if ET[employment] is ET.standard and not xml_id:
            res['warning'] = {
                    'title': 'Not Allowed',
                    'message': 'Permanent employees can only be created in FIS',
                    }
            res['value'] = {'employment_type': 'temporary'}
        elif employment == '':
            res['warning'] = {
                    'title': 'Not Allowed',
                    'message': 'Employment Status can not be blank.',
                    }
            res['value'] = {'employment_type': 'temporary'}
        return res

    def fnxfs_folder_name(self, records):
        "return name of folder to hold related files"
        res = {}
        for record in records:
            res[record['id']] = record['xml_id'] or record['name']
        return res
