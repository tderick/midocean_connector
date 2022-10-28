import logging
import requests
import base64


from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductCron(models.Model):
    _inherit = "product.product"

    def fetch_product_from_midocean(self):
        Product = self.env['product.product']
        Category = self.env['product.category']

        # Fetch data
        result = requests.get("https://fakestoreapi.com/products")

        for product in result.json():

            # Test if the product already exists
            if Product.search_count([("name", "like", product['title'])]) == 0:
                # Test if the category of the product already exists
                if Category.search_count([('name', 'like', product['category'])]) >= 1:
                    category_id = Category.search(
                        [("name", "like", product['category'])])[0].id
                else:
                    # Create the category if not exist
                    category_id = Category.create(
                        {"name": product['category']}).id

                image_1920 = base64.b64encode(
                    requests.get(product['image']).content)

                Product.create({
                    "name": product['title'],
                    "description": product['description'],
                    "price": product['price'],
                    "categ_id": category_id,
                    "image_1920": image_1920
                })
