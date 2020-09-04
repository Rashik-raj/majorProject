from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_collection, name='data_collection'),
]