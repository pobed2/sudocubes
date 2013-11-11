#coding: utf-8

import numpy as numpy
import cv2
from Kinocto.sudocube.adjustable_parameters import IMAGE_SIZE


class Unwarper(object):
    def __init__(self):
        self._destination_corners = self._init_destination_corners(*IMAGE_SIZE)

    def unwarp(self, green_frame_img, img):

    #        resized = cv2.resize(green_frame_img, (640, 480))
    #        cv2.imshow("green frame", resized)
    #        cv2.waitKey()
        corners = self._find_green_frame_corners(green_frame_img)

        transform = cv2.getPerspectiveTransform(corners, self._destination_corners)

        unwarped = cv2.warpPerspective(img, transform, IMAGE_SIZE)

        #cv2.imwrite("images/unwarped5.jpg", unwarped)

        return unwarped

    def _init_destination_corners(self, width, height):
        return numpy.array([[0, 0], [width, 0], [width, height], [0, height]], numpy.float32)

    def _find_green_frame_corners(self, green_frame_img):
        contours, h = cv2.findContours(green_frame_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        corners = self._find_corners_for_biggest_contour(contours)
        return corners

    def _find_corners_for_biggest_contour(self, contours):
        biggest_area_contour = {"area": 0, "corners": None}
        for i in contours:
            area = cv2.contourArea(i)
            if area > biggest_area_contour["area"]:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                biggest_area_contour = {"area": area, "corners": approx}

        corners = self._put_vertices_in_clockwise_order(biggest_area_contour["corners"])
        return corners

    def _put_vertices_in_clockwise_order(self, vertices):
        vertices = vertices.reshape((4, 2))
        ordered = numpy.zeros((4, 2), dtype=numpy.float32)

        add = vertices.sum(1)
        ordered[0] = vertices[numpy.argmin(add)]
        ordered[2] = vertices[numpy.argmax(add)]

        diff = numpy.diff(vertices, axis=1)
        ordered[1] = vertices[numpy.argmin(diff)]
        ordered[3] = vertices[numpy.argmax(diff)]

        return ordered
