#coding: utf-8
from __future__ import division

import numpy as np

import cv2
from Kinocto.sudocube.adjustable_parameters import *


class OCR(object):
    def __init__(self):

        samples = np.loadtxt(samples_data, np.float32)
        responses = np.loadtxt(response_data, np.float32)
        responses = responses.reshape((responses.size, 1))

        self.model = cv2.KNearest()
        self.model.train(samples, responses)

    def detect_number(self, hsv_img):
        bgr = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(gray, 255, 0, 1, 5, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        erode = cv2.erode(thresh, kernel, iterations=1)
        dilate = cv2.dilate(erode, kernel, iterations=3)

        #        cv2.imshow("contours", dilate)
        #        cv2.waitKey()

        #        cv2.imshow("contours", thresh)
        #        cv2.waitKey()
        #
        contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #        print "_____________________"
        #        for contour in contours:
        #            [x, y, w, h] = cv2.boundingRect(contour)
        #            area = h * w
        #            ratio = h / w
        #            cv2.rectangle(bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #            print area, ratio
        #
        #        cv2.imshow("contours", bgr)
        #        cv2.waitKey()




        return self._detect_every_number(contours, thresh)

    def _detect_every_number(self, contours, thresh):
        try:
            number = self._detect_number(contours, thresh, ocr_min_area, ocr_max_area, ocr_min_ratio, ocr_max_ratio,
                                         ocr_min_height)
            if number == "1":
                raise NoNumberPresentException
        except NoNumberPresentException:
            number = self._detect_ones(contours, thresh)
        return number

    def _detect_ones(self, contours, thresh):
        number = self._detect_number(contours, thresh, ocr_one_min_area, ocr_one_max_area, ocr_one_min_ratio,
                                     ocr_one_max_ratio, ocr_one_min_height)
        if number != "1":
            raise NoNumberPresentException
        return number

    def _detect_number(self, contours, thresh_img, min_area, max_area, min_ratio, max_ratio, min_height):
        contour = self._find_contour_with_biggest_area_within_limits(contours, min_area, max_area, min_ratio, max_ratio,
                                                                     min_height)
        #contour = self._find_contour_with_biggest_area_within_limits_and_print(contours, min_area, max_area, min_ratio, max_ratio, min_height, thresh_img) #DEBUG
        string = self._find_number_in_contour(contour, thresh_img)
        #string = self._find_number_in_contour_and_print(contour, thresh_img, thresh_img) #DEBUG
        return string

    def _find_number_in_contour(self, contour, thresh):

    #        cv2.imshow("Finding number", thresh)
    #        cv2.waitKey()

        [x, y, w, h] = cv2.boundingRect(contour)
        roi = thresh[y:y + h, x:x + w]
        roismall = cv2.resize(roi, (10, 10))
        roismall = roismall.reshape((1, 100))
        roismall = np.float32(roismall)
        retval, results, neigh_resp, dists = self.model.find_nearest(roismall, k=1)
        number = str(int((results[0][0])))

        #print "Number:", number

        return number

    #DEBUG ONLY
    def _find_number_in_contour_and_print(self, contour, im, thresh):
        out = np.zeros(im.shape, np.uint8)
        [x, y, w, h] = cv2.boundingRect(contour)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = thresh[y:y + h, x:x + w]
        roismall = cv2.resize(roi, (10, 10))
        roismall = roismall.reshape((1, 100))
        roismall = np.float32(roismall)
        retval, results, neigh_resp, dists = self.model.find_nearest(roismall, k=1)
        string = str(int((results[0][0])))
        cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))

        cv2.imshow("ocr", im)
        cv2.waitKey()

        print string

        return string

    def _find_contour_with_biggest_area_within_limits(self, contours, minimum, maximum, min_ratio, max_ratio,
                                                      min_height):

        biggest_area_contour = {"area": 0, "contour": None}

        for contour in contours:
            [_, _, w, h] = cv2.boundingRect(contour)
            area = h * w
            ratio = h / w
            if area > biggest_area_contour[
                "area"] and minimum < area < maximum and min_ratio < ratio < max_ratio and h > min_height:
                biggest_area_contour = {"area": area, "contour": contour}
        if biggest_area_contour["contour"] is None:
            raise NoNumberPresentException()

        return biggest_area_contour["contour"]

    #DEBUG ONLY
    def _find_contour_with_biggest_area_within_limits_and_print(self, contours, minimum, maximum, min_ratio, max_ratio,
                                                                min_height,
                                                                im):
        print "++++++++"
        biggest_area_contour = {"area": 0, "contour": None}
        image_copy = im.copy()
        for contour in contours:
            [x, y, w, h] = cv2.boundingRect(contour)
            area = h * w
            ratio = h / w
            print area, ratio
            if minimum < area < maximum and min_ratio < ratio < max_ratio and h > min_height:
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (255, 255, 255), 2)
                print area, ratio

            if area > biggest_area_contour["area"] and minimum < area < maximum and min_ratio < ratio < max_ratio:
                biggest_area_contour = {"area": area, "contour": contour}

        cv2.imshow("", image_copy)
        cv2.waitKey()

        if biggest_area_contour["contour"] is None:
            raise NoNumberPresentException()

        return biggest_area_contour["contour"]


class NoNumberPresentException(Exception):
    def __init__(self, value=""):
        Exception.__init__(self)
        self.value = value