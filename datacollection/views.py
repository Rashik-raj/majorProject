from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpRequest
import shortuuid
import mimetypes
import os

# Create your views here.
def index(request):
    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['data_image']
            file_extension = myfile.name.split('.')[-1]
            if file_extension not in ['jpg', 'jpeg', 'png']:
                messages.error(request, 'Please upload image with ".jpeg", ".jpg" or ".png" extension.')
            else:
                file_name = shortuuid.ShortUUID().random(length=8) + '.' + file_extension
                fs = FileSystemStorage()
                messages.success(request, 'Thank your for uploading image.')
                fs.save(file_name, myfile)
        else:
            messages.error(request, 'Please select an image to upload.')
    return render(request, 'data_collection.htm')

def sample_download(request):
    file_path = os.getcwd() + "\\static\\img\\sample.jpg"
    filename = "sample.jpg"
    sample_image = open(file_path, 'rb')
    mime_type = mimetypes.guess_type(file_path)[0]
    response = HttpResponse(sample_image, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def data_collection(request):
    main_working_dir = os.getcwd()
    data_path = main_working_dir + "\\online_data_collection"
    image = []
    for (_, _, filenames) in os.walk(data_path):
        image.extend(filenames)
        break
    context = {'image': image}
    return render(request, 'data_collection_list.htm', context=context)

def data_collection_download(request, file_name):
    file_path = os.getcwd() + "\\online_data_collection\\" + file_name
    if os.path.exists(file_path):
        sample_image = open(file_path, 'rb')
        mime_type = mimetypes.guess_type(file_path)[0]
        response = HttpResponse(sample_image, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def data_collection_delete(request, file_name):
    file_path = os.getcwd() + "\\online_data_collection\\" + file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
