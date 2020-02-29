from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('uploadImage/', views.uploadImage, name='uploadImage')
]