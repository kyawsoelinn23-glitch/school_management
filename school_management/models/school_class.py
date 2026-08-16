from odoo import fields, models


class SchoolClass(models.Model):
    _name = "school.class"
    _description = "School Class"

    name = fields.Char(string="Class Name", required=True)
    code = fields.Char(string="Class Code")
    academic_year = fields.Char(string="Academic Year")
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals["code"] = self.env["ir.sequence"].next_by_code("school.class")
    #     return super().create(vals_list)
