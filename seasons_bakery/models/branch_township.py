from odoo import api, fields, models

class BranchTownship(models.Model):
    _name = 'branch.township'
    _description = 'Branch Township'

    name = fields.Char(string='Township', required=True)
    branch_ids = fields.One2many('seasons.branch', 'township_id', string='Branches')