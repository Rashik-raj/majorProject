from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='data_collection'),
    path('sample/download', views.sample_download, name='download_sample'),
    path('admin', views.data_collection, name='data_collection_list'),
    path('admin/download/<str:file_name>', views.data_collection_download, name='data_collection_download'),
    path('admin/delete/<str:file_name>', views.data_collection_delete, name='data_collection_delete'),
]