from odoo import http
from odoo.http import request


class AutoLogin(http.Controller):

    @http.route('/autologin', auth='public', type='http')
    def auto_login(self, **kw):

        credential = {
            'login': 'demo',
            'password': 'demo123',
            'type': 'password',
        }

        request.session.authenticate(
            request.env,
            credential
        )

        return request.redirect('/web')
