from odoo import _, api, fields, models


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Student Information"

    name = fields.Char(string="Student Name", required=True)
    student_id = fields.Char(
        string="Student ID", readonly=True, default=lambda self: _("New"), copy=False,
    )

    class_id = fields.Many2one("school.class", string="Class")
    subject_ids = fields.Many2many("school.subject", string="Subjects")

    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")

    date_of_birth = fields.Date(string="Date of Birth")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email Address")
    address = fields.Text(string="Address")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["student_id"] = self.env["ir.sequence"].next_by_code("school.student")
        return super().create(vals_list)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals["student_id"] = self.env["ir.sequence"].next_by_code("school.student")
    #     res = super().create(vals_list)
    #     return res
