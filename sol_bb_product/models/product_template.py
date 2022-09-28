from odoo import fields, models, api, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # @api.constrains('default_code')
    # def _check_code_unique(self):
    #     if self.default_code:
    #         ref_counts = self.search_count(
    #             [('default_code', '=', self.default_code), ('id', '!=', self.id)])
    #         if ref_counts > 0:
    #             raise ValidationError("Internal Reference already exists!")
    #     else:
    #         return

    brand = fields.Many2one('product.brand', string='Brand')
    stock_type = fields.Many2one('stock.type', string='Stock Type')

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(string='Name')

class StockType(models.Model):
    _name = 'stock.type'
    _description = 'Stock Type'

    name = fields.Char(string='Name')