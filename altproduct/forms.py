from django.forms import ModelForm, EmailInput
from .models import User


class AccountCreationForm(ModelForm):
    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        
