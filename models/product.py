import logging
import requests
import base64

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductExtend(models.Model):
    _inherit = "product.template"

    hidden_reference_code = fields.Char("Internal hidden references code")

    def fetch_product_from_midocean(self):

        # Utility function
        def batch(iterable, n=1):
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]

        # Load env
        ProductTemplate = self.env['product.template']
        ProductProduct = self.env['product.product']
        ProductAttribute = self.env['product.attribute']
        ProductAttributeValue = self.env['product.attribute.value']
        ProductTemplateAttributeLine = self.env['product.template.attribute.line']
        ProductCategory = self.env['product.category']

        # Get the Midocean API Key
        x_gateway_apikey = self.env.user.company_id.x_gateway_apikey or False

        if x_gateway_apikey:

            # Fetch data
            result = requests.get(
                "https://api.midocean.com/gateway/products/2.0?language=fr",
                headers={"x-Gateway-APIKey": x_gateway_apikey}
            )

            all_products = result.json()

            # Number of product to process at once
            batchsize = 10

            # Iterable over product in batch size
            for products in batch(all_products, batchsize):

                # Itterate on the product on this batch
                for product in products:

                    # Test if the product already exists
                    if ProductTemplate.search_count([("name", "=", product['short_description'])]) == 0:

                        # Create product template
                        product_template = ProductTemplate.create({
                            "name": product['short_description'],
                            "description": product['long_description'] if product.get("long_description") is not None else "",
                            "weight": product['net_weight'],
                            "volume": product['volume'],
                            "type": "product",
                            "default_code": product['master_code']
                        })

                        category_level1 = None
                        category_level2 = None
                        category_level3 = None

                        # If the product has only one variant, use that variant as product template
                        if len(product['variants']) == 1:
                            variant = product['variants'][0]

                            # Create product category
                            if ProductCategory.search_count([("name", "=", variant['category_level1'])]) == 0:
                                category_level1 = ProductCategory.create({
                                    "name": variant['category_level1'],
                                })
                            else:
                                category_level1 = ProductCategory.search(
                                    [("name", "=", variant['category_level1'])])

                            if variant.get("category_level2") is not None and ProductCategory.search_count([("name", "=", variant['category_level2'])]) == 0:
                                category_level2 = ProductCategory.create({
                                    "name": variant['category_level2'],
                                    "parent_id": category_level1.id
                                })
                            elif variant.get("category_level2") is not None and ProductCategory.search_count([("name", "=", variant['category_level2'])]) > 0:
                                category_level2 = ProductCategory.search(
                                    [("name", "=", variant['category_level2'])])

                            if variant.get("category_level3") is not None and ProductCategory.search_count([("name", "=", variant['category_level3'])]) == 0:
                                category_level3 = ProductCategory.create({
                                    "name": variant['category_level3'],
                                    "parent_id": category_level2.id
                                })
                            elif variant.get("category_level3") is not None and ProductCategory.search_count([("name", "=", variant['category_level3'])]) > 0:
                                category_level3 = ProductCategory.search(
                                    [("name", "=", variant['category_level3'])])

                            image_1920 = None
                            image_1024 = None

                            if len(variant['digital_assets']) > 1:
                                image_1920 = base64.b64encode(requests.get(
                                    variant['digital_assets'][0]['url']).content)
                                image_1024 = base64.b64encode(requests.get(
                                    variant['digital_assets'][1]['url']).content)
                            else:
                                image_1920, image_1024 = base64.b64encode(requests.get(
                                    variant['digital_assets'][0]['url']).content)

                            # Check if category has been created
                            if category_level3 is not None:
                                product_template.write({
                                    "image_1920": image_1920,
                                    "image_1024": image_1024,
                                    "hidden_reference_code": variant['sku'],
                                    "categ_id": category_level3.id
                                })
                            elif category_level3 is None and category_level2 is not None:
                                product_template.write({
                                    "image_1920": image_1920,
                                    "image_1024": image_1024,
                                    "hidden_reference_code": variant['sku'],
                                    "categ_id": category_level2.id
                                })

                            elif category_level3 is None and category_level2 is None and category_level1 is not None:
                                product_template.write({
                                    "image_1920": image_1920,
                                    "image_1024": image_1024,
                                    "hidden_reference_code": variant['sku'],
                                    "categ_id": category_level1.id
                                })

                        elif len(product['variants']) > 1:
                            first_variant = product['variants'][0]

                            # Create product category
                            if ProductCategory.search_count([("name", "=", first_variant['category_level1'])]) == 0:
                                category_level1 = ProductCategory.create({
                                    "name": first_variant['category_level1'],
                                })
                            else:
                                category_level1 = ProductCategory.search(
                                    [("name", "=", first_variant['category_level1'])])

                            if first_variant.get("category_level2") is not None and ProductCategory.search_count([("name", "=", first_variant['category_level2'])]) == 0:
                                category_level2 = ProductCategory.create({
                                    "name": first_variant['category_level2'],
                                    "parent_id": category_level1.id
                                })
                            elif first_variant.get("category_level2") is not None and ProductCategory.search_count([("name", "=", first_variant['category_level2'])]) > 0:
                                category_level2 = ProductCategory.search(
                                    [("name", "=", first_variant['category_level2'])])

                            if first_variant.get("category_level3") is not None and ProductCategory.search_count([("name", "=", first_variant['category_level3'])]) == 0:
                                category_level3 = ProductCategory.create({
                                    "name": first_variant['category_level3'],
                                    "parent_id": category_level2.id
                                })
                            elif first_variant.get("category_level3") is not None and ProductCategory.search_count([("name", "=", first_variant['category_level3'])]) > 0:
                                category_level3 = ProductCategory.search(
                                    [("name", "=", first_variant['category_level3'])])

                            # Check if category has been created
                            if category_level3 is not None:
                                product_template.write({
                                    "categ_id": category_level3.id
                                })
                            elif category_level3 is None and category_level2 is not None:
                                product_template.write({
                                    "categ_id": category_level2.id
                                })
                            elif category_level3 is None and category_level2 is None and category_level1 is not None:
                                product_template.write({
                                    "categ_id": category_level1.id
                                })

                            for variant in product['variants']:

                                # Variant attributes
                                product_attribute = None
                                product_attribute_value = None
                                product_attribute_line = None

                                # Create product caracteristique if not exist
                                # Those caracteristiques are used later for product variant
                                if variant.get('color_group') is not None:
                                    color = variant.get('color_group')
                                    product_attribute = ProductAttribute.search(
                                        [('name', '=', 'Color')], limit=1)

                                    if len(product_attribute) >= 1:
                                        product_attribute_value = ProductAttributeValue.search(
                                            [('attribute_id', '=', product_attribute.id), ('name', '=', color)], limit=1)

                                        if len(product_attribute_value) == 0:
                                            product_attribute_value = ProductAttributeValue.create({
                                                "attribute_id": product_attribute.id,
                                                "name": color
                                            })

                                    else:
                                        product_attribute = ProductAttribute.create({
                                            "name": "Color",
                                        })

                                        product_attribute_value = ProductAttributeValue.create({
                                            "attribute_id": product_attribute.id,
                                            "name": color
                                        })

                                # Adding variant to product template
                                if ProductTemplateAttributeLine.search_count(['&', ("attribute_id", "=", product_attribute.id), ("product_tmpl_id", "=", product_template.id)]) == 0:
                                    product_attribute_line = ProductTemplateAttributeLine.create({
                                        "attribute_id": product_attribute.id,
                                        "value_ids": [(4, product_attribute_value.id)],
                                        "product_tmpl_id": product_template.id
                                    })
                                else:
                                    product_attribute_line = ProductTemplateAttributeLine.search(
                                        ['&', ("attribute_id", "=", product_attribute.id), ("product_tmpl_id", "=", product_template.id)], limit=1)

                                    if len(product_attribute_line) == 1:
                                        product_attribute_line.write({
                                            "attribute_id": product_attribute.id,
                                            "value_ids": [(4, product_attribute_value.id)],
                                            "product_tmpl_id": product_template.id
                                        })

                                # Update product.product variant
                                for product in product_template.product_variant_ids:

                                    colors = [
                                        att.name for att in product.product_template_attribute_value_ids]

                                    # Check if the current product is the current variant
                                    if variant.get('color_group') is not None and variant.get('color_group') in colors:
                                        image_variant_1920 = base64.b64encode(requests.get(
                                            variant['digital_assets'][0]['url']).content)

                                        image_variant_1024 = base64.b64encode(requests.get(variant['digital_assets'][1]['url']).content) if len(
                                            variant['digital_assets']) > 1 else base64.b64encode(requests.get(variant['digital_assets'][0]['url']).content)

                                        product.write({
                                            "default_code": variant['sku'],
                                            "hidden_reference_code": variant['sku'],
                                            "image_1920": image_variant_1920,
                                            "image_1024": image_variant_1024,
                                        })

                # Commit the product process in this batch
                self.env.cr.commit()

    def fetch_product_price_from_midocean(self):
        ProductTemplate = self.env['product.template']
        ProductProduct = self.env['product.product']

        # Get the Midocean API Key
        x_gateway_apikey = self.env.user.company_id.x_gateway_apikey or False

        products_price_factor = self.env.user.company_id.products_price_factor or False

        if x_gateway_apikey:

            # Fetch data
            result = requests.get(
                "https://api.midocean.com/gateway/pricelist/2.0/",
                headers={"x-Gateway-APIKey": x_gateway_apikey}
            )

            all_prices = result.json()['price']

            # Number of product to process at once
            batchsize = 10

            # Iterable over product in batch size
            for i in range(0, len(all_prices), batchsize):
                prices_batch = all_prices[i:i+batchsize]

                for price in prices_batch:
                    if ProductTemplate.search_count([('hidden_reference_code', '=', price['sku'])]) == 1:
                        product = ProductTemplate.search(
                            [('hidden_reference_code', '=', price['sku'])])

                        final_price = float(price['price'].replace(',', '.', 1))*float(
                            products_price_factor) if products_price_factor is not False else float(price['price'].replace(',', '.', 1))

                        product.write({
                            "list_price": final_price
                        })

                self.env.cr.commit()
