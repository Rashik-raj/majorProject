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
        os.chdir(os.path.join(working_directory, image_dir_folder))
        """
        image_collection : read gareko image halna lai
        image_names : images haru ko name halna lai which will be used later
        """
        image_collection = []
        image_names = []
        for each_image in os.listdir():
                image_names.append(each_image)
                image_collection.append(cv2.imread(each_image))
        """
        counter : image ko name halna lai use garne
        """
        image_name_counter = 0
        for i, each_image in enumerate(image_collection):                
                resized_image = cv2.resize(each_image, (800, 800))                
                #image bata noise remove garna
                denoised_image = cv2.fastNlMeansDenoisingColored(resized_image)                
                gray_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)                
                #Calaculate histogram
                hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
                plt.plot(hist)                
                #Sauvola's thresholding
                thresh_sauvola = threshold_sauvola(gray_image, window_size = 17)
                binary_sauvola = gray_image > thresh_sauvola
                binary_sauvola = img_as_ubyte(binary_sauvola)
                #cv2.imshow("binarized image", binary_sauvola)
                #cv2.waitKey()
                #smooth_image_gb = cv2.GaussianBlur(binary_sauvola, (11, 11), 0)
                image_copy= binary_sauvola.copy() 
                #Image lai smoothing gareko using median filtering
                #kernel_size = (7, 7)
                #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, kernel_size)
                #closing_img = cv2.morphologyEx(image_copy, cv2.MORPH_GRADIENT, kernel)
                #opening_img = cv2.morphologyEx(closing_img, cv2.MORPH_OPEN, kernel)
                smooth_image_mb = cv2.medianBlur(image_copy, 3)
                #cv2.imshow("smoothing image", smooth_image_mb)
                #cv2.waitKey()
                contour, hierarchy = cv2.findContours(smooth_image_mb, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)    
                #cntr_sizes = sorted([cv2.contourArea(ctr) for ctr in contour])
                #cntr_sizes , sorted_cntr = zip(*sorted(zip(cntr_sizes, contour)))
                sorted_ctrs = sorted(contour, key=lambda ctr: cv2.boundingRect(ctr)[0])
                for j, ctr in enumerate(sorted_ctrs[1:]):
                        x, y, w, h = cv2.boundingRect(ctr)                        
                        roi = smooth_image_mb[y: y+h, x : x+w]                        
                        #dim = roi.shape
                        #cv2.imshow("dim", roi)
                        #cv2.waitKey()                        
                        resized_image = cv2.resize(roi, (28, 28))                        
                        #ataset folder ma image halna lai
                        os.chdir(os.path.join(working_directory, dataset_folder))
                        cv2.imwrite(str(image_name_counter) + '.jpg', resized_image)
                        image_name_counter += 1        
                #sabai extract vaisake paxi original image lai chuttai folder ma halna
                os.chdir(os.path.join(working_directory, extraction_complete_folder))
                cv2.imwrite(str(image_names[i]), each_image)
                #sabai kaam sakesi original image lai folder bata delete garne
                os.chdir(os.path.join(working_directory, image_dir_folder))
                for each_file in os.listdir():
                        os.remove(each_file)
                cv2.destroyAllWindows()
        os.chdir(working_directory)