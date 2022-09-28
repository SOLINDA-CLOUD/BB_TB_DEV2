from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    trans_date = fields.Datetime(
        string='Transaction Date',
        default=fields.Datetime.now,
        index=True,
        required=True,
        readonly=True,
        )

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production')
        return super(MrpProduction, self).create(vals)

    customer = fields.Many2one(related='bom_id.customer', string='Customer', store=True)
    retail_price = fields.Float(related='bom_id.retail_price', string='Retail Price', store=True)
    sales_order_id = fields.Many2one(comodel_name='sale.order', string='SO No.')
    po_no = fields.Char(string='PO No.')