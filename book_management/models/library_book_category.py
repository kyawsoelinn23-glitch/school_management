from odoo import models, fields


class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'

    name = fields.Char(string='Category Name',required=True)
    code = fields.Char(string='Category Code',required=True)
    shelf_location = fields.Char(string='Shelf Location')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active',default=True)