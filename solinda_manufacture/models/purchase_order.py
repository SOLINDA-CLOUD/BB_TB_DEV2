from odoo import _, api, fields, models
from datetime import date,datetime

class TempProductMo(models.Model):
    _name = 'temp.product.mo'
    _description = 'Temp Product Mo'
    
    product_tmpl_id = fields.Many2one('product.template', string='Product')
    product_qty = fields.Float('Quantity')
    purchase_id = fields.Many2one('purchase.order', string='Purchase')
    

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    temp_prodmo_ids = fields.One2many('temp.product.mo', 'purchase_id', string='Temp Product MO')
    breakdown_id = fields.Many2one('mrp.breakdown', string='Breakdown')

    @api.onchange('order_line.product_id')
    def _onchange_order_line_product_id(self):
        temp2 = []
        for i in self:
            # temp = i.order_line.mapped('product_id.product_tmpl_id'):
            for l in i.order_line:
                if l.product_id.product_tmpl_id.product_variant_count >0:
                    temp2.append((0,0,{'product_tmpl_id':l.product_tmpl_id.id,'product_qty':l.product_qty}))
            i.temp_prodmo_ids = [(5,0,0)]
            i.write({'temp_prodmo_ids':temp2})

    def create_mrp_breakdown(self):
        self = self.sudo()
        breakdown = ''
        for i in self:
            for l in i.temp_prodmo_ids:
                breakdown = self.env["mrp.breakdown"].create({
                            # 'name': ,
                            'product_id': l.id,
                            'customer_id': i.partner_id.id,
                            'purchase_id': i.id,
                            'uom_id':l.product_tmpl_id.uom_id.id,
                            'product_qty':l.product_qty
                        })
                if breakdown:
                    i.breakdown_id = breakdown.id
        
                    return {
                        'name': _("Manufacturing"),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'res_model': 'temp.product.mo',
                        'type': 'ir.actions.act_window',
                        # 'target': 'new',
                        'res_id': breakdown.id,
                    } 