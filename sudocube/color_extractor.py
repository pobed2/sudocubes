#coding: utf-8
import cv2
from Kinocto.sudocube.adjustable_parameters import BLUE, GREEN, RED


class ColorExtractor(object):
    def extract_blue(self, img):
        return self._find_color_in_image(img, *BLUE)

    def extract_green(self, img):
        return self._find_color_in_image(img, *GREEN)

    def extract_red(self, img):
        return self._find_color_in_image(img, *RED)

    def _find_color_in_image(self, hsv_img, hsv_color_min, hsv_color_max):
        return cv2.inRange(hsv_img, hsv_color_min, hsv_color_max)