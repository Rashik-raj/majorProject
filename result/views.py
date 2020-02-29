from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def result(request):
    return render(request,'result.htm')
