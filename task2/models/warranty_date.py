# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, datetime, date



class DiscountCustomer(models.Model):
    _inherit = 'product.template'

    date_to = fields.Date(string='Date to')
    date_from = fields.Date(string='Date from')
    product_warranty = fields.Text(string='Product Warranty', compute='change_product_warranty')
    warranty_time = fields.Text(string='Warranty Time', compute='under_warranty')
    status = fields.Char(string="Status",default='Invalid',compute='check_status', store=True)
    time_warranty = fields.Text(string='Time Warranty',default='unexpired',  compute='check_time_warranty', store=True)


    @api.constrains('date_to')
    def check_time_warranty(self):
        for rec in self:
            duration = (rec.date_to - date.today()).days
            if duration < 0:
                rec.time_warranty = "expired"
            else:
                rec.time_warranty = "unexpired"

    @api.depends('product_warranty')
    def check_status(self):
        for rec in self:
            if "PWR" not in str(rec.product_warranty):
                rec.status = "Invalid"
            else:
                rec.status = "Value"

    @api.depends('product_warranty')
    def under_warranty(self):
        for rec in self:
            if int((rec.date_to - rec.date_from).days) < 30:
                rec.warranty_time = str((rec.date_to - rec.date_from).days) + '' + 'days'
            elif int((rec.date_to - rec.date_from).days) > 30 and int((rec.date_to - rec.date_from).days) < 365 :
                cal_months = int((rec.date_to - rec.date_from).days)
                rec.warranty_time =  str(int(cal_months / 30)) + '' + 'months'
            elif int((rec.date_to - rec.date_from).days) > 365:
                cal_months = int((rec.date_to - rec.date_from).days)
                rec.warranty_time = str(int(cal_months / 365)) + '' + 'years'
            else:
                rec.warranty_time = 0

    @api.onchange('date_to', 'date_from')
    def change_product_warranty(self):
        for rec in self:
            str_date_to = str(rec.date_to)
            split_date_to = str_date_to.split("-")
            list_empty_to = []
            for date_to in split_date_to:
                list_empty_to.append(date_to)

            str_date_from = str(rec.date_from)
            split_date_from = str_date_from.split("-")
            list_empty_from = []
            for date_from in split_date_from:
                list_empty_from.append(date_from)

            try:
                list_year_to = []
                for year_to in list_empty_to[0]:
                        list_year_to.append(year_to)
                value_to = list_empty_to[2] + list_empty_to[1] + list_year_to[2] + list_year_to[3]

                list_year_from = []
                for year_from in list_empty_from[0]:
                    list_year_from.append(year_from)
                value_from = list_empty_from[2] + list_empty_from[1] + list_year_from[2] + list_year_from[3]

                if int((rec.date_to - rec.date_from).total_seconds()) < 0:
                    rec.product_warranty = "False"
                else:
                    rec.product_warranty = "PWR" + "/" + value_from + "/" + value_to
            except:
                continue

class UpdateWarranry(models.TransientModel):

    _name = 'update.warranty'

    date_from_update = fields.Date(string='Date From Update')
    date_to_update = fields.Date(string='Date To Update')

    def update(self):
        list = self.env['product.template'].browse(self._context['active_ids'])
        for rec in list:
            rec.date_to = self.date_to_update
            rec.date_from = self.date_from_update



