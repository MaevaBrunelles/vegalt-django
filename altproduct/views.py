from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    h1_tag = "Mentions légales"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/legal.html', context)


def register(request):

    context = {
        'h1_tag': 'Créer un compte',
        'h2_tag': 'Un nom, un mot de passe et c\'est parti !'
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

                return redirect('altproduct:account_login')

        else:
            context['errors'] = register_form.errors.items()

    else:
        register_form = RegisterForm()

    context['register_form'] = register_form

    return render(request, 'altproduct/account.html', context)


class CustomLoginView(LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'h1_tag': 'Connexion à votre compte',
            'h2_tag': 'Entrez vos identifiants de connexion pour accéder à votre compte',
            'next': reverse_lazy('altproduct:account')
        })

        return context


def account(request):

    context = {
        'h1_tag': 'Ahoy',
        'h2_tag': 'Paramètres de votre compte',
    }

    return render(request, 'altproduct/account.html', context)
