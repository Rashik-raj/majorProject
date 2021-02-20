from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('image_classifier/', views.imageClassifier, name='image_classifier'),
]