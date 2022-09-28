from odoo import fields, api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier')
    # payment = fields.Many2one(comodel_name='account.payment.method', related='supplier.property_payment_method_id')
    color = fields.Many2one(comodel_name='dpt.color', string='Color')
    service = fields.Char(string='Fabric', default='FABRIC', readonly=True)
    hk = fields.Float(string='HK', related='bom_line_id.product_qty', store=True)