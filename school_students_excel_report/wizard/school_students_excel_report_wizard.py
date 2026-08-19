from odoo import api, fields, models, _

class StudentReportWizard(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    student_id = fields.Many2one('school.student',string='Student')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    report_file = fields.Binary(string='Report File', readonly=True, attachment=True)
    report_filename = fields.Char(string='Report Filename', readonly=True)

    def action_print_excel(self):
        return True