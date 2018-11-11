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


    def insert_product(self, name, description, link, image, nutrition_image, category_id, brand, store, nutrigrade):
        """Insert the food product informations in the database"""

        product = Product.objects.filter(link=link)

        if not product.exists():
            Product.objects.create(
                name=name,
                description=description,
                link=link,
                image=image,
                nutrition_image=nutrition_image,
                category=category_id,
                brand=brand,
                store=store,
                nutrigrade=nutrigrade
            )
