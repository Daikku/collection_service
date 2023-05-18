from django.urls import path

from .views import *


urlpatterns = [
    path('', home_page, name='home_page'),
    path('list/', list_view, name='list_view'),
]