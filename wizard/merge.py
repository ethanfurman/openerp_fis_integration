import logging
from osv import osv, fields
from osv.osv import except_osv as ERPError

_logger = logging.getLogger(__name__)

FIS_MODULES = 'F33', 'F65', 'F163'

class res_partner_merge(osv.TransientModel):
    _name = 'fis_integration.res.partner.merge'
    _description = 'merge res.partner records'

    _columns = {
        'possible_records': fields.one2many('fis_integration.res.partner.merge.sub', 'master_id', 'Possibles'),
        }

    def merge(self, cr, uid, ids, context=None):
        pass

    def default_get(self, cr, uid, fields=None, context=None):
        ctx = context or {}
        source_ids = ctx.get('active_ids', [])
        if not source_ids or 'possible_records' not in (fields or []):
            return super(res_partner_merge, self).default_get(cr, uid, fields=fields, context=context)

        partners = []
        res_partner = self.pool.get('res.partner')
        all_records = set()
        records = res_partner.browse(cr, uid, source_ids, context=None)
        for rec in records:
            all_records.add(rec)
            for rec in rec.child_ids:
                all_records.add(rec)
        for record in all_records:
            if record.xml_id and record.xml_id.startswith('cntct_'):
                disp = 'ignore'
            elif record.module in FIS_MODULES:
                disp = 'master'
            elif record.is_company and not record.child_ids:
                disp = 'ignore'
            else:
                disp = 'keep'
            partners.append(dict(
                    source_id=record.id,
                    orig_source_id=record.id,
                    parent_name=record.parent_name,
                    city=record.city,
                    state=record.state_id and record.state_id.code or False,
                    phone=record.phone,
                    disposition=disp,
                    active=True,
                    xml_id=record.xml_id,
                    module=record.module,
                    ))
        result = {}.fromkeys(fields)
        partners.sort(
            key=lambda p:
                (chr(0),) if p['disposition'] == 'master' else
                (chr(127), chr(127), chr(127)) if p['disposition'] == 'ignore' else
                (p['state'][1], p['city'], (chr(0), chr(1))[bool(p['parent_name'])])
            )
        result['possible_records'] = partners
        return result

    def create(self, cr, uid, values, context=None):
        # perform sanity check
        # - if any FIS companies in group they are either Master or Exclude
        # - one, and only one, record is marked as Master, and it is a company
        # - real FIS contacts are not being reassigned to other companies
        master = []
        include = []
        convert = []
        delete = []
        if values and 'possible_records' in values:
            res_partner = self.pool.get('res.partner')
            possible_records = [t[2] for t in values['possible_records'] if t[0] == 0]
            source_ids = [p['source_id'] for p in possible_records]
            source_recs = dict([(r.id, r) for r in res_partner.browse(cr, uid, source_ids, context=context)])
            for prec in possible_records:
                srec = source_recs[prec['source_id']]
                if prec['disposition'] == 'ignore':
                    pass
                elif prec['disposition'] == 'master':
                    if not srec.is_company:
                        raise ERPError(
                                'Merge Status Error',
                                'Only companies can be Master [%r is a contact]' % srec.name,
                                )
                    master.append(prec)
                elif prec['disposition'] == 'keep':
                    # check that FIS company records are not in this category
                    if srec.module in FIS_MODULES and not srec.xml_id.startswith('cntct_'):
                        raise ERPError(
                                'Merge Status Error',
                                '%s is a company and must be Master or Exclude' % srec.name,
                                )
                    if srec.is_company and not srec.child_ids:
                        # ignore companies without contacts (they should be 'convert' or 'delete')
                        prec['disposition'] = 'ignore'
                    else:
                        include.append(prec)
                elif prec['disposition'] == 'convert':
                    # verify this is a company
                    if srec.is_company:
                        convert.append(prec)
                    else:
                        prec['disposition'] = 'ignore'
                elif prec.disposition == 'delete':
                    delete.append(prec)
                else:
                    # shouldn't happen
                    raise ERPError(
                            'Logic Error',
                            'unknown disposition %r for record %r' % (prec['disposition'], prec),
                            )
            if len(master) != 1:
                raise ERPError(
                        'Merge Status Error',
                        'Must have 1, and only 1, record marked as Master',
                        )
            master = source_recs[master[0]['source_id']]
            # segregate merging companies / contacts
            merge_companies = {}
            merge_contacts = {}
            for prec in include:
                srec = source_recs[prec['source_id']]
                # make sure we're not changing FIS contacts
                if srec.xml_id and srec.xml_id.startswith('cntct_') and srec.xml_id.split('_')[1] != master.xml_id:
                    raise ERPError(
                            'Merge Status Error',
                            'Cannot merge FIS contact %r to %r' % (srec.xml_id, master.xml_id),
                            )
                if source_recs[prec['source_id']].is_company:
                    merge_companies[prec.source_id] = prec
                else:
                    merge_contacts[prec['source_id']] = prec
            # segregate deleting companies / contacts
            delete_companies = {}
            delete_contacts = {}
            for prec in delete:
                srec = source_recs[prec['source_id']]
                # make sure we're not changing FIS contacts
                if srec.xml_id and srec.xml_id.startswith('cntct_'):
                    raise ERPError(
                            'Merge Status Error',
                            'Cannot delete FIS contact %r' % srec.xml_id,
                            )
                if source_recs[prec['source_id']].is_company:
                    delete_companies[prec.source_id] = prec
                else:
                    delete_contacts[prec['source_id']] = prec
            # start merge
            handled_ids = set()
            # first move contacts
            target_ids = []
            for partner_id, prec in merge_contacts.items():
                target_ids.append(partner_id)
                prec['active'] = False
            if target_ids:
                res_partner.write(
                        cr, uid, target_ids,
                        {'type': 'contact', 'parent_id': master.id},
                        context=context,
                        )
                handled_ids |= set(target_ids)
            # then delete contacts
            target_ids = []
            for partner_id, prec in delete_contacts.items():
                target_ids.append(partner_id)
                prec['active'] = False
            if target_ids:
                res_partner.write(
                        cr, uid, target_ids,
                        {'type': 'contact', 'parent_id': False, 'active': False},
                        context=context,
                        )
                handled_ids |= set(target_ids)
            # then delete/merge companies
            target_ids = []
            for partner_id, prec in delete_companies.items():
                srec = source_recs[prec['source_id']]
                target_ids.append(partner_id)
                prec['active'] = False
                srec = source_recs[prec['source_id']]
                if srec.child_ids:
                    children = set([c.id for c in srec.child_ids])
                    if children & handled_ids != children:
                        raise ERPError(
                                'Merge Status Error',
                                'Cannot delete company unless its contacts are merged/deleted: %s, %s, %s'
                                    % (srec.name, srec.city, srec.state_id.name),
                                )
            for partner_id, prec in merge_companies.items():
                srec = source_recs[prec['source_id']]
                target_ids.append(partner_id)
                prec['active'] = False
                srec = source_recs[prec['source_id']]
                if srec.child_ids:
                    children = set([c.id for c in srec.child_ids])
                    if children & handled_ids != children:
                        raise ERPError(
                                'Merge Status Error',
                                'Cannot merge company unless its contacts are merged/deleted: %s, %s, %s'
                                    % (srec.name, srec.city, srec.state_id.name),
                                )
            if target_ids:
                res_partner.write(
                        cr, uid, target_ids,
                        {'active': False},
                        context=context,
                        )
                handled_ids |= set(target_ids)
            # then do converts
            target_ids = []
            for prec in convert:
                print 'checking', prec
                srec = source_recs[prec['source_id']]
                target_ids.append(prec['source_id'])
                prec['active'] = False
                srec = source_recs[prec['source_id']]
                if srec.child_ids:
                    children = set([c.id for c in srec.child_ids])
                    if children & handled_ids != children:
                        raise ERPError(
                                'Merge Status Error',
                                'Cannot convert company unless its contacts are merged/deleted: %s, %s, %s'
                                    % (srec.name, srec.city, srec.state_id.name),
                                )
            print target_ids
            if target_ids:
                print 'result is', res_partner.write(
                        cr, uid, target_ids,
                        {'type': 'contact', 'parent_id': master.id, 'is_company': False},
                        context=context)
            # done!
        # return to normal programming ;)
        return super(res_partner_merge, self).create(cr, uid, values, context=context)


