import cv2
import numpy as np

import sys
import getopt
import os

from helpers import convert_to_images, get_images, resize

PDF_DIR = "./resources/"
OUTPUT_DIR = "./data/images/"


def main(argv):
     flag = False
     
     try:
          opts, args = getopt.getopt(argv, "s")
     except getopt.GetoptError:
          print("invalid arguments")
          sys.exit()

     if len(args) > 0:
          for opt, arg in opts:
               if opt == '-s':
                    flag = True
                    
          pdf= args[0]
          dir = pdf.split(".pdf")[0]
          output_path = os.path.join(OUTPUT_DIR, dir)
          
          if flag:
               try:
                    images = get_images(output_path)
               except FileNotFoundError:
                    print("File not found")
                    sys.exit()
          else:
               try:
                    os.mkdir(output_path)
                    images = convert_to_images(PDF_DIR + pdf, output_path)
               except OSError:
                    print(OSError)
          
          for image in images:
               src_image = cv2.imread(image)
               sized_image = resize(src_image)
               grayscale_image = cv2.cvtColor(sized_image, cv2.COLOR_BGR2GRAY)
               blurred_image = cv2.GaussianBlur(grayscale_image, (5,5), cv2.BORDER_DEFAULT)
               
               # edge cascade
               t_lower = 130   #lower threshold
               t_upper = 225   #upper threshold
               edged_image = cv2.Canny(image=blurred_image, threshold1=t_lower, threshold2=t_upper, L2gradient=True)
               
               dilated_image = cv2.dilate(edged_image,(5,5), iterations=2)
               
               # ret, threshold_image = cv2.threshold(grayscale_image, 100, 255, cv2.THRESH_BINARY)
               
               contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
               
               answer_contours = []
               
               for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    if aspect_ratio > 1.4 and w > 50 and h > 20:
                         answer_contours.append(contour)
                         cv2.drawContours(sized_image, [contour], -1, (0,255,0), thickness=2)
                         
               print(len(answer_contours))
               
               cv2.imshow('dilated', dilated_image)
               cv2.imshow('After Contouring', sized_image)
               cv2.waitKey(0)
               cv2.destroyAllWindows()

if __name__ == "__main__":
     main(sys.argv[1:])