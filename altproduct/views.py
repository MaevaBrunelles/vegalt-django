""" Views file """

import requests

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegisterForm, SearchForm


def index(request):
    """ Home route. """

    context = {
        'h1_tag': 'Du gras oui, mais de qualité !',
        'search_form': SearchForm()
    }
    return render(request, 'altproduct/index.html', context)


def legal(request):
    """ Legal route. """

    context = {
        'h1_tag': 'Mentions légales',
    }
    return render(request, 'altproduct/legal.html', context)


def register(request):
    """ Account creation route. """

    context = {
        'h1_tag': 'Créer un compte',
        'h2_tag': 'Un nom, un mot de passe et c\'est parti !'
        }

    # If the register form is posted
    if request.method == "POST":

        register_form = RegisterForm(request.POST)

        # Verify all datas posted
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            # Create the new user in database if it's not existing
            user = User.objects.filter(email=email)
            if not user.exists():
                user = User.objects.create_user(username, email=email, password=password)

                return redirect('altproduct:account_login')

        else:
            context['errors'] = register_form.errors.items()

    # If not, create the empty register form
    else:
        register_form = RegisterForm()

    context['register_form'] = register_form

    return render(request, 'altproduct/account.html', context)


class CustomLoginView(LoginView):
    """ Subclass from Django LoginView. Personnalized account login route. """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'h1_tag': 'Connexion à votre compte',
            'h2_tag': 'Entrez vos identifiants de connexion pour accéder à votre compte',
            'next': reverse_lazy('altproduct:account')
        })

        return context


def account(request):
    """ Account route """

    context = {
        'h1_tag': 'Ahoy',
        'h2_tag': 'Paramètres de votre compte',
    }

    return render(request, 'altproduct/account.html', context)


def alternative(request):
    """ Alternative route, when a product is searched """

    searched_product = request.GET.get('produit')

    #result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms=" + searched_product + "&sort_by=unique_scans_n&page_size=20&axis_x=energy&axis_y=products_n&action=display&json=1")
    result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms=" + searched_product + "&tagtype_0=categories&tag_contains_0=contains&tag_0=" + searched_product + "&sort_by=unique_scans_n&page_size=20&axis_x=energy&axis_y=products_n&action=display&json=1")
    
    products_details = result.json()

    #product_name = products_details["products"][0]["product_name_fr"]
    product_img = products_details["products"][0]["image_front_url"]

    context = {
        'h1_tag': searched_product,
        'h2_tag': 'Vous pouvez remplacer cet aliment par :',
        'searched_product_img': product_img,
    }

    return render(request, 'altproduct/alternative.html', context)
 