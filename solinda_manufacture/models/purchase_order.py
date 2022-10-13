from odoo import _, api, fields, models
from datetime import date,datetime
from odoo.exceptions import ValidationError

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
    mrp_ids = fields.Many2many('mrp.production', string='MO')
    mrp_count = fields.Integer('Mrp Count')

    @api.depends('mrp_ids')
    def _compute_mrp_count(self):
        for i in self:
            i.mrp_count = len(i.mrp_ids.ids)

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

    def show_mrp_prod(self):
        return {
            'name': _("Manufacturing Order"),
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', self.mrp_ids.ids)],
            'context': {'create': False}
        }

    def create_mo_production(self):
        mrp,mo_line = [],[]
        BoM = False
        self = self.sudo()
        for i in self:
            if i.mrp_count > 0:
                return i.show_mrp_prod()
            else:
                company = self.env["res.company"].search([('is_manufacturing', '=', True)],limit=1)
                if not company:
                    raise ValidationError("Company for manufacture is not defined")
                header_product = i.order_line.filtered(lambda x: x.product_id.detailed_type in ['consu','product'])[0]
                prod_template = i.order_line.mapped('product_id.product_tmpl_id.id')
                # if len(prod_template) > 1:
                #     return
                # else:
                #     return
                
                for l in header_product:
                    if l.product_id:
                        if l.product_id.bom_count > 0:
                            BoM = self.env["mrp.bom"].search([('product_id', '=', l.product_id.id)],order = 'retail_price desc',limit=1).id
                        mp = self.env["mrp.production"].create({
                            'name': _('New'),
                            'product_id': l.product_id.id,
                            'product_qty': l.product_qty,
                            'product_uom_id':l.product_uom.id,
                            'bom_id':BoM,
                            'date_planned_start':datetime.now(),
                            'user_id': i.env.user.id,
                            'company_id': company.id,
                            'purchase_id':i.id,
                            })
                        if mp:
                            mrp.append(mp.id)
                            for j in i.order_line:
                                mo_line.append((0,0, {
                                    'name': _('New'),
                                    'product_id': j.product_id.id,
                                    # 'location_dest_id': False,
                                    'product_uom_qty': j.product_qty,
                                    'product_uom': j.product_id.uom_id.id,
                                }))
                            mp.update({'move_byproduct_ids':mo_line})
                i.write({'mrp_ids' : [(6,0,mrp)]})
                return i.show_mrp_prod()

    def create_mrp_production(self):
        mrp = []
        BoM = False
        self = self.sudo()
        for i in self:
            if i.mrp_count > 0:
                return i.show_mrp_prod()
            else:
                company = self.env["res.company"].search([('is_manufacturing', '=', True)],limit=1)
                if not company:
                    raise ValidationError("Company for manufacture is not defined")
                for l in i.order_line:
                    if l.product_id:
                        if l.product_id.bom_count > 0:
                            BoM = self.env["mrp.bom"].search([('product_id', '=', l.product_id.id)],order = 'retail_price desc',limit=1).id
                        mp = self.env["mrp.production"].create({
                            'name': _('New'),
                            'product_id': l.product_id.id,
                            'product_qty': l.product_qty,
                            'product_uom_id':l.product_uom.id,
                            'bom_id':BoM,
                            'date_planned_start':datetime.now(),
                            'user_id': i.env.user.id,
                            'company_id': company.id,
                            'purchase_id':i.id,
                            })
                        if mp:
                            mrp.append(mp.id)
                i.write({'mrp_ids' : [(6,0,mrp)]})
                return i.show_mrp_prod()
    

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
                        'res_id': breakdown.id,
                    } 