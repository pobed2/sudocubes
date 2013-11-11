#coding: utf-8
from __future__ import division

import numpy as np
from numpy import array, float32

import cv2


class CornerFinder(object):
    def find_corners(self, img):

        self.MIN_AREA_CORNER_DETECTION = 300
        self.LEFT_THIRD = img.shape[1] / 3
        self.MIDDLE_THIRD = 2 * img.shape[1] / 3
        self.RIGHT_THIRD = img.shape[1]

        self.img = img
        #corners = np.vstack(tuple(cv2.goodFeaturesToTrack(self.img, 150, 0.01, 10)))
        #outside_corners = self._get_outside_corners(corners)

        hard_coded_corners = {
            'front': {'bl': array([36., 514.], dtype=float32), 'tl': array([40., 214.], dtype=float32),
                      'tr': array([250., 292.], dtype=float32), 'br': array([252., 592.], dtype=float32)},
            'top': {'bl': array([40., 214.], dtype=float32), 'tl': array([228., 48.], dtype=float32),
                    'tr': array([441., 127.], dtype=float32), 'br': array([250., 292.], dtype=float32)},
            'side': {'bl': array([252., 592.], dtype=float32), 'tl': array([250., 292.], dtype=float32),
                     'tr': array([441., 127.], dtype=float32), 'br': array([446., 427.], dtype=float32)}}

        #self._draw_circles_around_points(self.img, outside_corners) #DEBUG
        #self._draw_circles_around_points(self.img, hard_coded_corners) #DEBUG

        return hard_coded_corners

    #DEBUG ONLY
    def _draw_circles_around_points(self, img, points):
        try:
            for face, face_value in points.iteritems():
                for key, value in face_value.iteritems():
                    cv2.circle(img, tuple(value), 10, (255, 255, 0))
        except AttributeError:
            for point in points:
                cv2.circle(img, tuple(point), 10, (255, 255, 0))
        finally:
            cv2.imshow("im", img)
            cv2.waitKey()

    def _get_outside_corners(self, corners):
        left_corners = self._find_left_corners(corners)
        middle_corners = self._find_middle_corners(corners)
        right_corners = self._find_right_corners(corners)

        face_corners = {"tl": left_corners["face-top-left"], "tr": middle_corners["face-top-right"],
                        "bl": left_corners["face-bottom-left"], "br": middle_corners["face-bottom-right"]}
        side_corners = {"tl": middle_corners["face-top-right"], "tr": right_corners["side-top"],
                        "bl": middle_corners["face-bottom-right"], "br": right_corners["side-bottom"]}
        top_corners = {"tl": middle_corners["rooftop"], "tr": right_corners["side-top"],
                       "bl": left_corners["face-top-left"], "br": middle_corners["face-top-right"]}

        return {"front": face_corners, "side": side_corners, "top": top_corners}

    def _find_middle_corners(self, corners):
        possible_corners = self._find_possible_corners(corners, self.LEFT_THIRD, self.MIDDLE_THIRD)

        #Find top corner
        top = np.argmin(possible_corners, axis=0)[0]
        top_corner = possible_corners[top]
        possible_corners.pop(top)

        #Find possible middle corner and real bottom corner
        middle_corner, bottom_corner = self._find_top_and_bottom_corner(possible_corners)

        #finding real middle corner
        delta_x = (bottom_corner[0] - middle_corner[0]) / 2
        delta_y = (bottom_corner[1] - middle_corner[1]) / 2

        possible_middle = (middle_corner[0] + delta_x, middle_corner[1] + delta_y)
        tolerance = 30.0

        the_corners = []
        for corner in possible_corners:
            if possible_middle[0] + tolerance > corner[0] > possible_middle[0] - tolerance and possible_middle[
                1] + tolerance > corner[1] > possible_middle[1] - tolerance:
                the_corners.append(corner)

        #Middle corner should be highest corner in the corners
        minimum = {"corner": None, "y-value": float('inf')}
        for corner in the_corners:
            if corner[1] < minimum["y-value"]:
                minimum = {"corner": corner, "y-value": corner[1]}

        return {"rooftop": middle_corner, "face-top-right": minimum["corner"], "face-bottom-right": bottom_corner}

    def _find_left_corners(self, corners):
        possible_corners = self._find_possible_corners(corners, 0, self.LEFT_THIRD)

        x_least = float('inf')
        for corner in possible_corners:
            if corner[0] < x_least:
                x_least = corner[0]

        the_corners = []
        tolerance = 20.0
        for corner in possible_corners:
            if x_least + tolerance > corner[0] > x_least - tolerance:
                the_corners.append(corner)

        x_sum = 0
        for corner in the_corners:
            x_sum += corner[0]
        x_avg = x_sum / len(the_corners)

        corn = []
        tolerance = 5
        for corner in the_corners:
            if x_avg + tolerance > corner[0] > x_avg - tolerance:
                corn.append(corner)

        top_corner, bottom_corner = self._find_top_and_bottom_corner(corn)
        return {"face-top-left": top_corner, "face-bottom-left": bottom_corner}

    def _find_right_corners(self, corners):
        possible_corners = self._find_possible_corners(corners, self.MIDDLE_THIRD, self.RIGHT_THIRD)

        x_max = 0
        for corner in possible_corners:
            if corner[0] > x_max:
                x_max = corner[0]

        the_corners = []
        tolerance = 20.0
        for corner in possible_corners:
            if x_max + tolerance > corner[0] > x_max - tolerance:
                the_corners.append(corner)

        x_sum = 0
        for corner in the_corners:
            x_sum += corner[0]
        x_avg = x_sum / len(the_corners)

        corn = []
        tolerance = 5.0
        for corner in the_corners:
            if x_avg + tolerance > corner[0] > x_avg - tolerance:
                corn.append(corner)

        top_corner, bottom_corner = self._find_top_and_bottom_corner(corn)
        return {"side-top": top_corner, "side-bottom": bottom_corner}

    def _find_possible_corners(self, corners, left_limit, right_limit):
        possible_corners = []
        for corner in corners:
            if left_limit <= corner[0] < right_limit:
                possible_corners.append(corner)

        return possible_corners

    def _find_top_and_bottom_corner(self, corners):
        top = np.argmin(corners, axis=0)[1]
        bottom = np.argmax(corners, axis=0)[1]
        return corners[top], corners[bottom]