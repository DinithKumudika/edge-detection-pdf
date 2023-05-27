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
               image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
               
               image = resize(image)
               
               image = cv2.GaussianBlur(image, (5,5), cv2.BORDER_DEFAULT)
               
               # edge cascade
               t_lower = 125   #lower threshold
               t_upper = 175   #upper threshold
               image = cv2.Canny(image, t_lower, t_upper, L2gradient=True)
               
               image = cv2.dilate(image,(7,7), iterations=2)
               
               cv2.imshow('Image 1', image)
               cv2.waitKey(0)
               cv2.destroyAllWindows()

if __name__ == "__main__":
     main(sys.argv[1:])