#coding: utf-8

import unittest

from mock import MagicMock, patch

import cv2
from Kinocto.sudocube.sudocube_factory import SudocubeFactory


class TestSudocubeFactory(unittest.TestCase):
    @patch('cv2.GaussianBlur')
    @patch('cv2.cvtColor')
    def setUp(self, cv2_cvtColor_mock, cv2_GaussianBlur_mock):
        #Constants
        self._image = "AN IMAGE"
        self._hsv_image = "AN HSV IMAGE"
        self._smooth_image = "SMOOTH IMAGE"
        self._unwarped_image = "UNWARPED IMAGE"
        self._sudocube_frame = "SUDOCUBE FRAME"
        self._green_frame = "GREEN FRAME"
        self._corners = "CORNERS"

        #Mocks
        self._cv2_cvtColor_mock = cv2_cvtColor_mock
        self._cv2_GaussianBlur_mock = cv2_GaussianBlur_mock
        self._corner_finder_mock = MagicMock(name="corner_finder")
        self._data_extractor_mock = MagicMock(name="data_extractor")
        self._unwarper_mock = MagicMock(name="unwarper")
        self._color_extractor_mock = MagicMock(name="color_extractor")

        #Return value changes
        self._cv2_cvtColor_mock.return_value = self._hsv_image
        self._cv2_GaussianBlur_mock.return_value = self._smooth_image
        self._corner_finder_mock.find_corners.return_value = self._corners
        self._unwarper_mock.unwarp.return_value = self._unwarped_image
        self._color_extractor_mock.extract_blue.return_value = self._sudocube_frame
        self._color_extractor_mock.extract_green.return_value = self._green_frame

        #Object creation
        self._sudocube_factory = SudocubeFactory()
        self._sudocube_factory._init_dependencies = self._fake_init_dependencies(self._sudocube_factory,
                                                                                 self._corner_finder_mock,
                                                                                 self._data_extractor_mock,
                                                                                 self._unwarper_mock,
                                                                                 self._color_extractor_mock)

        #Execution
        self._sudocube_factory.create_sudocube_from_image(self._image)

    def test_should_convert_image_to_hsv(self):
        self._cv2_cvtColor_mock.assert_called_once_with(self._image, cv2.COLOR_RGB2HSV)

    def test_should_find_frame_of_sudocube_by_taking_only_its_color(self):
        self._color_extractor_mock.extract_blue.assert_called_once_with(self._unwarped_image)

    def test_should_tell_corner_finder_to_find_outside_corners_of_sudocube(self):
        self._corner_finder_mock.find_corners.assert_called_once_with(self._sudocube_frame)

    def test_should_tell_sudocube_data_extractor_to_find_data_from_image_and_corner_positions(self):
        self._data_extractor_mock.extract_data_from_image_with_corner_info.assert_called_once_with(self._unwarped_image,
                                                                                                   self._corners)

        #Monkey patch to mock dependencies

    def _fake_init_dependencies(self, sudocube_factory, corner_finder, data_extractor, unwarper, color_extractor):
        sudocube_factory._corner_finder = corner_finder
        sudocube_factory._data_extractor = data_extractor
        sudocube_factory._unwarper = unwarper
        sudocube_factory._color_extractor = color_extractor