from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='demo'),
    path('upload-demo-image/', views.upload_demo_image, name='upload-demo-image'),
    path('demo-in-action/', views.demo_in_action, name='demo-in-action'),
    path('download/<str:folder_name>/<str:file_name>', views.image_download, name='image_download'),
    path('delete/<str:folder_name>/<str:file_name>', views.image_delete, name='image_delete'),
]