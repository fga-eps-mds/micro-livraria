from django.urls import path
from .views import get_shipping_rate

urlpatterns = [
    path('rate/', get_shipping_rate, name='get_shipping_rate'),
]

