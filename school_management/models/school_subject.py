from odoo import api, fields, models

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'School Subject'

    name = fields.Char(string='Subject Name',required=True)
    code = fields.Char(string='Subject Code')
    description = fields.Text(string='Description')