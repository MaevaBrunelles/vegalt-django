""" Unit tests + Integration tests """

import json
from io import StringIO

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command

from .models import Product, Category, Brand, Store, NutriGrade, FavouriteProduct


def setUpModule():
    """ Create all necessary objects for application tests in test database. """

    fake_categories = ["Fake steak", "Fake milk", "Fake ham", "Fake sausage"]
    for fake_category_name in fake_categories:
        Category.objects.create(name=fake_category_name, alternative=False)

    fake_alt_categories = ["Fake alt steak", "Fake alt steak 2", "Fake alt steak 3", "Fake alt milk", "Fake alt ham", "Fake alt sausage"]
    for fake_alt_category_name in fake_alt_categories:
        Category.objects.create(name=fake_alt_category_name, alternative=True)

    for i in range(5):
        store_name = "Fake store " + str(i)
        Store.objects.create(name=store_name)

    for i in range(5):
        brand_name = "Fake brand " + str(i)
        Brand.objects.create(name=brand_name)

    nutrigrades = ['a', 'b', 'c', 'd', 'e']
    for nutrigrade in nutrigrades:
        NutriGrade.objects.create(nutrigrade=nutrigrade)

    all_fake_categories = fake_categories + fake_alt_categories
    for category in all_fake_categories:
        for i in range(2):
            product_name = category + " " + str(i)

            fake_category = Category.objects.get(name=category)
            nutrigrade = NutriGrade.objects.order_by('?').first()
            fake_store = Store.objects.order_by('?').first()
            fake_brand = Brand.objects.order_by('?').first()

            Product.objects.create(
                name=product_name,
                category=fake_category,
                store=fake_store,
                brand=fake_brand,
                nutrigrade=nutrigrade,
            )

    fake_user = User.objects.create_user(
        username='FakeUser',
        email='test@mail.com',
        password='fake_password'
    )

    fake_product = Product.objects.order_by('?').first()
    FavouriteProduct.objects.create(user_id=fake_user.id, product_id=fake_product.id)


class ProductTestCase(TestCase):
    """ Unit and integration tests for searched product feature """

    def test_product_creation(self):
        """ Test product creation """

        fake_product = Product.objects.get(name='Fake sausage 1')
        self.assertEqual(fake_product.name, 'Fake sausage 1')

    def test_category_creation(self):
        """ Test category creation """

        fake_category = Category.objects.get(name='Fake milk')
        self.assertEqual(fake_category.name, 'Fake milk')

    def test_store_creation(self):
        """ Test store creation """

        fake_store = Store.objects.get(name='Fake store 1')
        self.assertEqual(fake_store.name, 'Fake store 1')

    def test_brand_creation(self):
        """ Test brand creation """

        fake_brand = Brand.objects.get(name='Fake brand 1')
        self.assertEqual(fake_brand.name, 'Fake brand 1')

    def test_nutrigrade_creation(self):
        """ Test nutrigrade creation """

        nutrigrade_a = NutriGrade.objects.get(nutrigrade='a')
        self.assertEqual(nutrigrade_a.nutrigrade, 'a')

    def test_alternative_page_returns_200(self):
        """ Alternative page with URL parameter returns 200 """

        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'ham'})
        self.assertEqual(response.status_code, 200)

    def test_product_page_returns_200(self):
        """ Product page with product name in URL returns 200 """

        fake_product = Product.objects.order_by('?').first()

        response = self.client.get(reverse('altproduct:product_detail', args=[fake_product.id, fake_product.name]))
        self.assertEqual(response.status_code, 200)

    def test_non_existing_product_returns_error_message(self):
        """ Non existing product in database returns error message in HTML """

        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'Non existing product'})
        self.assertContains(response, '<p id="error-message">')


    def test_product_returned_is_alternative(self):
        """
        Verify that products returned are alternative products
        and are part of the same product range.
        """

        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'steak'})

        fake_alt_products = response.context['alt_products']

        categories = []
        for fake_alt_product in fake_alt_products.object_list:
            category = Category.objects.get(id=fake_alt_product.category.id)
            if category not in categories:
                categories.append(category)

        for category in categories:
            self.assertIn('steak', category.name)
            self.assertEqual(True, category.alternative)


