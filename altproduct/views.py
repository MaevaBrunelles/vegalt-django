""" Views file """

import requests
import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegisterForm, SearchForm
from .models import Product, Category


def index(request):
    """ Home route. """

    context = {
        'h1_tag': 'Du gras oui, mais de qualité !',
        'search_form': SearchForm(),
    }
    return render(request, 'altproduct/index.html', context)


def legal(request):
    """ Legal route. """

    context = {
        'h1_tag': 'Mentions légales',
        'search_form': SearchForm(),
    }
    return render(request, 'altproduct/legal.html', context)


def register(request):
    """ Account creation route. """

    context = {
        'h1_tag': 'Créer un compte',
        'h2_tag': 'Un nom, un mot de passe et c\'est parti !',
        'search_form': SearchForm(),
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
            'search_form': SearchForm(),
            'next': reverse_lazy('altproduct:account')
        })

        return context


def account(request):
    """ Account route """

    context = {
        'h1_tag': 'Ahoy',
        'h2_tag': 'Paramètres de votre compte',
        'search_form': SearchForm(),
    }

    return render(request, 'altproduct/account.html', context)


def alternative(request):
    """ Alternative route, when a product is searched """

    searched_product = request.GET.get('produit')

    context = {
        'h1_tag': searched_product,
        'search_form': SearchForm(),
    }

    category = Category.objects.get(name__icontains=searched_product, alternative=False)
    product = Product.objects.filter(category_id=category.id).order_by('?')[1]

    # tag_0 == category
    #result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms=" + searched_product + "&tagtype_0=categories&tag_contains_0=contains&tag_0=" + searched_product + "&sort_by=unique_scans_n&page_size=20&axis_x=energy&axis_y=products_n&action=display&json=1")
    #products_details = result.json()

    #if products_details['count'] == 0:
    #    context['h2_tag'] = 'Votre recherche n\'a retourné aucun résultat'
    #    context['message'] = 'Essayez une nouvelle recherche avec un autre produit.'

    #else:
        #product_img = products_details["products"][0]["image_front_url"]
    context['searched_product_img'] = product.image

    #alt_category = searched_product + " vegetal"
    #result2 = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=" + alt_category + "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action=display&json=1")
    #alt_products = result2.json()

    # if alt_products['count'] == 0:
    #     context['h2_tag'] = 'Aucun produit alternatif n\'a été trouvé :('
    #     context['message'] = 'Essayez une nouvelle recherche avec un autre produit.'
    # else:
    #     random_alt_products = []
    #     for _ in range(6):
    #         alt_product = random.choice(alt_products['products'])
    #         if 'product_name_fr' in alt_product and 'image_front_url' in alt_product:
    #             random_alt_products.append(alt_product)
    #         else:
    #             continue

    context['h2_tag'] = 'Vous pouvez remplacer cet aliment par :'
        #context['alt_products'] = random_alt_products

    return render(request, 'altproduct/alternative.html', context)
 

def product_detail(request, product_id, product_name):
    """ Product detail route. """
    
    result = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms=" + product_name + "&sort_by=unique_scans_n&page_size=20&axis_x=energy&axis_y=products_n&action=display&json=1")
    products = result.json()

    product_detail = {}
    for product in products['products']:
        if product['id'] == product_id:
            #product_nutrigrade = product_details['']
            product_detail['url'] = product['url']
            product_detail['nutriscore'] = product['nutrition_grade_fr']
            product_detail['nutrition_img'] = product['image_nutrition_small_url']
            product_img = product['image_front_url']

    context = {
        'h1_tag': product_name,
        'h2_tag': 'Informations nutritionnelles',
        'search_form': SearchForm(),
        'product': product_detail,
        'searched_product_img': product_img,
    }

    return render(request, 'altproduct/product.html', context)
