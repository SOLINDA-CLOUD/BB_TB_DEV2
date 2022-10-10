# -*- coding: utf-8 -*-

from odoo import _, models, fields, api

class PatternAlteration(models.Model):
    _name = 'pattern.alteration'
    _description = 'Link Purchase Request and Pattern Alteration'

    parent_purchase_id = fields.Many2one('purchase.request', string='Request')
    pattern_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    user_id = fields.Many2one('res.users', string='User Pattern Alteration')

class CustomPattern(models.Model):
    _name = 'custom.pattern'
    _description = 'Custom Pattern'

    # name = fields.Char('Print/Color')
    parent_custom_id = fields.Many2one('purchase.request', string='custom')
    print_color_id = fields.Many2one('product.template.attribute.value', string='Print/Color')
    model_ptr = fields.Many2one('product.category', string='Model')
    size = fields.Many2one('product.template.attribute.value', string='Size')
    pattern_marker = fields.Char('Pattern Marker')
    size_approve = fields.Char('Size Approve')
    fabric = fields.Many2one(comodel_name='data.fabric.lining', string='Fabric')

class FabricLining(models.Model):
    _name = 'fabric.lining'
    _description = 'Fabric Lining'

    fabric_lining_id = fields.Many2one('purchase.request', string='fabric lining ids')
    fabric = fields.Many2one(comodel_name='data.fabric.lining', string='Fabric')
    lining = fields.Many2one(comodel_name='data.fabric.lining', string='Lining')
    color = fields.Many2one(comodel_name='print.color', string='Color')

class LabelHardware(models.Model):
    _name = 'label.hardware'
    _description = 'Label Hardware'

    label_hardware_id = fields.Many2one('purchase.request', string='label hardware ids')
    description = fields.Char('Description')
    color = fields.Many2one(comodel_name='print.color', string='Color')
    qty_label = fields.Float('Qty')

class LabelDress(models.Model):
    _name = 'label.dress'
    _description = 'Label Dress'

    label_dress_id = fields.Many2one('purchase.request', string='label dress ids')
    brand = fields.Many2one('product.brand', string='Brand', ondelete='cascade')
    image = fields.Image('Label Pict')
    comment = fields.Html('Comment')

class ProductionSummary(models.Model):
    _name = 'production.summary'
    _description = 'Production Summary'

    prod_summ_id = fields.Many2one('purchase.request', string='prod summ ids')
    summary = fields.Char('Summary')
    description = fields.Char('Description')

class RequestDetail(models.Model):
    _name = 'request.detail'
    _description = 'Request Detail'

    name = fields.Char(string='Original Sample')
    sample_size = fields.Char(string='Sample Size')
    approved_size = fields.Char(string='Sample In Approved Size')
    sample_in_size = fields.Char(string='Please Make Sample In Size')

class DataFabricLining(models.Model):
    _name = 'data.fabric.lining'
    _description = 'Database Fabric and Lining'

    name = fields.Char(string='fabric and lining')

class PrintColor(models.Model):
    _name = 'print.color'
    _description = 'Print Color'

    name = fields.Char(string='color')

class DataMasterStory(models.Model):
    _name = 'data.master.story'
    _description = 'Data Master Story'

    name = fields.Char('Story Name')

class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    image = fields.Image(string='Fabric Swatch')
    department = fields.Many2one('product.category', string='Department')
    sub_department = fields.Char(string='Sub Department')
    fabric = fields.Many2one(comodel_name='data.fabric.lining', string='Fabric', ondelete='cascade')
    lining= fields.Many2one(comodel_name='data.fabric.lining', string='Lining', ondelete='cascade')
    view_story = fields.Many2one(string='Story', related='request_id.story_id', readonly=True)

    @api.onchange('product_id')
    def _onchange_image(self):
        if self.product_id:
            self.image = ''
            if self.product_id.image_1920:
                self.image = self.product_id.image_1920
            self.image = self.image
    
    @api.onchange('product_id')
    def _onchange_department(self):
        if self.product_id:
            department = ''
            if self.product_id.categ_id:
                self.department = self.product_id.categ_id
            return department

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    ### SAMPLE DEVELOPMENT ###
    request_detail_id = fields.Many2one(string='Original Sample', comodel_name='request.detail', ondelete='cascade')
    notes = fields.Html(string='Notes')
    date_start = fields.Date(string='Transaction Date')
    story_id = fields.Many2one(string='Story', comodel_name='data.master.story')
    alt_cmnt = fields.Html('Alteration Comment')

    ### PATTERN ALTERATION ###
    purchase_custom_ids = fields.One2many('custom.pattern', 'parent_custom_id', string='Custom', copy=True)
    purchase_pattern_ids = fields.One2many('pattern.alteration', 'parent_purchase_id', string='Order History')
    revision_id = fields.Many2one('purchase.request', string='Purchase to Pattern Alteration')
    purchase_revision_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    pattern_count = fields.Integer(string='Pattern', compute='_find_len')
    test = fields.Boolean(string="Test", default=False)

    ### PENDING ORDER ###
    status_of_sample = fields.Char(string='Status of Sample')
    ordering_date = fields.Date(string='Delivery Date', states={'done': [('readonly', False)]})
    delivery_date = fields.Date(states={'done': [('readonly', False)]})
    thread_type = fields.Char(string='Thread Type')
    thread_color = fields.Char(string='Thread Color')
    hanging_tape = fields.Char(string='Hanging Tape')

    seams = fields.Html(string='Seams')
    grading_intructions = fields.Html(string='Grading Intructions')
    fit_changes = fields.Html(string='Fit Changes')

    fabric_lining_ids = fields.One2many('fabric.lining', 'fabric_lining_id', string='fabric lining id')
    label_hardware_ids = fields.One2many('label.hardware', 'label_hardware_id', string='label hardware id')
    label_dress_ids = fields.One2many('label.dress', 'label_dress_id', string='label dress id')
    prod_summ_ids = fields.One2many('production.summary', 'prod_summ_id', string='prod summ id')

    def button_to_pattern(self):
        return self.write({'state':'rejected'})

    @api.model
    def create(self, vals):
        res = super(PurchaseRequest, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("purchase.request.seq")
        return res

    def _find_len(self):
        self.pattern_count = len(self.purchase_pattern_ids.ids)

    def create_pattern_alteration(self):
        pattern = self.copy()
        uid_id = self.env.user.id
        self.env['pattern.alteration'].create({
            'pattern_id': pattern.id,
            'user_id': uid_id,
            'parent_purchase_id': self.ids[0],
        })
        pattern.name = self.name + ' - PTR ' + str(len(self.purchase_pattern_ids.ids))
        pattern.test = True
        self.env['custom.pattern'].create({
            'parent_custom_id': self.ids[0],
        })
        return {
            "name": _("Pattern Alteration"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.request",
            "views": [
                (self.env.ref("purchase_request.view_purchase_request_form").id, "form"),
            ],
            "target": "current",
            "res_id": pattern.id,
        }
        
    def view_pattern_alteration(self):
        action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
        purchase_pattern_ids = self.mapped('purchase_pattern_ids.pattern_id')
        if len(purchase_pattern_ids) > 1: 
            action['domain'] = [('id', 'in', purchase_pattern_ids.ids)]
        elif purchase_pattern_ids:
            action['views'] = [
                (self.env.ref('purchase_request.view_purchase_request_form').id, 'form')
            ]
            action['res_id'] = purchase_pattern_ids.id
        return action


    