class AccountViewsTestCase(TestCase):
    """ Unit tests for views """

    def test_login_page_returns_200(self):
        """ Login page returns 200 """

        response = self.client.get(reverse('altproduct:account_login'))
        self.assertEqual(response.status_code, 200)

    def test_bad_url_returns_404(self):
        """ Bad URL returns 404 """

        response = self.client.get('badurl')
        self.assertEqual(response.status_code, 404)


class AccountTestCase(TestCase):
    """ Integration tests for account feature """

    def test_create_user_in_db(self):
        """ Get the user in database to verify if it's created """

        user = User.objects.get(username='FakeUser')
        self.assertEqual(user.username, 'FakeUser')

    def test_good_login_returns_true(self):
        """ Test login with good credentials """

        login = self.client.login(username='FakeUser', password='fake_password')
        self.assertTrue(login)

    def test_bad_login_returns_error(self):
        """ Test login with bad credentials. Login must return True or False  """

        login = self.client.login(username='BadUser', password='fake_password')
        self.assertFalse(login)

    def test_logout_is_effective(self):
        """
        Test logout feature. When the client is login, a session is created
        with an id for the authentificated user, and it disappeared when the client logout.
        """

        self.client.login(username='FakeUser', password='fake_password')
        self.client.logout()
        self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])


class FavouriteProductTestCase(TestCase):
    """ Unit and integration tests for save product feature """

    def test_fav_products_page_returns_200(self):
        """ Favourite products page returns 200 """

        response = self.client.get(reverse('altproduct:fav_products'))
        self.assertEqual(response.status_code, 200)

    def test_alternative_page_doesnt_return_favourite_product(self):
        """
        Verify that products returned in alternative products
        page are not registered products.
        """

        fake_fav_product = FavouriteProduct.objects.order_by('?').first()

        self.client.login(username='FakeUser', password='fake_password')
        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'steak'})

        fake_alt_products = response.context['alt_products']

        self.assertNotIn(fake_fav_product, fake_alt_products)

    def fav_products_page_returns_alt_and_fav_products(self):
        """
        Verify that products returned in fav products page are alternative
        products registered by the user.
        """

        fake_fav_product = FavouriteProduct.objects.order_by('?').first()

        self.client.login(username='FakeUser', password='fake_password')
        response = self.client.get(reverse('altproduct:fav_products'))

        fake_fav_products = response.context['fav_products']
        # See test_product_returned_is_alternative test for object_list use
        category = Category.objects.get(id=fake_fav_products.object_list.category.id)

        self.assertEqual(fake_fav_products.object_list.id, fake_fav_product.product_id)
        self.assertEqual(True, category.alternative)

    def test_saved_product_ajax_feature(self):
        """
        Verify that an user can save a product as favourite.
        Call the Django route which get the Ajax post.
        If product is saved, the result page must return a success message,
        and a new instance is created in FavouriteProduct model with user and product ids.
        """

        fake_product = Product.objects.get(name='Fake alt milk 1')
        user = User.objects.get(username='FakeUser')

        data = {
            'user_id': user.id,
            'product_id': fake_product.id
        }

        self.client.login(username=user.username, password=user.password)
        response = self.client.post(reverse('altproduct:save_product'), data=data, HTTP_X_REQUESTED='XMLHttpRequest')

        response_json = json.loads(response.content)
        self.assertEqual(response_json['success_message'], 'Produit sauvegardé')

        fake_fav_product = FavouriteProduct.objects.get(user_id=user.id, product_id=fake_product.id)
        self.assertTrue(fake_fav_product)


class CommandTestCase(TestCase):
    """ Unit test for custom commands """

    def test_populate_db_command(self):
        """ Test if custom command populate_db is working well. """

        out = StringIO()
        call_command('populate_db', stdout=out)
        self.assertIn('Successfully populate database', out.getvalue())


def tearDownModule():
    """
    Delete all objects from test database.
    Don't change the order to respect foreign keys constraint.
    """

    FavouriteProduct.objects.all().delete()
    User.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Store.objects.all().delete()
    Brand.objects.all().delete()
    NutriGrade.objects.all().delete()
