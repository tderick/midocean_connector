# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    """
        We have to inherit the res.company model in order to add our custom configuration fields to the model.        
        When you open a configuration menu in Odoo then Odoo will automatically look in the table res.company        
        for the values set there. By default all configurations are company wide in Odoo.        
        Have a look at res_config_settings.py where you can see that all fields are related to this model to get/set        
        those values on the company.    
    """
    x_gateway_apikey = fields.Char(string='x-Gateway-APIKey')

    products_price_factor = fields.Float(
        string='Coefficient de multiplication des prix')
