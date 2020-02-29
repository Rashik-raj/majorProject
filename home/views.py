from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'home.htm')

def uploadImage(request):
    return HttpResponse('''hello <a href="/">home</a>''')