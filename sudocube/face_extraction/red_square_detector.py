#coding: utf-8

import cv2


class RedSquareDetector(object):
    def is_red_square(self, img):
        return (cv2.countNonZero(img) / len(img)) > 20