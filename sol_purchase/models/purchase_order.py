from odoo import _, fields, api, models

class BuyerComp(models.Model):
  _name = 'buyer.comp'
  name = fields.Char('buyer')

class AttComp(models.Model):
  _name = 'att.comp'
  name = fields.Char('attention')

class LabelComp(models.Model):
  _name = 'label.comp'
  name = fields.Char('Label')

class PurchaseOrder(models.Model):
  _inherit = 'purchase.order'

  attention = fields.Many2one(comodel_name='att.comp', string='Attention')
  sub_suplier = fields.Many2one('res.partner', string='Sub Supplier')
  brand = fields.Many2one('product.brand', string='Brand')
  buyer = fields.Many2one(comodel_name='buyer.comp',string='Buyer')
  
  supplier_po = fields.Char('Supplier PO')
  po = fields.Char('PO')
  ordering_date = fields.Date(string='Delivery Date', states={'purchase': [('readonly', True)]})
  delivery_date = fields.Date(states={'purchase': [('readonly', True)]})

  @api.model
  def create(self, vals):
      res = super(PurchaseOrder, self).create(vals)
      res.name = self.env["ir.sequence"].next_by_code("purchase.order.seq")
      return res

class PurchaseOrderLine(models.Model):
  _inherit = 'purchase.order.line'

  product_id = fields.Many2one(string='Style Name')
  image = fields.Image(string='Image')
  fabric_po = fields.Many2one('data.fabric.lining', string='Fabric')
  lining_po = fields.Many2one('data.fabric.lining', string='Lining')

  color = fields.Many2many('product.template.attribute.value', string="Color")
  size = fields.Many2one('product.template.attribute.value', string="Size")

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
  def _onchange_color(self):
    if self.product_id:
      color = ''
      if self.product_id.product_template_variant_value_ids:
        self.color = self.product_id.product_template_variant_value_ids
      return color

  # @api.onchange('product_id')
  # def _onchange_size(self):
  #   if self.product_id:
  #     size = ''
  #     if self.product_id.product_template_variant_value_ids:
  #       self.size = self.product_id.product_template_variant_value_ids
  #     return size

