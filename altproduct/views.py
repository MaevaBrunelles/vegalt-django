""" Views file """

import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.mail import BadHeaderError, send_mass_mail, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from python_http_client.exceptions import BadRequestsError

from .forms import RegisterForm, SearchForm, ContactForm
from .models import Product, Category, FavouriteProduct


def index(request):
    """ Home route. """

    context = {
        'search_form': SearchForm(),
    }

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            sender_mail = contact_form.cleaned_data['sender_mail']
            message = contact_form.cleaned_data['message']

            message_to_site = "Bonjour Vegalt,\n\nVoici un nouveau message de " + sender_mail + " :\n\n" + message + "\n\nBonne journée."
            subject_to_site = "Vegalt - Nouvelle demande de contact"

            message_to_sender = "Bonjour " + name + ",\n\n" + "L'équipe de Vegalt a bien reçu votre message. Nous vous répondons rapidement.\n\nBonne journée,\nVegalt"
            subject_to_sender = "Vegalt - Confirmation de contact"

            try:
                mail_to_site = (
                    subject_to_site,
                    message_to_site,
                    'vegalt@ovh.fr',
                    ['vegalt@ovh.fr']
                )

                mail_to_sender = (
                    subject_to_sender,
                    message_to_sender,
                    'vegalt@ovh.fr', # from=
                    ['vegalt@ovh.fr'] # to=
                )

                send_mass_mail((mail_to_site, mail_to_sender), fail_silently=False)

                return redirect('altproduct:thanks')

            except BadHeaderError:
                return HttpResponse('Invalid header found')
            except BadRequestsError as e:
                return None


    else:
        contact_form = ContactForm()

    context['h1_tag'] = 'Du gras oui, mais de qualité !',
    context['contact_form'] = contact_form

    return render(request, 'altproduct/index.html', context)


def thanks(request):
    """ Thanks route after contact form submission. """

    context = {
        'search_form': SearchForm(),
        'h1_tag': 'Reçu 5/5 !',
    }

    return render(request, 'altproduct/thanks.html', context)


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
                # User needs to activate his account
                user.is_active = False
                user.save()

                # Create an account activation mail
                subject = "Vegalt : Activez votre compte fraîchement créé !"
                content = "Veuillez confirmer votre mail et activer votre compte en cliquant sur le lien suivant :"
                signature = "A bientôt sur Vegalt !"

                # Get domain name for activation link
                protocol = "http://" # To be changed on prod by https ?
                host = request.get_host()

                # Create the message
                html_message = render_to_string('mail.html', {
                    'username': username,
                    'content': content,
                    'protocol': protocol,
                    'host': host,
                    'account_id': user.id,
                    'signature': signature
                })
                plain_message = strip_tags(html_message)

                # Set mails settings
                from_mail = 'vegalt@ovh.fr'
                to_mail = email

                send_mail(
                    subject,
                    plain_message,
                    from_mail,
                    [to_mail],
                    html_message=html_message
                )

                return redirect('altproduct:account_login')

        else:
            context['errors'] = register_form.errors.items()

    # If not, create the empty register form
    else:
        register_form = RegisterForm()

    context['register_form'] = register_form

    return render(request, 'altproduct/account.html', context)


def account_activation(request, account_id):
    """ Account activation route. Set the is_active field from User model to True. """

    user = User.objects.get(pk=account_id)
    user.is_active = True
    user.save()

    context = {
        'h1_tag': 'Activation de votre compte',
        'username': user.username,
    }

    return render(request, 'altproduct/activation.html', context)


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
    user = request.user

    context = {
        'h1_tag': searched_product,
        'search_form': SearchForm(),
        'searched_product': searched_product,
    }

    try:
        category = Category.objects.get(name__icontains=searched_product, alternative=False)
        product = Product.objects.filter(category_id=category.id).order_by('?')[1]

        context['searched_product_img'] = product.image
        context['h2_tag'] = 'Vous pouvez remplacer cet aliment par :'

        categories = Category.objects.filter(name__icontains=searched_product, alternative=True)

        # Isolate products registered by the user
        if user:
            fav_products = FavouriteProduct.objects.filter(user_id=user.id)
            fav_products_id = [fav_product.product_id for fav_product in fav_products]

        products = []
        for category in categories:
            # Get all products by category, excluding products registered
            products_per_category = Product.objects.filter(category_id=category.id).exclude(id__in=fav_products_id)

            for product in products_per_category:
                # Keep FR products
                if product not in products and not 'Hamburguesa' in product.name and not 'Bebida' in product.name:
                    products.append(product)

        if not products:
            context['h2_tag'] = 'Aucun produit alternatif n\'a été trouvé :('
            context['message'] = 'Essayez une nouvelle recherche avec un autre produit.'

        else:
            paginator = Paginator(products, 9)
            page = request.GET.get('page')
            alt_products = paginator.get_page(page)

            context['alt_products'] = alt_products
            context['paginate'] = True

    except Category.DoesNotExist:
        context['h2_tag'] = 'Votre recherche n\'a retourné aucun résultat'
        context['message'] = 'Essayez une nouvelle recherche avec un autre produit.'

    return render(request, 'altproduct/alternative.html', context)


def product_detail(request, product_id, product_name):
    """ Product detail route. """

    # Get product by id, because many products can have the same name
    product = Product.objects.get(id=product_id)

    context = {
        'h1_tag': product_name,
        'h2_tag': 'Informations nutritionnelles',
        'search_form': SearchForm(),
        'product': product,
        'searched_product_img': product.image,
    }

    return render(request, 'altproduct/product.html', context)


def save_product(request):
    """ Route to get save product Ajax script. Return confirmation or error message. """

    response_data = {}

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')

        fav_product_for_current_user = FavouriteProduct.objects.filter(product_id=product_id, user_id=user_id)
        if not fav_product_for_current_user.exists():
            FavouriteProduct.objects.create(product_id=product_id, user_id=user_id)
            response_data['success_message'] = 'Produit sauvegardé'
        else:
            response_data['error_message'] = 'Produit déjà sauvegardé'

    else:
        response_data['error_message'] = 'Impossible de sauvegarder le produit'

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json',
    )


def fav_products(request):
    """ Favourite products page. Need an account to have access to it. """

    context = {
        'h1_tag': 'Les alternatives gardées au chaud',
        'search_form': SearchForm(),
    }

    user = request.user
    fav_products = FavouriteProduct.objects.filter(user_id=user.id)

    if fav_products.exists():
        products = []
        for fav_product in fav_products:
            product = Product.objects.get(id=fav_product.product_id)
            if product not in products:
                products.append(product)

        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        alt_products = paginator.get_page(page)

        context['h2_tag'] = 'Très bon choix :)'
        context['alt_products'] = alt_products
        context['paginate'] = True

    else:
        context['h2_tag'] = 'Pas de produit enregistré pour le moment'
        context['message'] = 'Faites vite une recherche !'

    return render(request, 'altproduct/alternative.html', context)
