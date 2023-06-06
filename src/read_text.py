from dotenv import dotenv_values
from google.cloud import vision
import pandas as pd

import sys
import os
import io

from helpers import get_images

config = dotenv_values(".env")
TEXT_IMG_DIR = "./data/text/"

dir = "paper_2"

images = get_images(os.path.join(TEXT_IMG_DIR, dir))

     # instantiate google client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'../env/service_account.json'
client = vision.ImageAnnotatorClient()

for image in images:
     print(image)
     with io.open(image, "rb") as image_file:
          content = image_file.read()
     image = vision.Image(content=content)
     response = client.document_text_detection(image=image)
     text = response.full_text_annotation.text
     print(text)
          
     pages = response.full_text_annotation.pages
          
     # for page in pages:
     #      for block in page.blocks:
     #           print(f'block confidence: {block.confidence}')
     #           for paragraph in block.paragraph:
     #                print(f"paragraph confidence: {paragraph.confidence}")
     #                for word in paragraph.words:
     #                     word_text = ''.join([symbol.text for symbol in word.symbols])
     #                     print(f"word text: {word_text} confidence: {word.confidence}")
     #                     for symbol in word.symbols:
     #                          print(f"symbol: {symbol.text} confidence: {symbol.confidence}")