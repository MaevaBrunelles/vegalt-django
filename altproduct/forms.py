""" Forms file """

from django.forms import (
    ModelForm, EmailInput, PasswordInput, ValidationError, Form, CharField, TextInput
)
from django.contrib.auth.models import User


class RegisterForm(ModelForm):
    """ Form to create an account. Based on Django User model. """

    class Meta:
        """ Get the Django User attributes. """

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


class SearchForm(Form):
    """ Form to search a product alternative. Display on nav and index page. """

    product = CharField(
        max_length=200,
        widget=TextInput(attrs={
            'placeholder': 'Entrez le produit que vous voulez remplacer',
            })
    )

    def add_prefix(self, field_name):
        """ Custom field name to have the URL parameter in FR """

        field_name = "produit"
        return super(SearchForm, self).add_prefix(field_name)
