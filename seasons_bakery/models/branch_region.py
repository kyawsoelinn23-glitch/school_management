from odoo import fields, models


class BranchRegion(models.Model):
    _name = 'branch.region'
    _description = 'Branch Region'

    name = fields.Char(string='Region', required=True)
    branch_ids = fields.One2many("seasons.branch", "region_id", string='Branches')
