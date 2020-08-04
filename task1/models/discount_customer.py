# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re


class DiscountCustomer(models.Model):
    _inherit = 'res.partner'

    discount_code = fields.Char(string='Discount Code')
    status = fields.Char(string="Status",default='Invalid', compute='check_discount_code', store=True)

    @api.depends('discount_code')
    def check_discount_code(self):
        for rec in self:
            if not rec.discount_code:
                rec.status = "Invalid"
            else:
                if (re.match("^VIP_([1-9]|[1-9][0-9]|0[1-9])$", rec.discount_code)):
                    rec.status = "Valid code"
                else:
                    rec.status = "Invalid code"

class DiscountTotal(models.Model):
    _inherit = 'sale.order'

    discount_code = fields.Char(string='Discount', related='partner_id.discount_code', store=True, readonly=True)
    discount_percent = fields.Integer(string='Discount(%)', readonly=True, compute='discount_count')
    valid_code = fields.Char(string='Value Code', related='partner_id.status',readonly=True, store=True)
    final_total = fields.Char(string='Final Total', readonly=True, compute='findtotal')

    @api.depends('valid_code')
    def discount_count(self):
        for rec in self:
            if rec.valid_code == 'Valid code':
                rec.discount_percent = rec.discount_code.split('_')[1]
            else:
                rec.discount_percent = 0

    @api.depends('amount_total', 'discount_percent')
    def findtotal(self):
        for rec in self:
            percent = int(rec.discount_percent) / 100
            rec.final_total = rec.amount_total - (percent * rec.amount_total)

class UpdateDiscountCode(models.TransientModel):

    _name = 'update.discount.code'

    update_discount_code = fields.Text(string='Update Discount Code')

    def update(self):
        list = self.env['res.partner'].browse(self._context['active_ids'])
        for rec in list:
            rec.discount_code = self.update_discount_code













