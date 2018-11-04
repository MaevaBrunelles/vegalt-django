""" Script to get data from OpenFoodFacts API and register them in a database """

import requests

from django.core.management.base import BaseCommand
from ._db_interact import DbInteract


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Get products informations from OpenFoodFacts
        and insert them in a database.
        """

        # pylint: disable=line-too-long

        products_categories = [
            {
                "name": "Steaks hachés",
                "alternative": False,
            },
            {
                "name": "Steaks végétaux pour hamburgers",
                "alternative": True,
            },
            {
                "name": "Laits pasteurisés",
                "alternative": False,
            },
            {
                "name": "Laits végétaux",
                "alternative": True,
            },
            {
                "name": "Yaourts brassés",
                "alternative": False,
            },
            {
                "name": "Yaourts végétaux",
                "alternative": True,
            }
        ]

        # Connection to the database
        database = DbInteract()

        for category in products_categories:

            # Registration of each category in a SQL table
            category_reference = database.insert_category(category["name"], category["alternative"])

            # API call to get all food products for each category
            result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=" + category["name"] + "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action=display&json=1")
            products_details = result.json()

            for product in products_details["products"]:

                name = "product_name"
                nutrigrade = "nutrition_grades"
                store = "stores"
                brand = "brands"
                url = "url"
                description = "generic_name"
                image = "image_front_url"
                nutrition_image = "image_nutrition_small_url"

                # Test for each product if a name (or other below) is present.
                if product.get(name) and product.get(nutrigrade) and product.get(store) and product.get(brand) and product.get(url) and product.get(description) and product.get(image) and product.get(nutrition_image):
                    
                    name = product[name]
                    description = product[description]
                    url = product[url]
                    image = product[image]
                    nutrition_image = product[nutrition_image]
                    # Just to monitore
                    print(url)

                    nutrigrade = database.insert_nutrigrade(product[nutrigrade])

                    store = database.insert_store(product[store])

                    brand = database.insert_brand(product[brand])

                    database.insert_product(
                        name,
                        description,
                        url,
                        image,
                        nutrition_image,
                        category_reference,
                        brand,
                        store,
                        nutrigrade
                    )

                else:
                    continue # to the following product
