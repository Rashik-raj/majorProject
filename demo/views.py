from django.shortcuts import render
from django.contrib import messages
from .image_processing import image_preprocessing

# Create your views here.
def index(request):
    return render(request, 'demo.htm')

def demo_in_action(request):
    images = image_preprocessing()
    messages.success(request, 'Image Processing has been success!')
    context = {'images':images}
    return render(request, 'demo.htm', context=context)