#coding: utf-8
import cv2
from corner_finder import CornerFinder
from sudocube import Sudocube
from color_extractor import ColorExtractor
from warp_adjustement.unwarper import Unwarper
from sudocube_data_extractor import SudocubeDataExtractor


class SudocubeFactory(object):
    def __init__(self):
        self._init_dependencies()

    def _init_dependencies(self):
        self._corner_finder = CornerFinder()
        self._data_extractor = SudocubeDataExtractor()
        self._unwarper = Unwarper()
        self._color_extractor = ColorExtractor()

    def create_sudocube_from_image(self, bgr_img):
        hsv_img = self._convert_bgr_image_to_hsv(bgr_img)
        smooth_img = self._smooth_image(hsv_img)
        smooth_img = cv2.GaussianBlur(smooth_img, (9, 9), 0.5)

        unwarped_img = self._unwarp_image(smooth_img)
        sudocube_corners = self._find_corners(unwarped_img)

        sudocube_data = self._data_extractor.extract_data_from_image_with_corner_info(unwarped_img, sudocube_corners)
        sudocube = Sudocube(sudocube_data)

        return sudocube

    def _unwarp_image(self, img):
        green_frame = self._find_green_frame_around_sudoku(img)
        unwarped_img = self._unwarper.unwarp(green_frame, img)

        return unwarped_img

    def _find_corners(self, img):
        sudocube_frame = self._find_sudocube_frame(img)

        sudocube_corners = self._corner_finder.find_corners(sudocube_frame)
        return sudocube_corners

    def _convert_bgr_image_to_hsv(self, bgr_img):
        return cv2.cvtColor(bgr_img, cv2.COLOR_RGB2HSV)

    def _smooth_image(self, img):
        return cv2.GaussianBlur(img, (5, 5), 0.50)

    def _find_sudocube_frame(self, img):
        return self._color_extractor.extract_blue(img)

    def _find_green_frame_around_sudoku(self, img):
        return self._color_extractor.extract_green(img)