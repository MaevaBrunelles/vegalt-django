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
                "name": "Steaks hachés 2",
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

            # Get the category_id for product registration
            #category_registered = database.get_category_id(category["name"])

            for product in products_details["products"]:

                # Test for each product if a name (or other below) is present.
                # If not, put on None (= NULL in the database)
                store = "stores"
                store = product[store] if store in product else None
                store = database.insert_store(store)

                brand = "brands"
                brand = product[brand] if brand in product else None
                brand = database.insert_brand(brand)

                nutrigrade = "nutrition_grades"
                nutrigrade = product[nutrigrade] if nutrigrade in product else None
                nutrigrade = database.insert_nutrigrade(nutrigrade)

                name = "product_name"
                product_name = product[name] if name in product else None

                description = "generic_name"
                description = product[description] if description in product else None

                url = "url"
                url = product[url] if url in product else None

                database.insert_product(product_name, description, brand, store, url, nutrigrade, category_reference)

                # Just to monitore
                print(url)

