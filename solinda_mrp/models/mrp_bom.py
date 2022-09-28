from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    name = fields.Char(
        required=True,
        default='New',
        index=True,
        readonly=True,
        string='Trans No.'
    )

    trans_date = fields.Datetime(
        string='Transaction Date',
        default=fields.Datetime.now,
        index=True,
        required=True,
        readonly=True,
        )
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mrp.bom')
        return super(MrpBom, self).create(vals)
    
    over_packaging = fields.Float(string='Over & Packaging', default=0.00)
    customer = fields.Many2one(comodel_name='res.partner', string='Customer')
    color = fields.Many2one(comodel_name='dpt.color', string='Color')
    categ_id = fields.Many2one('product.category', related='product_tmpl_id.categ_id', string='Group')
    retail_price = fields.Float(related='product_tmpl_id.list_price', string='Retail Price')
    landed_cost = fields.Float(string='Landed Cost')
    landed_quoted = fields.Float(string='Landed Quoted')

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    color = fields.Many2one(comodel_name='dpt.color', string='Color')
    sizes = fields.Many2one(comodel_name='sizes', string='Sizes')
    ratio = fields.Float(string='Ratio', default=1.00)

class Sizes(models.Model):
    _name = 'sizes'
    _description = 'Sizes'

    name = fields.Char(string='Name')

class DptColor(models.Model):
    _name = 'dpt.color'
    _description = 'DPT Color'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

    @api.constrains('name')
    def _check_code_unique(self):
        if self.name:
            ref_counts = self.search_count(
                [('name', '=', self.name), ('id', '!=', self.id)])
            if ref_counts > 0:
                raise ValidationError("Color already exists!")
        else:
            return

    @api.constrains('code')
    def _check_code_unique(self):
        if self.code:
            ref_counts = self.search_count(
                [('code', '=', self.code), ('id', '!=', self.id)])
            if ref_counts > 0:
                raise ValidationError("Code already exists!")
        else:
            return
