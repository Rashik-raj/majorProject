from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import shortuuid

# Create your views here.
def data_collection(request):
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
                fs.save("online_data_collection/"+file_name, myfile)
        else:
            messages.error(request, 'Please select an image to upload.')
    return render(request, 'data_collection.htm')