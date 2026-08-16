from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Is Student')
    student_code = fields.Char(string='Student Code')
    enrollment_date = fields.Date(string='Enrollment Date')
