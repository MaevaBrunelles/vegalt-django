from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'altproduct/index.html')


def legal(request):
    return render(request, 'altproduct/legal.html')
