from django.contrib import admin
from home.models import Image
# Register your models here.
class AdminImageapp(admin.ModelAdmin):
    list_display = ('id', 'image', 'classification', 'upload_date')
    fieldsets = (
        (("Basic info"), {'fields':('image', 'classification')}),
    )

admin.site.register(Image, AdminImageapp)