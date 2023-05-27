import pdf2image as p2i
import cv2

import os

# convert pdf pages to images
def convert_to_images(file, path):
     pages = p2i.convert_from_path(file, 500)
     count = 1
     images = [] 
     for i, page in enumerate(pages):
          if(i != 0):
               image = path + '/img-' + str(count) + ".jpg"
               count += 1
               page.save(image, "JPEG")
               images.append(image)
     
     return images

# get images already saved inside data/images
def get_images(dir_path):
     images_arr = []
     for image in os.listdir(dir_path):
          if(image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
               images_arr.append(dir_path + '/' + image)
     return images_arr

# resize an image
def resize(image, scaleX=0.2, scaleY=0.19):
     height = int(image.shape[0] * scaleY)
     width = int(image.shape[1] * scaleX)
     dimensions = (width,height)
     return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)