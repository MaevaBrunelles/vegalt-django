from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = "altproduct"

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legal, name='legal'),
    path('creer-compte/', views.register, name='register'),
    path('connexion/', LoginView.as_view(), name='login'),
    path('mon-compte/', views.account, name='account'),
]
