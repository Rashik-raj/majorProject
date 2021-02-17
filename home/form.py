from django.forms import ModelForm
from home.models import Image

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image', ]
