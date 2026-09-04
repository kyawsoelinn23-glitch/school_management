from odoo import fields, models, _
from datetime import timedelta
from io import BytesIO
import base64

import xlsxwriter


from odoo.exceptions import ValidationError


class StudentReportWizard(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    student_id = fields.Many2one('school.student', string='Student')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    report_file = fields.Binary(
        string='Report File', readonly=True, attachment=True
    )
    report_filename = fields.Char(
        string='Report Filename', readonly=True
    )

    def action_print_excel(self):
        self.ensure_one()

        if self.start_date > self.end_date:
            raise ValidationError(
                _('Start Date must be before or equal to End Date.')
            )

        Student = self.env['school.student']

        # The supplied wizard does not identify a report-specific date field
        # on school.student, so create_date is used for the date-range filter.
        domain = []
        if 'create_date' in Student._fields:
            start_dt = fields.Datetime.to_datetime(self.start_date)
            end_dt = fields.Datetime.to_datetime(self.end_date) + timedelta(days=1)
            domain += [
                ('create_date', '>=', start_dt),
                ('create_date', '<', end_dt),
            ]

        if self.student_id:
            domain.append(('id', '=', self.student_id.id))

        students = Student.search(domain, order='id')

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        title_fmt = workbook.add_format({
            'bold': True, 'font_size': 16,
            'align': 'center', 'valign': 'vcenter',
        })
        label_fmt = workbook.add_format({'bold': True, 'border': 1})
        value_fmt = workbook.add_format({'border': 1})
        header_fmt = workbook.add_format({
            'bold': True, 'bg_color': '#D9EAF7', 'border': 1,
            'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        })
        cell_fmt = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        date_fmt = workbook.add_format({
            'border': 1, 'num_format': 'dd/mm/yyyy', 'valign': 'top',
        })
        datetime_fmt = workbook.add_format({
            'border': 1, 'num_format': 'dd/mm/yyyy hh:mm:ss', 'valign': 'top',
        })

        sheet = workbook.add_worksheet('Student Report')
        sheet.freeze_panes(6, 0)
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

        title_fmt = workbook.add_format({
            'bold': True, 'font_size': 16,
            'align': 'center', 'valign': 'vcenter', 'border': 1,
        })
        sheet.merge_range('A1:G1', 'Student Report', title_fmt)

        sheet.write('A3', 'Student', label_fmt)
        sheet.merge_range(
            'B3:D3',
            self.student_id.display_name if self.student_id else 'All Students',
            workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
        )

        sheet.write('A4', 'Start Date', label_fmt)
        sheet.write_datetime('B4', fields.Datetime.to_datetime(self.start_date), date_fmt)
        sheet.write('C4', 'End Date', label_fmt)
        sheet.write_datetime('D4', fields.Datetime.to_datetime(self.end_date), date_fmt)

        # works even if some fields are custom fields in the module.
        requested_columns = [
            ('name', 'Student Name'),
            ('student_id', 'Student ID'),
            ('class_id', 'Class'),
            ('gender', 'Gender'),
            ('phone', 'Phone'),
            ('email', 'Email'),
        ]
        # If the module uses alternative common field names, map them here.
        aliases = {
            'student_id': ['student_code', 'student_number', 'code', 'roll_no'],
            'class_id': ['class', 'class_name', 'standard_id'],
            'phone': ['mobile', 'phone_number'],
            'email': ['email_address'],
        }

        resolved_columns = []
        for requested_name, label in requested_columns:
            # Exact field name
            field_name = requested_name
            # If not found, search aliases
            if field_name not in Student._fields:
                for alias in aliases.get(requested_name, []):
                    if alias in Student._fields:
                        field_name = alias
                        break
            # Keep the original requested order
            if field_name in Student._fields:
                resolved_columns.append((field_name, label))

        columns = resolved_columns

        header_row = 5
        sheet.write(header_row, 0, 'No', header_fmt)
        for col, (field_name, label) in enumerate(columns, start=1):
            sheet.write(header_row, col, label, header_fmt)

        def get_value(record, field_name):
            field = Student._fields[field_name]
            value = record[field_name]
            if not value:
                return ''

            if field.type in ('many2one', 'many2many', 'one2many'):
                return ', '.join(value.mapped('display_name'))
            if field.type == 'boolean':
                return 'Yes' if value else 'No'
            if field.type == 'selection':
                selection = field.selection
                if callable(selection):
                    selection = selection(record.env)
                return dict(selection or []).get(value, value)

            return value

        for row_no, record in enumerate(students, start=1):
            row_idx = header_row + row_no
            # No Column
            sheet.write(row_idx, 0, row_no, cell_fmt)
            for col_idx, (field_name, label) in enumerate(columns, start=1):
                value = get_value(record, field_name)

                field = Student._fields[field_name]
                if field.type == 'datetime' and value:
                    sheet.write_datetime(
                        row_idx, col_idx,
                        fields.Datetime.to_datetime(value),
                        datetime_fmt,
                    )
                elif field.type == 'date' and value:
                    sheet.write_datetime(
                        row_idx, col_idx,
                        fields.Date.to_date(value),
                        date_fmt,
                    )
                else:
                    sheet.write(row_idx, col_idx, value, cell_fmt)

        widths = {
            'Student Name': 25,
            'Student ID': 25,
            'Class': 18,
            'Gender': 12,
            'Phone': 18,
            'Email': 30,
        }
        # No column width
        sheet.set_column(0, 0, 10)
        for col_idx, (field_name, label) in enumerate(columns, start=1):
            sheet.set_column(
                col_idx,
                col_idx,
                widths.get(label, 18)
            )

        if columns:
            sheet.autofilter(
                header_row, 0,
                header_row + len(students),
                len(columns),
            )

        workbook.close()
        output.seek(0)

        start_date = fields.Date.to_date(self.start_date)
        end_date = fields.Date.to_date(self.end_date)
        filename = 'student_report_%s_to_%s.xlsx' % (
            start_date.strftime('%d-%m-%Y'),
            end_date.strftime('%d-%m-%Y'),
        )

        self.write({
            'report_file': base64.b64encode(output.read()),
            'report_filename': filename,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': (
                       '/web/content?model=student.report.wizard'
                       '&id=%s'
                       '&field=report_file'
                       '&filename_field=report_filename'
                       '&download=true'
                   ) % self.id,
            'target': 'self',
        }
