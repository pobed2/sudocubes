#coding: utf-8

import os

import numpy as np

import ocr_training


IMAGE_SIZE = (480, 640)

NB_OF_ROWS = 4
NB_OF_COLUMNS = 4

samples_data = os.path.dirname(ocr_training.__file__) + '/trained_data/generalsamples.data'
response_data = os.path.dirname(ocr_training.__file__) + '/trained_data/generalresponses.data'

ocr_min_area = 500
ocr_max_area = 800
ocr_min_ratio = 1.5
ocr_max_ratio = 2.5
ocr_min_height = 30

#OCR bounding boxes area for
#detecting '1' only
ocr_one_min_area = 250
ocr_one_max_area = 600
ocr_one_min_ratio = 2.25
ocr_one_max_ratio = 4.5
ocr_one_min_height = 25


#ColorExtractor
BLUE = (np.array([5, 100, 50], np.uint8), np.array([40, 255, 255], np.uint8))
GREEN = (np.array([45, 100, 50], np.uint8), np.array([70, 255, 255], np.uint8))
RED = (np.array([100, 100, 50], np.uint8), np.array([150, 255, 255], np.uint8))

front_face = "front"
side_face = "side"
top_face = "top"
red_square = "red square"