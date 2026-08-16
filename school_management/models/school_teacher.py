from odoo import _, api, fields, models


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'School Teacher'

    name = fields.Char(string="Teacher Name", required=True)
    employee_id = fields.Char(string="Employee ID", readonly=True, default=lambda self: _("New"))
    phone = fields.Char(string="Phone Number", required=True)
    email = fields.Char(string="Email Address", required=True)
    date_joined = fields.Date(string="Date Joined")
    subject_id = fields.Many2one('school.subject', string='Subjects')
    active = fields.Boolean(string="Active", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["employee_id"] = self.env["ir.sequence"].next_by_code("school.teacher")
        return super().create(vals_list)
