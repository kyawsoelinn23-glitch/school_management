from odoo import models, fields


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Author Name',required=True)
    email = fields.Char(string='Email')
    description = fields.Text(string='Description')