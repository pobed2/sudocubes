#coding: utf-8
from __future__ import division
from math import sqrt, atan2, cos, sin

import numpy as np

from Kinocto.sudocube.adjustable_parameters import *
from Kinocto.sudocube.color_extractor import ColorExtractor
from Kinocto.sudocube.face_extraction.red_square_detector import RedSquareDetector
from Kinocto.sudocube.ocr import OCR, NoNumberPresentException


class FaceExtractor(object):
    def __init__(self):
        self._ocr = OCR()
        self._red_square_detector = RedSquareDetector()
        self._color_extractor = ColorExtractor()

    def extract_data(self, img, corners):
        self._define_corners(corners)
        self._img = img
        self._red_img = self._get_image_for_red_square(img)
        self._red_square_position = None

        x_angle, y_angle, delta_x, delta_y = self._calculate_face_coordinates()
        face_data = self._find_face_data(x_angle, y_angle, delta_x, delta_y)

        return face_data, self._red_square_position

    def _get_image_for_red_square(self, img):
        return self._color_extractor.extract_red(img)

    def _define_corners(self, corners):
        self._top_left = corners["tl"]
        self._top_right = corners["tr"]
        self._bottom_left = corners["bl"]
        self._bottom_right = corners["br"]

    def _calculate_face_coordinates(self):
        #Calculate the deltas of a single square of top, bottom, right and left sides
        top_lenght_single = self._calculate_distance(self._top_right, self._top_left) / 4
        bottom_lenght_single = self._calculate_distance(self._bottom_right, self._bottom_left) / 4
        right_lenght_single = self._calculate_distance(self._bottom_right, self._top_right) / 4
        left_lenght_single = self._calculate_distance(self._bottom_left, self._top_left) / 4

        #Calculate the average angle from the x axis
        top_angle = atan2(self._top_right[1] - self._top_left[1], self._top_right[0] - self._top_left[0])
        bottom_angle = atan2(self._bottom_right[1] - self._bottom_left[1], self._bottom_right[0] - self._bottom_left[0])
        x_angle = self.avg((top_angle, bottom_angle))

        #Calculate the average angle from the y axis
        left_angle = atan2(self._bottom_left[1] - self._top_left[1], self._bottom_left[0] - self._top_left[0])
        right_angle = atan2(self._bottom_right[1] - self._top_right[1], self._bottom_right[0] - self._top_right[0])
        y_angle = self.avg((left_angle, right_angle))

        #Calculate the average width and height of a single square
        single_width = self.avg((top_lenght_single, bottom_lenght_single))
        single_height = self.avg((right_lenght_single, left_lenght_single))

        return x_angle, y_angle, single_width, single_height

    def _find_face_data(self, x_angle, y_angle, delta_x, delta_y):
        data = []
        for row_number in range(NB_OF_ROWS):
            top_left_corner_of_row = self._top_left + row_number * np.array(
                [delta_x * cos(y_angle), delta_y * sin(y_angle)]) #Move down one row

            for col_number in range(NB_OF_COLUMNS):
                corners = self._get_square_corners(delta_x, delta_y, top_left_corner_of_row, col_number, x_angle,
                                                   y_angle)
                x_cutoffs, y_cutoffs = self._calculate_cutoffs(*corners)

                square = self._img[y_cutoffs[0]:y_cutoffs[1], x_cutoffs[0]:x_cutoffs[1]]

                #print "Corners:", corners
                #print"Cutoffs:", row_number, col_number, y_cutoffs[0], y_cutoffs[1], x_cutoffs[0], x_cutoffs[1]

                red_image_square = self._red_img[y_cutoffs[0]:y_cutoffs[1], x_cutoffs[0]:x_cutoffs[1]]
                if self._red_square_detector.is_red_square(red_image_square):
                    self._red_square_position = (row_number * 4 + col_number)

                #                cv2.imshow("square", square)
                #                cv2.waitKey()

                digit = self._find_digit_in_square(square)
                data.append(digit)

        return data

    def _get_square_corners(self, delta_x, delta_y, top_left_corner_of_row, col_number, x_angle, y_angle):
        top_left_corner = top_left_corner_of_row + col_number * np.array(
            [delta_x * cos(x_angle), delta_y * sin(x_angle)])
        top_right_corner = top_left_corner + np.array([delta_x * cos(x_angle), delta_y * sin(x_angle)])
        bottom_left_corner = top_left_corner + np.array([delta_x * cos(y_angle), delta_y * sin(y_angle)])
        bottom_right_corner = bottom_left_corner + np.array([delta_x * cos(x_angle), delta_y * sin(x_angle)])
        return top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner

    def _find_digit_in_square(self, square):
        try:
            number = self._ocr.detect_number(square)
            return number
        except NoNumberPresentException:
            return None

    def _calculate_distance(self, first, second):
        return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)

    def avg(self, array):
        return sum(array) / len(array)