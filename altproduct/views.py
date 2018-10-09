from django.shortcuts import render, redirect
from .forms import AccountCreationForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    h1_tag = "Mentions légales"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/legal.html', context)


def account_creation(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username, email=email, password=password)

        return redirect('altproduct:account')

    else:
        h1_tag = "Créer un compte"
        account_form = AccountCreationForm()

        context = {
            'h1_tag': h1_tag,
            'form': account_form,
        }

        return render(request, 'altproduct/account.html', context)

def account(request):
    #h1_tag = "Ahoy " + username + " !"

    context = {
        'h1_tag': "LOL",
    }

    return render(request, 'altproduct/account.html', context)
