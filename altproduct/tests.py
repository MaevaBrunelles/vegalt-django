""" Unit tests + Integration tests """

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Product, Category, Brand, Store, NutriGrade


class ProductTestCase(TestCase):
    """ Unit and integration tests for searched product feature """

    def setUp(self):
        """ Create all necessary elements to create fake products """

        for i in range(5):
            category_name = "Fake category " + str(i)
            Category.objects.create(name=category_name, alternative=False)

        for i in range(5):
            alt_category_name = "Fake alt category " + str(i)
            Category.objects.create(name=alt_category_name, alternative=True)

        for i in range(10):
            store_name = "Fake store " + str(i)
            Store.objects.create(name=store_name)

        for i in range(10):
            brand_name = "Fake brand " + str(i)
            Brand.objects.create(name=brand_name)

        nutrigrades = ['a', 'b', 'c', 'd', 'e']
        for nutrigrade in nutrigrades:
            NutriGrade.objects.create(nutrigrade=nutrigrade)

        for i in range(20):
            product_name = "Fake product " + str(i)

            fake_category = Category.objects.order_by('?').first()
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

    def test_product_creation(self):
        """ Test product creation """

        fake_product = Product.objects.get(name='Fake product 1')
        self.assertEqual(fake_product.name, 'Fake product 1')

    def test_category_creation(self):
        """ Test category creation """

        fake_category = Category.objects.get(name='Fake category 1')
        self.assertEqual(fake_category.name, 'Fake category 1')

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

        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_product_page_returns_200(self):
        """ Product page with product name in URL returns 200 """

        fake_product = Product.objects.order_by('?').first()

        response = self.client.get(reverse('altproduct:product_detail', args=[fake_product.id, fake_product.name]))
        self.assertEqual(response.status_code, 200)

    def test_search_product_returns_product_from_same_category(self):
        """ When a product is searched,  """

        response = self.client.get(reverse('altproduct:alternative'), {'produit': 'Fake product'})

        fake_category = Category.objects.get(name__icontains=response.produit, alternative=False)
        fake_product = Product.objects.filter(category_id=fake_category.id).order_by('?')[1]

        self.assertEqual(fake_category, fake_product.category)


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

    def setUp(self):
        """ Create an user in test database """

        self.fake_user = User.objects.create_user(
            username='FakeUser',
            email='test@mail.com',
            password='fake_password'
        )

    def test_create_user_in_db(self):
        """ Get the user in database to verify if it's created """

        user = User.objects.get(username='FakeUser')
        self.assertEqual(user, self.fake_user)

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
