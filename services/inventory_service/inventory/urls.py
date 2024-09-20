from django.urls import path
from .views import search_all_products

urlpatterns = [
    path('products/', search_all_products, name='search_all_products'),
]

