from odoo import _, fields, api, models

class PurchaseOrder(models.Model):
  _inherit = 'purchase.order'

  attention = fields.Char(string='Attention')
  supplier = fields.Char('Supplier')
  sub_suplier = fields.Char('Sub Suplier')
  brand = fields.Char('Brand')
  buyer = fields.Char('Buyer')

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
  fabric = fields.Char(string='Fabric')
  lining = fields.Char(string='Lining')
  color = fields.Char(string='Color')
  label = fields.Char(string='Label')
  # type = fields.Many2one(comodel_name='type.model', string='Type')
  type = fields.Char(string='Size')
  prod_comm = fields.Html(string='Production Comment')

  @api.onchange('product_id')
  def _onchange_image(self):
      if self.product_id:
          self.image = ''
          if self.product_id.image_1920:
            self.image = self.product_id.image_1920
          self.image = self.image
