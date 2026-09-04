from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean(string='Is Library Member')
    member_code = fields.Char(string='Member Code')
    membership_date = fields.Date(string='Membership Date')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_library_member') and not vals.get('member_code'):
                vals['member_code'] = self.env['ir.sequence'].next_by_code(
                    'library.member'
                )
        return super().create(vals_list)