""" Unit tests + Integration tests """

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
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
