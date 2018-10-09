from django.forms import ModelForm, EmailInput, PasswordInput
from django.contrib.auth.models import User


class AccountCreationForm(ModelForm):
    class Meta:

        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'email': EmailInput(),
            'password': PasswordInput()
        }
