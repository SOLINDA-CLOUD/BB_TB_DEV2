from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    order_id = fields.Many2one(comodel_name='purchase.order',string='PO')
    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier')
    fabric_id = fields.Many2one(comodel_name='mrp.bom.line',string='Fabric', related='production_bom_id.operation_ids.fabric_id', store=True)
    hk = fields.Float(string='HK', related='production_bom_id.operation_ids.hk', store=True)
    color_id = fields.Many2one(comodel_name='dpt.color', string='Color', related='production_bom_id.operation_ids.color_id', store=True)
    shrinkage = fields.Float(string='Shkg(%)', default=0.0)
    duration_expected = fields.Float(
        'Expected Duration',
        digits=(16, 2),
        default=1.0,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Expected duration (in minutes)")
    in_date = fields.Date('In Date')
    out_date = fields.Date('Out Date')
    picking_ids = fields.Many2many('stock.picking', string='Receive',related="order_id.picking_ids")

    def show_receive_po(self):
        self.order_id.action_view_picking()

    def show_po(self):
        if not self.order_id:
            raise ValidationError("PO is not defined!\nPlease create PO first")
        return {
                'name': _("Purchase Order"),
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'purchase.order',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'res_id': self.order_id.id,
            } 

    def create_po(self):
        for i in self:
            raw_po_line = []
            i.button_start()
            po = i.env['purchase.order'].create({'partner_id': i.supplier.id,'state': 'draft','date_approve': datetime.now()})
            if po:
                i.order_id = po.id
            raw_po_line.append((0,0, {
                'product_id': i.workcenter_id.product_service_id.id,
                'fabric': i.fabric_id.name,
                'lining':'',
                'color':i.color_id.name,
                'product_qty': i.qty_producing,
            }))           
            i.show_po()
            po.update({"order_line": val})
            

    def create_po_action(self):
        self.ensure_one()
        if any(not time.date_end for time in self.time_ids.filtered(lambda t: t.user_id.id == self.env.user.id)):
            return True
        # As button_start is automatically called in the new view
        if self.state in ('done', 'cancel'):
            return True
        
        if self.product_tracking == 'serial':
            self.qty_producing = 1.0
        else:
            self.qty_producing = self.qty_remaining
        self.env['mrp.workcenter.productivity'].create(
            self._prepare_timeline_vals(self.duration, datetime.now())
        )
        if self.production_id.state != 'progress':
            self.production_id.write({
                'date_start': datetime.now(),
            })
        if self.state == 'progress':
            return True
        
        start_date = datetime.now()

        if not self.supplier:
            raise ValidationError("Please Input Supplier first!")

        vals = {
            'state': 'progress',
            'date_start': start_date,
        }
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'state': 'purchase',
            'date_approve': start_date,
        })

        if not self.workcenter_id.product_service_id:
            raise ValidationError("Product Service in this Workcenter hasn't been set")
        
        self.env['purchase.order.line'].create({
            'product_id': self.workcenter_id.product_service_id.id,
            'product_qty': self.qty_producing,
            'order_id': po.id,
        })
        vals['order_id'] = po.id
        if not self.leave_id:
            leave = self.env['resource.calendar.leaves'].create({
                'name': self.display_name,
                'calendar_id': self.workcenter_id.resource_calendar_id.id,
                'date_from': start_date,
                'date_to': start_date + relativedelta(minutes=self.duration_expected),
                'resource_id': self.workcenter_id.resource_id.id,
                'time_type': 'other'
            })
            vals['leave_id'] = leave.id
            return self.write(vals)
        else:
            if self.date_planned_start > start_date:
                vals['date_planned_start'] = start_date
            if self.date_planned_finished and self.date_planned_finished < start_date:
                vals['date_planned_finished'] = start_date
            return self.with_context(bypass_duration_calculation=True).write(vals)
