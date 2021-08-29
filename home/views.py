import os
import shutil

import cv2
import matplotlib.pyplot as plt
import numpy as np
import shortuuid
import tensorflow as tf
from django.contrib import messages
from django.shortcuts import redirect, render
from keras.preprocessing import image
from recognizeMe.settings import BASE_DIR
from skimage import img_as_ubyte
from skimage.filters import threshold_sauvola
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from home.form import ImageForm
from home.models import Image

plt.style.use('seaborn')


def imgName():
    return str(shortuuid.uuid()) + '.jpg'


def preprocessImage(img_path):
    # preprocess and load input image
    img = cv2.imread(img_path)
    resized_image = cv2.resize(img, (250, 250))
    # removing noise form colored images
    denoised_image = cv2.fastNlMeansDenoisingColored(
        resized_image, None, 10, 10, 7, 21)
    denoised_img_name = imgName()
    cv2.imwrite("online_data_collection/image_processing/" +
                denoised_img_name, denoised_image)
    # Since denoiseing converts BGR image to CELAB, converting CELAB to BGR
    bgr_image = cv2.cvtColor(denoised_image, cv2.COLOR_Lab2BGR)
    bgr_img_name = imgName()
    cv2.imwrite("online_data_collection/image_processing/" +
                bgr_img_name, bgr_image)
    # Converion of BGR to Grayscale
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    gray_img_name = imgName()
    cv2.imwrite("online_data_collection/image_processing/" +
                gray_img_name, gray_image)
    # Binarization
    thres_sauvola = threshold_sauvola(gray_image, window_size=17)
    binary_sauvola = gray_image > thres_sauvola
    binary_sauvola = img_as_ubyte(binary_sauvola)
    binary_img_name = imgName()
    cv2.imwrite("online_data_collection/image_processing/" +
                binary_img_name, binary_sauvola)
    # Smoothing image
    # smooth_image = cv2.medianBlur(binary_sauvola, 3)
    smooth_image = cv2.bilateralFilter(binary_sauvola, 9, 75, 75)
    smooth_img_name = imgName()
    cv2.imwrite("online_data_collection/image_processing/" +
                smooth_img_name, smooth_image)
    return denoised_img_name, bgr_img_name, gray_img_name, binary_img_name, smooth_img_name

# Create your views here.


def check_directory():
    os.chdir(os.path.join(BASE_DIR))
    dir_names = ['chart', 'classification_input', 'image_dataset',
                 'image_extraction_complete', 'image_folder', 'image_processing', 'layer_image']
    for name in dir_names:
        if not os.path.isdir(os.path.join(BASE_DIR, 'online_data_collection', name)):
            os.mkdir(os.path.join(BASE_DIR, 'online_data_collection', name))
        for filename in os.listdir(os.path.join(BASE_DIR, 'online_data_collection', name)):
            file_path = os.path.join(os.path.join(
                BASE_DIR, 'online_data_collection', name), filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                pass


def index(request):
    check_directory()
    return render(request, 'home.htm')


def trainGraph(request):
    return render(request, 'train_graph.htm')


def imageClassifier(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        working_directory = os.getcwd()
        data = form.save()
        # data prediction
        model = load_model(working_directory + '/home/cnn_model.h5')

        # predicting images
        path = os.getcwd() + data.image.url
        denoised_img_name, bgr_img_name, gray_img_name, binary_img_name, smooth_img_name = preprocessImage(
            path)
        path = os.path.join(os.getcwd(), 'online_data_collection',
                            'image_processing', smooth_img_name)
        img = image.load_img(path, target_size=(180, 180))
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
            predictions.append([count, np.round(val, 5) * 100])
        x_axis = [x[0] for x in predictions]
        y_axis = [x[1] for x in predictions]
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
        plt.close(fig='all')

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
        layer_names = [layer.name for layer in model.layers[:]]

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
                plt.clf()
                plt.figure(figsize=(scale * n_features, scale))
                plt.title(layer_name)
                plt.grid(False)
                plt.imshow(display_grid, aspect='auto', cmap='viridis')
                plt.savefig(layer_name + ".jpg")
                plt.close(fig='all')
                layer_name_list.append(
                    [layer_name, '/layer_image/' + layer_name + ".jpg"])

        context = {
            'input_data': data,
            'predictions': predictions,
            'output_img': output_img,
            'predicted': np.argmax(classes),
            'preprocess_imgs': [
                ['Denoised Image', denoised_img_name],
                ['BGR Image', bgr_img_name],
                ['Gray Image', gray_img_name],
                ['Binary Image', binary_img_name],
                ['Smooth Image', smooth_img_name]
            ],
            'chart': 'chart/' + graph_name,
            'layers': layer_name_list,
        }
        os.chdir(working_directory)
        return render(request, 'result.htm', context=context)
    else:
        messages.warning(request, 'Please upload valid image file!')
        return redirect('/')
