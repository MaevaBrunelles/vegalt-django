""" URLs file """

from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from .views import CustomLoginView

app_name = "altproduct"

urlpatterns = [
    path('', views.index, name='index'),
    path('mentions-legales/', views.legal, name='legal'),
    path('creer-compte/', views.register, name='register'),
    path('connexion/', CustomLoginView.as_view(), name='account_login'),
    path('deconnexion/', LogoutView.as_view(), name='logout'),
    path('mon-compte/', views.account, name='account'),
    path('alternatives/', views.alternative, name='alternative'),
    path('alternatives/save_product/', views.save_product, name='save_product'), # Ajax view
    path('produit-alternatif/<str:product_id>/<str:product_name>/', views.product_detail, name='product_detail'),
    path('mes-produits/', views.fav_products, name='fav_products'),
]
