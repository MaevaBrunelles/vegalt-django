""" Script to get data from OpenFoodFacts API and register them in a database """

import requests

from django.core.management.base import BaseCommand
from ._db_interact import DbInteract


class Command(BaseCommand):

    NAME = "product_name"
    NUTRIGRADE = "nutrition_grades"
    STORE = "stores"
    BRAND = "brands"
    URL = "url"
    DESCRIPTION = "generic_name"
    IMAGE = "image_front_url"
    NUTRITION_IMAGE = "image_nutrition_small_url"
    PRODUCTS_CATEGORIES = [
        {
            "name": ["Steaks hachés", "Saucisses françaises", "Jambons de Paris", "Laits pasteurisés", "Yaourts brassés", "Crèmes fraîches légères", "Viandes"],
            "alternative": False,
        },
        {
            "name": ["Steaks végétaux pour hamburgers", "Hamburgers végétariens", "Steak végétal", "Saucisses végétales", "Jambon végétal", "Laits végétaux", "Substitut du lait", "Yaourts végétaux", "Crèmes végétales pour cuisiner", "Substituts de viande"],
            "alternative": True,
        }
    ]

    def _does_product_contains_given_attributes(self, product, *attrs):
        """ Return True if the product contains all given attributes """

        for attribute in list(attrs[0]):
            if not product.get(attribute):
                return False

        return True

    def handle(self, *args, **options):
        """
        Get products informations from OpenFoodFacts
        and insert them in a database.
        """

        # pylint: disable=line-too-long

        # Connection to the database
        database = DbInteract()

        for categories in self.PRODUCTS_CATEGORIES:

            for category in categories["name"]:
                # Registration of each category in a SQL table
                category_reference = database.insert_category(category, categories["alternative"])

                # API call to get all food products for each category
                result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=" + category + "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action=display&json=1")
                products_details = result.json()

                for product in products_details["products"]:

                    attributes = [self.NAME, self.NUTRIGRADE, self.URL, self.IMAGE, self.NUTRITION_IMAGE, self.DESCRIPTION, self.STORE, self.BRAND]
                    if not self._does_product_contains_given_attributes(product, attributes):
                        continue # to the following product

                    else:
                        name = product[self.NAME]
                        description = product[self.DESCRIPTION]
                        url = product[self.URL]
                        image = product[self.IMAGE]
                        nutrition_image = product[self.NUTRITION_IMAGE]
                        # Just to monitore
                        print(url)

                        nutrigrade = database.insert_nutrigrade(product[self.NUTRIGRADE])

                        store = database.insert_store(product[self.STORE])

                        brand = database.insert_brand(product[self.BRAND])

                        database.insert_product(
                            name,
                            description,
                            url,
                            image,
                            nutrition_image,
                            category_reference,
                            brand,
                            store,
                            nutrigrade,
                        )

        self.stdout.write(self.style.SUCCESS('Successfully populate database'))
