from odoo import fields, api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier')
    # payment = fields.Many2one(comodel_name='account.payment.method', related='supplier.property_payment_method_id')
    color = fields.Many2one(comodel_name='dpt.color', string='Color')
    service = fields.Char(string='Fabric', default='FABRIC', readonly=True)
    hk = fields.Float(string='HK', related='bom_line_id.product_qty', store=True)
    purchase_id = fields.Many2one('purchase.order', string='Purchase')
 

    def show_receive_po(self):
        self.purchase_id.action_view_picking()
        return self.purchase_id.action_view_picking()

    def show_po(self):
        if not self.purchase_id:
            raise ValidationError("PO is not defined!\nPlease create PO first")
        return {
                'name': _("Purchase Order"),
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'purchase.order',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'res_id': self.purchase_id.id,
            } 

    def create_po(self):
        self = self.sudo()
        for i in self:
            raw_po_line = []
            total_quant = i.product_qty
            if not i.supplier:
                raise ValidationError("Please input the supplier first")
            po = i.env['purchase.order'].create({'partner_id': i.supplier.id,'state': 'draft','date_approve': datetime.now()})
            if po:
                i.purchase_id = po.id
            raw_po_line.append((0,0, {
                'product_id': i.product_id.id,
                # 'fabric': i.fabric_id.product_id.name,
                # 'lining':'',
                # 'color':'',
                'product_qty': total_quant,
            }))           
            po.update({"order_line": raw_po_line})
            po.button_confirm()
            i.show_po()