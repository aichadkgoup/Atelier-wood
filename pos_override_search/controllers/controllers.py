# -*- coding: utf-8 -*-
# from odoo import http


# class PosOverrideSearch(http.Controller):
#     @http.route('/pos_override_search/pos_override_search/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_override_search/pos_override_search/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_override_search.listing', {
#             'root': '/pos_override_search/pos_override_search',
#             'objects': http.request.env['pos_override_search.pos_override_search'].search([]),
#         })

#     @http.route('/pos_override_search/pos_override_search/objects/<model("pos_override_search.pos_override_search"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_override_search.object', {
#             'object': obj
#         })
