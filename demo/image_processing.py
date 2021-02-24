# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:54:24 2020

@author: SurajRatnaKalu
"""

#Importing all the required librarires
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_sauvola
from skimage import img_as_ubyte
import shortuuid
import os

# #Setting the working directory manually
# os.chdir('C:\opencvpython\image')
def image_preprocessing():
        working_directory = os.getcwd()
        #image extract garnu parne folder
        image_dir_folder = 'image_folder'
        #extract gareko image halne folder
        dataset_folder = 'image_dataset'
        #extract garisakepaxi original image halne folder
        extraction_complete_folder = 'image_extraction_complete'
        #changing the working directory to image vayeko directory
        os.chdir(os.path.join(working_directory, 'online_data_collection', image_dir_folder))
        """
        image_collection : read gareko image halna lai
        image_names : images haru ko name halna lai which will be used later
        """
        # extracted_image_name = []
        if os.listdir():
                image_collection = []
                image_names = []
                for each_image in os.listdir():
                        image_names.append(each_image)
                        image_collection.append(cv2.imread(each_image))
                """
                extracted_image_name : image ko name return garna ko lai
                """
                for i, each_image in enumerate(image_collection):                
                        resized_image = cv2.resize(each_image, (800, 800))                
                        #image bata noise remove garna
                        denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 10, 7, 21)                
                        # Since denoiseing converts BGR image to CELAB, converting CELAB to BGR
                        bgr_image = cv2.cvtColor(denoised_image, cv2.COLOR_Lab2BGR)

                        # Converion of BGR to Grayscale
                        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

                        # Binarization
                        thres_sauvola = threshold_sauvola(gray_image, window_size=17)
                        binary_sauvola = gray_image > thres_sauvola
                        binary_sauvola = img_as_ubyte(binary_sauvola)

                        # Smoothing image
                        smooth_image = cv2.medianBlur(binary_sauvola, 3)

                        # Inverting image so that characters are white and background is black
                        inverted_image = cv2.bitwise_not(smooth_image)

                        # finding the contours
                        contour, hierarchy = cv2.findContours(
                        inverted_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                        sorted_ctrs = sorted(contour, key=lambda ctr: cv2.boundingRect(ctr)[0])
                        for j, ctr in enumerate(sorted_ctrs[1:]):
                                x, y, w, h = cv2.boundingRect(ctr)
                                roi = inverted_image[y: y+h, x: x+w]
                                resized_image = cv2.resize(roi, (28, 28))
                                reinverted_image = cv2.bitwise_not(resized_image)                       
                                #dataset folder ma image halna lai
                                os.chdir(os.path.join(working_directory, 'online_data_collection', dataset_folder))
                                img_name = str(shortuuid.uuid()) + '.jpg'
                                cv2.imwrite(img_name, reinverted_image)
                                # extracted_image_name.append('image_dataset/' + img_name)    
                        #sabai extract vaisake paxi original image lai chuttai folder ma halna
                        os.chdir(os.path.join(working_directory, 'online_data_collection', extraction_complete_folder))
                        cv2.imwrite(str(image_names[i]), each_image)
                        #sabai kaam sakesi original image lai folder bata delete garne
                        os.chdir(os.path.join(working_directory, 'online_data_collection', image_dir_folder))
                        for each_file in os.listdir():
                                os.remove(each_file)
                        cv2.destroyAllWindows()
                os.chdir(working_directory)
                # return extracted_image_name, True
                return True
        else:
                os.chdir(working_directory)
                # return extracted_image_name, False
                return False