from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    h1_tag = "Mentions légales"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/legal.html', context)


def account(request):
    h1_tag = "Créer un compte"
    context = {'h1_tag': h1_tag}
    return render(request, 'altproduct/account.html', context)
