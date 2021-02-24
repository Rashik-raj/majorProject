from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .image_processing import image_preprocessing
import os
import shortuuid
import mimetypes

def get_images(folder_name):
    working_directory = os.getcwd()
    os.chdir(os.path.join(working_directory, 'online_data_collection', folder_name))
    images = []
    for each_img in os.listdir():
        images.append(each_img)
    os.chdir(working_directory)
    return images

# Create your views here.
def index(request):
    unprocessed_images = get_images('image_folder')
    processed_images = get_images('image_dataset')
    context = {
        'unprocessed_images': unprocessed_images,
        'processed_images': processed_images
        }
    return render(request, 'demo.htm', context=context)

def demo_in_action(request):
    # images, is_processed = image_preprocessing()
    is_processed = image_preprocessing()
    unprocessed_images = get_images('image_folder')
    processed_images = get_images('image_dataset')
    if is_processed:
        messages.success(request, 'Image Processing has been success!')
    else:
        messages.warning(request, 'No image to process!')
    context = {
        'unprocessed_images': unprocessed_images,
        'processed_images': processed_images
        }
    return render(request, 'demo.htm', context=context)

def upload_demo_image(request):
    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['data_image']
            file_extension = myfile.name.split('.')[-1]
            if file_extension not in ['jpg', 'jpeg', 'png']:
                messages.error(request, 'Please upload image with ".jpeg", ".jpg" or ".png" extension.')
            else:
                file_name = shortuuid.ShortUUID().random(length=8) + '.' + file_extension
                fs = FileSystemStorage()
                fs.save('image_folder/'+file_name, myfile)
                messages.success(request, 'Image Uploaded.')
        else:
            messages.error(request, 'Please select an image to upload.')
    return redirect('/demo')

def image_download(request, folder_name, file_name):
    file_path = os.path.join(os.getcwd(), "online_data_collection", folder_name, file_name)
    if os.path.exists(file_path):
        sample_image = open(file_path, 'rb')
        mime_type = mimetypes.guess_type(file_path)[0]
        response = HttpResponse(sample_image, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def image_delete(request, folder_name, file_name):
    file_path = os.path.join(os.getcwd(), "online_data_collection", folder_name, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('/demo')