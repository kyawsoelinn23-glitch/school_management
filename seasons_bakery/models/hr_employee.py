from odoo import api, fields, models



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    branch_ids = fields.Many2many('seasons.branch',string='Branches')