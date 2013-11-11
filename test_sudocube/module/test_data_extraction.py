#coding: utf-8
import unittest

import cv2

from Kinocto.sudocube.sudocube_factory import SudocubeFactory
from Kinocto.test.test_sudocube.test_images.test_images_parameters import *


class ModuleTestDataExtraction(unittest.TestCase):
    def setUp(self):
        self._sudocube_factory = SudocubeFactory()

    def test_should_detect_right_numbers_in_front_facing_image(self):
        image = self._read_image(first_front_image_path)
        sudocube = self._sudocube_factory.create_sudocube_from_image(image)

        expected = first_front_image_expected
        self._assert_same_unsolved_sudocube(expected, sudocube)


    def test_should_detect_right_numbers_in_another_front_facing_image(self):
        image = self._read_image(second_front_image_path)
        sudocube = self._sudocube_factory.create_sudocube_from_image(image)

        expected = second_front_image_expected
        self._assert_same_unsolved_sudocube(expected, sudocube)

    def _assert_same_unsolved_sudocube(self, expected, given):
        data = given._data
        self.assertEqual(expected["front"], data["front"])
        self.assertEqual(expected["side"], data["side"])
        self.assertEqual(expected["top"], data["top"])
        self.assertEqual(expected["red square"], data["red square"])

    def _read_image(self, path):
        rgb = cv2.imread(path)
        return rgb