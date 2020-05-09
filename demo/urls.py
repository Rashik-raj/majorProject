from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='demo'),
    path('demo-in-action/', views.demo_in_action, name='demo-in-action'),
]