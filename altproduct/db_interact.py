""" Class to connect and communicate with the database (insert, get, select...) """

from models import Product

class DbInteract():
    """ Class to connect and communicate with the database (insert, get, select...) """

    # pylint: disable=line-too-long

    def insert_category(self, name, alternative):
        """Registration of categories in a SQL table"""

        Product.objects.create(name=name, alternative=alternative)

    def get_category_id(self, name):
        """Return the category_id for product registration"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "SELECT id FROM Categories WHERE category_name = (%s);"
                cursor.execute(sql, (name))
                category_id = cursor.fetchone()

        finally:
            connection.close()

        return category_id

    def insert_product(self, product_name, description, brand, store, url, nutri_grade, category_id):
        """Insert the food product informations in the database"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "INSERT INTO Food_product (product_name, description, brand_name, store, link, nutri_grade, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (product_name, description, brand, store, url, nutri_grade, category_id))

            connection.commit()

        finally:
            connection.close()

    def get_categories(self, alternative):
        """Return the list of categories. Set alternative as 0 to get animals categories,
        and 1 to get vegetal categories"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "SELECT id, category_name FROM Categories WHERE alternative = %s;"
                cursor.execute(sql, (alternative))
                categories = cursor.fetchall()

        finally:
            connection.close()

        return categories

    def get_products_from_category(self, category_id, limit):
        """Return x (limit) random products associated to the choosen category"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "SELECT product_name, brand_name FROM Food_product WHERE category_id = %s ORDER BY RAND() LIMIT %s;"
                cursor.execute(sql, (category_id, limit))
                products = cursor.fetchall()

        finally:
            connection.close()

        return products

    def get_vegalt_product(self, veg_category_id, limit):
        """Return x (limit) random product associated to the choosen category,
        but on vegan version"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql_select_products = "SELECT id, product_name, brand_name, store, link FROM Food_product WHERE category_id = %s ORDER BY RAND() LIMIT %s;"
                cursor.execute(sql_select_products, (veg_category_id, limit))
                vegalt_product = cursor.fetchone()

        finally:
            connection.close()

        return vegalt_product

    def register_product(self, product_id):
        """Put the product on registered by updating the "favourite" column of the product at 1"""
        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "UPDATE Food_product SET favourite = 1 WHERE id = %s;"
                cursor.execute(sql, (product_id))

            connection.commit()

        finally:
            connection.close()

    def get_registered_products(self):
        """Return the products registered = where "favourite" column equal to 1"""

        try:
            connection = self._connection()

            with connection.cursor() as cursor:
                sql = "SELECT product_name, brand_name, store, link FROM Food_product WHERE favourite = 1"
                cursor.execute(sql)
                fav_products = cursor.fetchall()

        finally:
            connection.close()

        return fav_products