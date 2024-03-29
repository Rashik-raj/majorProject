from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('data_collection/', include('datacollection.urls')),
    path('demo/', include('demo.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT, }),
    re_path(r'^online_data_collection/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, }),
]
