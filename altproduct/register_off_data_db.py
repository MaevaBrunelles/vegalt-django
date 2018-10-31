""" Script to get data from OpenFoodFacts API and register them in a database """

import os
import requests

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegalt.settings')
django.setup()

from db_interact import DbInteract

def main():
    """
    Get products informations from OpenFoodFacts
    and insert them in a database.
    """

    # pylint: disable=line-too-long

    # 0 if the category contains animals products, 1 if it contains only vegetals products
    products_categories = [
        {
            "name": "Steaks hachés",
            "alternative": 0,
        },
        {
            "name": "Steaks végétaux pour hamburgers",
            "alternative": 1,
        },
        {
            "name": "Laits pasteurisés",
            "alternative": 0,
        },
        {
            "name": "Laits végétaux",
            "alternative": 1,
        },
        {
            "name": "Yaourts brassés",
            "alternative": 0,
        },
        {
            "name": "Yaourts végétaux",
            "alternative": 1,
        }
    ]

    # Connection to the database
    database = DbInteract()

    for category in products_categories:

        # Registration of each category in a SQL table
        database.insert_category(category["name"], category["alternative"])

        # API call to get all food products for each category
        result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=" + category["name"] + "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action=display&json=1")
        products_details = result.json()

        # Get the category_id for product registration
        category_id = database.get_category_id(category["name"])

        for product in products_details["products"]:

            # Test for each product if a name (or other below) is present.
            # If not, put on None (= NULL in the database)
            name = "product_name"
            product_name = product[name] if name in product else None

            description = "generic_name"
            description = product[description] if description in product else None

            url = "url"
            url = product[url] if url in product else None

            store = "stores"
            store = product[store] if store in product else None

            brand = "brands"
            brand = product[brand] if brand in product else None

            nutri_grade = "nutrition_grades"
            nutri_grade = product[nutri_grade] if nutri_grade in product else None

            database.insert_product(product_name, description, brand, store, url, nutri_grade, category_id["id"])

            # Just to monitore
            print(url)

if __name__ == "__main__":
    main()
