# -*- coding: utf-8 -*-
# from odoo import http


# class MidoceanConnector(http.Controller):
#     @http.route('/midocean_connector/midocean_connector', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/midocean_connector/midocean_connector/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('midocean_connector.listing', {
#             'root': '/midocean_connector/midocean_connector',
#             'objects': http.request.env['midocean_connector.midocean_connector'].search([]),
#         })

#     @http.route('/midocean_connector/midocean_connector/objects/<model("midocean_connector.midocean_connector"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('midocean_connector.object', {
#             'object': obj
#         })
