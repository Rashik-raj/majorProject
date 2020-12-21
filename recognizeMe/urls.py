from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('datacollection/', include('datacollection.urls')),
    path('demo/', include('demo.urls')),
    path('result/',include('result.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),
    re_path(r'^online_data_collection/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]