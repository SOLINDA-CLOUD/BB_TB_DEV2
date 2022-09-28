from odoo import fields, api, models

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    product_service_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('type', '=', 'service')],
        string='Product Service'
        )
