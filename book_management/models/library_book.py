from odoo import models, fields

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    book_name = fields.Char(string="Book Name",required=True)
    isbn = fields.Char(string="ISBN",required=True)
    author = fields.Char(string="Author",required=True)
    published_date = fields.Date(string="Published Date",required=True)
    price = fields.Float(string="Price",required=True)
    available_copies = fields.Integer(string="Available Copies",required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active",default=True)

    category_id = fields.Many2one('library.book.category', string='Category', required=True)
    author_ids = fields.Many2many('library.author',string='Authors')

    book_code = fields.Char(string='Book Code',readonly=True)

    def action_generate_book_code(self):
        for record in self:
            if not record.book_code:
                record.book_code = self.env[
                    'ir.sequence'
                ].next_by_code(
                    'library.book'
            ) or 'New'


