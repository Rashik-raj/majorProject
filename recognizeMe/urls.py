from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('datacollection/', include('datacollection.urls')),
    path('demo/', include('demo.urls')),
    path('result/',include('result.urls')),

]