from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    h1_tag = "Mentions légales"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/legal.html', context)


def register(request):

    context = {
        'h1_tag': 'Créer un compte',
        }

    if request.method == "POST":

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            user = User.objects.filter(email=email)
            if not user.exists():
                User.objects.create_user(username, email=email, password=password)
                user = authenticate(username=username, password=password)

                context = {
                    'user': user,
                }

                return redirect('altproduct:account', context)

        else:
            context['errors'] = register_form.errors.items()

    else:
        register_form = RegisterForm()

    context['form'] = register_form

    return render(request, 'altproduct/account.html', context)


def account(request):
    #h1_tag = "Ahoy " + username + " !"

    context = {
        'h1_tag': "LOL",
    }

    return render(request, 'altproduct/account.html', context)
