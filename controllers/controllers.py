# -*- coding: utf-8 -*-
from odoo import http

# class AutoWord(http.Controller):
#     @http.route('/auto_word/auto_word/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auto_word/auto_word/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('auto_word.listing', {
#             'root': '/auto_word/auto_word',
#             'objects': http.request.env['auto_word.auto_word'].search([]),
#         })

#     @http.route('/auto_word/auto_word/objects/<model("auto_word.auto_word"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auto_word.object', {
#             'object': obj
#         })