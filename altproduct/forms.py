""" Forms file """

from django.forms import ModelForm, EmailInput, PasswordInput, ValidationError
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.html import format_html


class RegisterForm(ModelForm):
    """ Form to create an account. Based on Django User model. """

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'email': EmailInput(),
            'password': PasswordInput()
        }

    def clean_email(self):
        """
        Force verification to have unique email per account. Not by default on User Django model.
        """

        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(u'Un utilisateur avec cette adresse email existe déjà.')

        return email


# class LoginForm(ModelForm):

#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = {
#             'password': PasswordInput()
#         }
