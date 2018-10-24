from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

### UNIT TEST ###

class LoginTestCase(TestCase):
    """ Login page returns 200 """

    def test_login_page_returns_200(self):
        response = self.client.get(reverse('altproduct:account_login'))
        self.assertEqual(response.status_code, 200)

# Login page returns 404

# Login page returns 500


### FUNCTIONNAL TEST ###

# Create User in database
class CreateUserTestCase(TestCase):
    def test_create_user_in_db(self):
        user = User.objects.create_user(username="FakeUser", email="test@mail.com", password="fake_password")
        fake_user = User.objects.get(username="FakeUser")
        self.assertEqual(fake_user, user)

# Check logout

# Account login

# Login error