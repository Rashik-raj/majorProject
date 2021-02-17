from django.shortcuts import render, redirect
from django.contrib import messages
from home.form import ImageForm
from home.models import Image
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.filters import threshold_sauvola
from skimage import img_as_ubyte
from tensorflow.keras.models import load_model
import os
import cv2
import shortuuid

import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
plt.style.use('seaborn')


def preprocessImage(img_path):
    # preprocess and load input image
    img = cv2.imread(img_path)

    resized_image = cv2.resize(img, (180, 180))
    # image bata noise remove garna
    denoised_image = cv2.fastNlMeansDenoisingColored(resized_image)
    gray_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
    # Sauvola's thresholding
    thresh_sauvola = threshold_sauvola(gray_image, window_size=17)
    binary_sauvola = gray_image > thresh_sauvola
    binary_sauvola = img_as_ubyte(binary_sauvola)
    image_copy = binary_sauvola.copy()

    smooth_image_mb = cv2.medianBlur(image_copy, 3)
    resized_image = cv2.resize(smooth_image_mb, (250, 250))
    resized_img_name = str(shortuuid.uuid()) + '.jpg'
    cv2.imwrite(resized_img_name, resized_image)
    return resized_img_name

# Create your views here.


def index(request):
    return render(request, 'home.htm')


def imageClassifier(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        working_directory = os.getcwd()
        data = form.save()
        # data prediction
        model = load_model(os.getcwd() + '/home/cnn_model.h5')

        # predicting images
        path = os.getcwd() + data.image.url
        path = preprocessImage(path)
        img = image.load_img(path, target_size=(180, 180))
        os.remove(path)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)
        Image.objects.filter(id=data.id).update(
            classification=np.argmax(classes))
        output_img = '/classification_output/' + \
            str(np.argmax(classes)) + ".jpg"
        predictions = []
        for count, val in enumerate(classes[0]):
            predictions.append([count, np.round(val, 5)])
        # print(np.max(classes))
        # print(np.argmax(classes))
        x_axis = [x[0] for x in predictions]
        y_axis = [x[1]*100 for x in predictions]
        upload_img_path = data.image.url
        upload_img_name = upload_img_path.split('/')[-1]
        graph_name = upload_img_name.split('.')[0] + '_graph.png'
        os.chdir(os.path.join(working_directory,
                              'online_data_collection', 'chart'))
        plt.clf()
        barplot = plt.bar(x_axis, y_axis)
        plt.suptitle('Probability values vs Classes')
        for bar in barplot:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() /
                     2.0, yval, int(yval), va='bottom')
        plt.xlabel('Classes')
        plt.ylabel('Probability values (in %)')
        plt.xticks(range(len(x_axis)), x_axis, size='small')
        plt.savefig(graph_name, dpi=400)

        # Creating image for each layer

        os.chdir(os.path.join(working_directory,
                              'online_data_collection', 'layer_image'))
        successive_outputs = [layer.output for layer in model.layers[1:]]
        visualization_model = tf.keras.models.Model(
            inputs=model.input, outputs=successive_outputs)

        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        # Rescale by 1/255
        x /= 255
        successive_feature_maps = visualization_model.predict(x)
        layer_names = [layer.name for layer in model.layers[1:]]

        layer_name_list = []
        # Now let's display our representations
        for layer_name, feature_map in zip(layer_names, successive_feature_maps):
            if len(feature_map.shape) == 4:
                # Just do this for the conv / maxpool layers, not the fully-connected layers
                # number of features in feature map
                n_features = feature_map.shape[-1]
                # The feature map has shape (1, size, size, n_features)
                size = feature_map.shape[1]
                # We will tile our images in this matrix
                display_grid = np.zeros((size, size * n_features))
                for i in range(n_features):
                    # Postprocess the feature to make it visually palatable
                    x = feature_map[0, :, :, i]
                    x -= x.mean()
                    x /= x.std()
                    x *= 64
                    x += 128
                    x = np.clip(x, 0, 255).astype('uint8')
                    # We'll tile each filter into this big horizontal grid
                    display_grid[:, i * size: (i + 1) * size] = x
                # Display the grid
                scale = 50. / n_features
                plt.figure(figsize=(scale * n_features, scale))
                plt.title(layer_name)
                plt.grid(False)
                plt.imshow(display_grid, aspect='auto', cmap='viridis')
                plt.savefig(layer_name + ".jpg")
                layer_name_list.append('/layer_image/' +
                                       layer_name + ".jpg")

        context = {
            'input_data': data,
            'predictions': predictions,
            'output_img': output_img,

            'chart': 'chart/' + graph_name,
            'layers': layer_name_list,
        }
        os.chdir(working_directory)
        return render(request, 'result.htm', context=context)
    else:
        messages.warning(request, 'Please upload valid image file!')
