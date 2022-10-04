from odoo import _, fields, api, models

class BuyerComp(models.Model):
  _name = 'buyer.comp'
  name = fields.Char('buyer')

class BrandComp(models.Model):
  _name = 'brand.comp'
  name = fields.Char('Brand')

class SubSupplierComp(models.Model):
  _name = 'sub.supplier.comp'
  name = fields.Char('sub supplier')

class SupplierComp(models.Model):
  _name = 'supplier.comp'
  name = fields.Char('supplier')

class LabelComp(models.Model):
  _name = 'label.comp'
  name = fields.Char('Label')

class PurchaseOrder(models.Model):
  _inherit = 'purchase.order'

  attention = fields.Many2one('res.partner', string='Attention')
  supplier = fields.Many2one(comodel_name='supplier.comp',string='Supplier')
  sub_suplier = fields.Many2one(comodel_name='sub.supplier.comp',string='Sub Supplier')
  brand = fields.Many2one(comodel_name='brand.comp',string='Brand')
  buyer = fields.Many2one(comodel_name='buyer.comp',string='Buyer')

  supplier_po = fields.Char('Supplier PO')
  po = fields.Char('PO')

  @api.model
  def create(self, vals):
      res = super(PurchaseOrder, self).create(vals)
      res.name = self.env["ir.sequence"].next_by_code("purchase.order.seq")
      return res

class PurchaseOrderLine(models.Model):
  _inherit = 'purchase.order.line'

  product_id = fields.Many2one(string='Style Name')
  image = fields.Image(string='Image')
  fabric_po = fields.Char(string='Fabric')
  lining_po = fields.Char(string='Lining')
  color = fields.Many2many('product.template.attribute.value', string="Size and Color")
  label = fields.Many2one(comodel_name='label.comp', string='Label')
  prod_comm = fields.Html(string='Production Comment')

  @api.onchange('product_id')
  def _onchange_image(self):
    if self.product_id:
      image = ''
      if self.product_id.image_1920:
        self.image = self.product_id.image_1920
      return image

  @api.onchange('product_id')
  def _onchange_color_size(self):
    if self.product_id:
      color = ''
      if self.product_id.product_template_variant_value_ids:
        self.color = self.product_id.product_template_variant_value_ids
      return color