class res_partner_merge_sub(osv.TransientModel):
    _name = 'fis_integration.res.partner.merge.sub'

    _columns = {
        'active': fields.boolean('Active'),
        'master_id': fields.many2one('fis_integration.res.partner.merge'),
        'source_id': fields.many2one('res.partner', 'Source Record'),
        'orig_source_id': fields.many2one('res.partner', 'Backup Source Record'),
        'disposition': fields.selection(
            (
                ('master', 'Master'),
                ('ignore', 'Exclude'),
                ('keep', 'Yes'),
                ('convert', 'Convert'),
                ('delete', 'Delete'),
                ),
            'Merge',
            sort_order='definition',
            ),
        'name': fields.related('source_id', 'name', type='char', size=128, string='Name'),
        'parent_name': fields.related('source_id', 'parent_id', 'name', type='char', size=128, string='Related'),
        'city': fields.related('source_id', 'city', type='char', size=128, string='City'),
        'state': fields.related('source_id', 'state_id', 'code', type='char', size=5, string='State'),
        'country': fields.related('source_id', 'country_id', 'name', type='char', size=128, string='Country'),
        'phone': fields.related('source_id', 'phone', type='char', size=64, string='Phone'),
        'xml_id': fields.related('source_id', 'xml_id', type='char', size=16, string='FIS ID'),
        'module': fields.related('source_id', 'module', type='char', size=16, String='FIS Module'),
        'is_company': fields.related('source_id', 'is_company', type='boolean', string='Company'),
        'child_ids': fields.related('source_id', 'child_ids', type='one2many', string='Contacts'),
        }

    def onchange_source(self, cr, uid, ids, orig_source_id, context=None):
        return {'warning': {
                    'title': 'Error',
                    'message': 'Switching source record is not allowed, only changing the Merge status',
                    },
                'value': {
                    'source_id': orig_source_id,
                    },
                }

