import cv2
import numpy as np
from dotenv import dotenv_values

import sys
import getopt
import os

from helpers import *

PDF_DIR = "./resources/"
OUTPUT_DIR = "./data/images/"
CROPPED_IMG_DIR = "./data/cropped/"

def main(argv):
     config = dotenv_values(".env")
     
     draw = False
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
          
          if(draw):
               save_path = os.path.join(CROPPED_IMG_DIR, dir)
               os.mkdir(save_path)
          
          for img_idx, image in enumerate(images):
               selection = []
               is_selecting = False
               src_image = cv2.imread(image)
               screen_width = get_screen_width()
               screen_height = get_screen_height() 
               sized_image = resize(src_image, screen_height, screen_width)
               
               if(draw):
                    cv2.namedWindow(winname="Mark answer")
                    params = {
                         "output_folder": output_path,
                         "image": sized_image,
                         "coords": selection
                    }
                    cv2.setMouseCallback("Mark answer", draw_rectangle, params)
                    
                    while True:
                         cv2.imshow("Mark answer", sized_image)
                         
                         # wait for key press
                         key = cv2.waitKey(1) & 0xFF
                         
                         # Press 'r' to reset the selection
                         if key == ord('r'):
                              selection = []
                              src_image = cv2.imread(image)
                              sized_image = resize(src_image, screen_height, screen_width)
                         # Press 'c' to crop and save the selected areas
                         elif key == ord("c"):
                              for sel_idx, sel in enumerate(selection):
                                   crop_and_save(sized_image, sel, save_path, sel_idx, img_idx)
                              break
                         # Press 'Esc' to exit without cropping
                         elif key == 27:
                              break
                    cv2.destroyAllWindows()
               else:
                    contours = detect_edges(sized_image)
                    
                    answer_contours = []
                    
                    for i, contour in enumerate(contours):
                         
                         # precision for approximation
                         # epsilon = 0.01 * cv2.arcLength(contour, True)
                         # approx = cv2.approxPolyDP(contour, epsilon, True)
                         
                         x, y, w, h = cv2.boundingRect(contour)
                         aspect_ratio = w / h
                         
                         if aspect_ratio > 1 and w > 50 and h > 20 and cv2.contourArea(contour) > 100:
                              answer_contours.append(contour)
                              cv2.drawContours(sized_image, [contour], -1, (0,255,0), thickness=1)
                              
                    print(len(answer_contours))
                    cv2.imshow('After Contouring', sized_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

if __name__ == "__main__":
     main(sys.argv[1:])