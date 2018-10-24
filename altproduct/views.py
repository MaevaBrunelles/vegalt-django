from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    h1_tag = "Mentions légales"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/legal.html', context)


def register(request):

    context = {
        'h1_tag': 'Créer un compte',
        'h2_tag': 'C\'est facile et rapide !',
        }

    if request.method == "POST":

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            user = User.objects.filter(email=email)
            if not user.exists():
                user = User.objects.create_user(username, email=email, password=password)
                return redirect('altproduct:login')

        else:
            context['errors'] = register_form.errors.items()

    else:
        register_form = RegisterForm()

    context['register_form'] = register_form

    return render(request, 'altproduct/account.html', context)


def login(request):

    context = {
        'h1_tag': 'Connexion à votre compte',
        'h2_tag': 'Entrez vos identifiants de connexion pour accéder à votre compte',
        'next': 'monurl'
    }

    # if request.method == "POST":
    #     login_form = LoginForm(request.POST)

    #     if login_form.is_valid():
    #         username = login_form.cleaned_data['username']
    #         password = login_form.cleaned_data['password']

    #         try:
    #             authenticate(username=username, password=password)
    #         except:
    #             print("marche pas")
    
    # else:
    #     login_form = LoginForm()

    # context['login_form'] = login_form

    # return render(request, 'altproduct/account.html', context)


def account(request):
    #h1_tag = "Ahoy " + username + " !"

    context = {
        'h1_tag': "LOL",
    }

    return render(request, 'altproduct/account.html', context)
