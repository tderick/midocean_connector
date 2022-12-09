import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductProductExtend(models.Model):
    _inherit = "product.product"

    lst_price = fields.Float(readonly=True, compute="_compute_lst_price")

    def _compute_lst_price(self):
        products_price_factor = float(
            self.env.user.company_id.products_price_factor)

        for product in self:
            product.lst_price = product.standard_price*products_price_factor
