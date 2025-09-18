from django.urls import path
from .views import shorten_url, redirect_to_original, index

urlpatterns = [
    path('', index, name='index'), 
    path('shorten', shorten_url, name='shorten_url'),
    path('<str:short_key>', redirect_to_original, name='redirect_to_original'),
]
