#coding: utf-8

import unittest
from mock import patch
from Kinocto.sudocube.adjustable_parameters import BLUE, GREEN
from Kinocto.sudocube.color_extractor import ColorExtractor


class TestColorExtractor(unittest.TestCase):
    def setUp(self):
        self._img = "AN IMAGE"
        self._color_extractor = ColorExtractor()

    @patch('cv2.inRange')
    def test_should_find_img_in_range_of_hsv_blue_when_extracting_blue(self, cv2_inRange_mock):
        self._color_extractor.extract_blue(self._img)

        cv2_inRange_mock.assert_called_once_with(self._img, *BLUE)

    @patch('cv2.inRange')
    def test_should_find_img_in_range_of_hsv_blue_when_extracting_green(self, cv2_inRange_mock):
        self._color_extractor.extract_green(self._img)

        cv2_inRange_mock.assert_called_once_with(self._img, *GREEN)
