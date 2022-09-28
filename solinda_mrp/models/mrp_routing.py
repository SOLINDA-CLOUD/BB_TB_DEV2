from email.policy import default
from odoo import api, fields, models

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    api.depends('shrinkage')
    def _compute_shrinkage(self):
        for line in self:
            res = line.hk - line.hk * line.shrinkage / 100
            line.shkg = res

    qty = fields.Float(string='Qty', related='bom_id.product_qty', store=True)
    fabric_id = fields.Many2one(comodel_name='mrp.bom.line',string='Fabric')
    hk = fields.Float(string='HK', related='fabric_id.product_qty', store=True)
    time_cycle_manual = fields.Float(
        string='Qty', related='bom_id.product_qty', store=True)
    workcenter_id = fields.Many2one(
        'mrp.workcenter', 'Service', required=True, check_company=True)
    color_id = fields.Many2one(comodel_name='dpt.color', string='Color')
    shrinkage = fields.Float(string='Shkg(%)', default=0.0)
    shkg = fields.Float(string='Shkg', compute = _compute_shrinkage)

 