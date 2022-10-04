from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class VariantDetail(models.Model):
    _name = 'variant.detail'
    _description = 'Variant Detail'
    
    product_id = fields.Many2one('product.product', string='Product')
    product_template_variant_value_ids = fields.Many2many('product.template.variant.value', string='Variant')
    product_qty = fields.Float('Quantity To Produce',default=1.0, digits='Product Unit of Measure',readonly=True, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',related="product_id.uom_id")
    breakdown_id = fields.Many2one('mrp.breakdown', string='Breakdown')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for i in self:
            i.write({
                'product_template_variant_value_ids' : [(6,0,i.product_id.product_template_variant_value_ids.ids)],
                'uom_id' : i.product_id.uom_id.id
            })


class MrpBreakdown(models.Model):
    _name = 'mrp.breakdown'
    _description = 'Mrp Breakdown'
    _inherit = 'mail.thread'

    name = fields.Char('Name',tracking=True,default=lambda x: _('New'))
    product_id = fields.Many2one('product.template', string='Product',tracking=True)
    bom_id = fields.Many2one('mrp.bom', string='Bill of Material',tracking=True, help="Bill of Materials allow you to define the list of required components to make a finished product.")
    customer_id = fields.Many2one('res.partner', string='Customer',tracking=True)
    purchase_id = fields.Many2one('purchase.order', string='Purchase',tracking=True)
    product_qty = fields.Float('Quantity',default=1.0,readonly=True, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',related="product_id.uom_id")
    variant_detail_ids = fields.One2many('variant.detail', 'breakdown_id', string='Variant Detail')

    def break_down_to_mo(self):
        for i in self:
            if i.product_id.product_variant_ids:
                for l in i.product_id.product_variant_ids:
                    mo_temp = self.env["mrp.production"].create({
                        "product_id": ,
                        })

    # product_uom_qty = fields.Float(string='Total Quantity', compute='_compute_product_uom_qty', store=True)
    # picking_type_id = fields.Many2one(
    #     'stock.picking.type', 'Operation Type',
    #     domain="[('code', '=', 'mrp_operation'), ('company_id', '=', company_id)]",
    #     default=_get_default_picking_type, required=True, check_company=True)


