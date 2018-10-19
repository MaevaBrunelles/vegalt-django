from django.urls import path

from . import views
from .views import CustomLoginView

app_name = "altproduct"

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legal, name='legal'),
    path('creer-compte/', views.register, name='register'),
    path('connexion/', CustomLoginView.as_view(), name='account_login'),
    path('mon-compte/', views.account, name='account'),
]
