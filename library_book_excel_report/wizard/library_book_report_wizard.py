from odoo import fields, models, _
from io import BytesIO
import base64

import xlsxwriter


class LibraryBookReportWizard(models.TransientModel):
    _name = 'library.book.report.wizard'
    _description = 'Library Book Report Wizard'

    category_id = fields.Many2one('library.book.category',string='Category')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    report_file = fields.Binary(string='Report File',readonly=True,attachment=True)

    report_filename = fields.Char(string='File Name',readonly=True)

    def action_print_excel(self):
        self.ensure_one()
        domain = []
        if self.category_id:
            domain.append(
                ('category_id', '=', self.category_id.id)
            )
        if self.from_date:
            domain.append(
                ('create_date', '>=', self.from_date)
            )

        if self.to_date:
            domain.append(
                ('create_date', '<=', self.to_date)
            )

        books = self.env['library.book'].search(domain)

        output = BytesIO()

        workbook = xlsxwriter.Workbook(
            output,
            {'in_memory': True}
        )

        sheet = workbook.add_worksheet(
            'Library Books'
        )

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'border': 1,
        })

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'bg_color': '#D9EAD3',
            'align': 'center',
        })

        cell_format = workbook.add_format({
            'border': 1,
        })

        sheet.merge_range(
            'A1:F1',
            'Library Book Report',
            title_format
        )

        headers = [
            'Book Code',
            'Book Name',
            'Category',
            'Author',
            'Price',
            'Available Copies'
        ]

        row = 2

        for col, header in enumerate(headers):
            sheet.write(
                row,
                col,
                header,
                header_format
            )

        row += 1

        for book in books:

            authors = ', '.join(
                book.author_ids.mapped('name')
            )

            sheet.write(
                row, 0,
                book.book_code or '',
                cell_format
            )

            sheet.write(
                row, 1,
                book.book_name or '',
                cell_format
            )

            sheet.write(
                row, 2,
                book.category_id.name or '',
                cell_format
            )

            sheet.write(
                row, 3,
                authors,
                cell_format
            )

            sheet.write(
                row, 4,
                book.price,
                cell_format
            )

            sheet.write(
                row, 5,
                book.available_copies,
                cell_format
            )

            row += 1

        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 50)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 20)

        workbook.close()

        output.seek(0)

        filename = 'library_book_report.xlsx'

        self.write({
            'report_file': base64.b64encode(
                output.read()
            ),
            'report_filename': filename,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': (
                '/web/content?model=library.book.report.wizard'
                '&id=%s'
                '&field=report_file'
                '&filename_field=report_filename'
                '&download=true'
            ) % self.id,
            'target': 'self',
        }