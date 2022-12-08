# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    x_gateway_apikey = fields.Char(
        related='company_id.x_gateway_apikey', string='x-Gateway-APIKey', readonly=False)

    products_price_factor = fields.Float(
        related='company_id.products_price_factor', string='Coefficient de multiplication des prix', readonly=False)
