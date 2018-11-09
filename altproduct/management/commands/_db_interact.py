""" Class to connect and communicate with the database (insert, get, select...) """

from altproduct.models import Category, Brand, Store, NutriGrade, Product

class DbInteract():
    """ Class to connect and communicate with the database (insert, get, select...) """

    def insert_category(self, name, alternative):
        """ Registration of categories in a SQL table """

        category = Category.objects.filter(name=name)

        if not category.exists():
            category_registered = Category.objects.create(name=name, alternative=alternative)
        else:
            category_registered = category.first()

        return category_registered


    def insert_brand(self, name):
        """ Registration of brand in a SQL table """

        brand = Brand.objects.filter(name=name)

        if not brand.exists():
            brand_registered = Brand.objects.create(name=name)
        else:
            brand_registered = brand.first()

        return brand_registered
    
    def insert_store(self, name):
        """ Registration of stores in a SQL table """

        store = Store.objects.filter(name=name)

        if not store.exists():
            store_registered = Store.objects.create(name=name)
        else:
            store_registered = store.first()

        return store_registered

    def insert_nutrigrade(self, score):
        """ Registration of nutrigrades in a SQL table """

        nutrigrade = NutriGrade.objects.filter(nutrigrade=score)

        if not nutrigrade.exists():
            nutrigrade_registered = NutriGrade.objects.create(nutrigrade=score)
        else:
            nutrigrade_registered = nutrigrade.first()

        return nutrigrade_registered


    def insert_product(self, product_name, description, link, image, nutrition_image, brand, category_id, nutrigrade, store):
        """ Insert the food product informations in the database """

        Product.objects.create(
            name=product_name,
            description=description,
            link=link,
            image=image,
            nutrition_image=nutrition_image,
            brand=brand,
            category=category_id,
            nutrigrade=nutrigrade,
            store=store,
        )

    # def get_categories(self, alternative):
    #     """Return the list of categories. Set alternative as 0 to get animals categories,
    #     and 1 to get vegetal categories"""

    #     try:
    #         connection = self._connection()

    #         with connection.cursor() as cursor:
    #             sql = "SELECT id, category_name FROM Categories WHERE alternative = %s;"
    #             cursor.execute(sql, (alternative))
    #             categories = cursor.fetchall()

    #     finally:
    #         connection.close()

    #     return categories

    # def get_products_from_category(self, category_id, limit):
    #     """Return x (limit) random products associated to the choosen category"""

    #     try:
    #         connection = self._connection()

    #         with connection.cursor() as cursor:
    #             sql = "SELECT product_name, brand_name FROM Food_product WHERE category_id = %s ORDER BY RAND() LIMIT %s;"
    #             cursor.execute(sql, (category_id, limit))
    #             products = cursor.fetchall()

    #     finally:
    #         connection.close()

    #     return products

    # def get_vegalt_product(self, veg_category_id, limit):
    #     """Return x (limit) random product associated to the choosen category,
    #     but on vegan version"""

    #     try:
    #         connection = self._connection()

    #         with connection.cursor() as cursor:
    #             sql_select_products = "SELECT id, product_name, brand_name, store, link FROM Food_product WHERE category_id = %s ORDER BY RAND() LIMIT %s;"
    #             cursor.execute(sql_select_products, (veg_category_id, limit))
    #             vegalt_product = cursor.fetchone()

    #     finally:
    #         connection.close()

    #     return vegalt_product

    # def register_product(self, product_id):
    #     """Put the product on registered by updating the "favourite" column of the product at 1"""
    #     try:
    #         connection = self._connection()

    #         with connection.cursor() as cursor:
    #             sql = "UPDATE Food_product SET favourite = 1 WHERE id = %s;"
    #             cursor.execute(sql, (product_id))

    #         connection.commit()

    #     finally:
    #         connection.close()

    # def get_registered_products(self):
    #     """Return the products registered = where "favourite" column equal to 1"""

    #     try:
    #         connection = self._connection()

    #         with connection.cursor() as cursor:
    #             sql = "SELECT product_name, brand_name, store, link FROM Food_product WHERE favourite = 1"
    #             cursor.execute(sql)
    #             fav_products = cursor.fetchall()

    #     finally:
    #         connection.close()

    #     return fav_products