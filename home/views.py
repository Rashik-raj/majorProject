from django.shortcuts import render
from django.http import HttpResponse
from home.form import ImageForm
from home.models import Image
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from tensorflow.keras.models import load_model
import os

# Create your views here.
def index(request):
    return render(request,'home.htm')

def imageClassifier(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.save()
        # data prediction
        model = load_model(os.getcwd() + '/home/cnn_mode.h5')
        
        # predicting images
        path = os.getcwd() + data.image.url
        img = image.load_img(path, target_size=(180, 180))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        img = mpimg.imread(path)
        plt.imshow(img)
        
        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)
        Image.objects.filter(id=data.id).update(classification=np.argmax(classes))
        output_img = '/classification_output/' + str(np.argmax(classes)) + ".jpg"
        predictions = []
        for count, val in enumerate(classes[0]):
            predictions.append([count, val])
        # print(np.max(classes))
        # print(np.argmax(classes))
        context = {
            'input_data': data,
            'predictions': predictions,
            'output_img': output_img
        }
        return render(request,'result.htm', context=context)
    else:
        print("form is not valid")
    return HttpResponse('''hello <a href="/">home</a>''')