from odoo import fields, models


class SeasonsBranch(models.Model):
    _name = 'seasons.branch'
    _description = 'Seasons Branch'

    name = fields.Char(string='Branch Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    opening_hours = fields.Char(string='Opening Hours')

    region_id = fields.Many2one('branch.region', string='Region')
    township_id = fields.Many2one('branch.township', string='Township')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
