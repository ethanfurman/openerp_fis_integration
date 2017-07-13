from openerp.osv import fields, osv

class sample_product(osv.Model):
    _name = 'sample.product'
    _inherit = 'sample.product'

    _columns = {
        'xml_id': fields.related('product_id', 'xml_id', string='FIS ID'),
        'module': fields.related('product_id', 'module', string='FIS Module'),
        }

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            junctor = ('|', '&')['not' in operator or operator == '!=']
            args.extend([junctor, (self._rec_name, operator, name), ('xml_id', operator, name)])
            name = ''
            operator = 'ilike'
        return super(sample_product, self).name_search(
                cr, uid,
                name=name,
                args=args,
                operator=operator,
                context=context,
                limit=limit,
                )

