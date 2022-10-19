from odoo import _, api, fields, models

class ByProductDummy(models.Model):
    _name = 'by.product.dummy'
    _description = 'By Product Dummy'
    
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    product_uom_qty = fields.Float(string='To Produce')
    colour = fields.Char('Color')
    size = fields.Char('Size')
    remarks = fields.Text('Remarks')
    mrp_id = fields.Many2one('mrp.production', string='MRP')
    fabric_po_id = fields.Many2one('data.fabric.lining', string='Fabric')
    lining_po_id = fields.Many2one('data.fabric.lining', string='Lining')

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    by_product_ids = fields.One2many('by.product.dummy', 'mrp_id', string='By Product')
    
    