
from odoo import models, fields, api

class Picking(models.Model):
  _inherit = 'stock.picking'

  origin_pr = fields.Many2one('purchase.request', 'Source Document', index=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, help="Reference of the document")

class StockPickingType(models.Model):
  _inherit = 'stock.picking.type'

  mandatory_source = fields.Boolean('Required Source Documents', default=False)