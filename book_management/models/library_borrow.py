from odoo import api, models, fields


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow'

    name = fields.Char(string='Reference',required=True,copy=False,default='New')
    member_id = fields.Many2one('res.partner',string='Member',required=True)
    book_id = fields.Many2one('library.book',string='Book',required=True)
    borrow_date = fields.Date(string='Borrow Date',required=True)
    due_date = fields.Date(string='Due Date',required=True)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
        ],string='Status',default='draft')
    active = fields.Boolean(default=True)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env[
                    'ir.sequence'
                ].next_by_code('library.borrow') or 'New'
        return super().create(vals_list)

    def action_print_receipt(self):
        return self.env.ref(
            'book_management.action_report_library_borrow'
        ).report_action(self)