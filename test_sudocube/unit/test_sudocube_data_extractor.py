#coding: utf-8

import unittest

from mock import MagicMock
from Kinocto.sudocube.adjustable_parameters import front_face, side_face, top_face, red_square
from Kinocto.sudocube.sudocube_data_extractor import SudocubeDataExtractor


class TestSudocubeDataExtractor(unittest.TestCase):
    def setUp(self):
        #Constants
        self._image = "IMAGE"
        self._corners = {front_face: [1, 2, 3, 4], side_face: [5, 6, 7, 8], top_face: [9, 10, 11, 12]}
        self._face = [7, None, 7, None]
        self._side = [None, None, 10, 4]
        self._top = [1, None, None, None]
        self._red_square = (front_face, 2)
        self._expected_data = {front_face: self._face, side_face: self._side, top_face: self._top,
                               red_square: self._red_square}

        #Mocks
        self._front_face_extractor = MagicMock()
        self._side_face_extractor = MagicMock()
        self._top_face_extractor = MagicMock()

        #Mocks return values
        self._front_face_extractor.extract_data.return_value = self._face, 2
        self._side_face_extractor.extract_data.return_value = self._side, None
        self._top_face_extractor.extract_data.return_value = self._top, None

        #Actual operations
        self._data_extractor = SudocubeDataExtractor()
        self._data_extractor._init_dependencies = self._fake_init_dependencies(self._data_extractor,
                                                                               self._front_face_extractor,
                                                                               self._side_face_extractor,
                                                                               self._top_face_extractor)
        self._data = self._data_extractor.extract_data_from_image_with_corner_info(self._image, self._corners)

    def test_should_tell_front_extractor_to_extract_data(self):
        self._front_face_extractor.extract_data.assert_called_once_with(self._image, self._corners[front_face])

    def test_should_tell_side_extractor_to_extract_data(self):
        self._side_face_extractor.extract_data.assert_called_once_with(self._image, self._corners[side_face])

    def test_should_tell_top_extractor_to_extract_data(self):
        self._top_face_extractor.extract_data.assert_called_once_with(self._image, self._corners[top_face])

    def test_should_return_data_as_dictionnary_of_data_and_red_square_position(self):
        self.assertEqual(self._expected_data, self._data)

    #Monkey patch to mock dependencies
    def _fake_init_dependencies(self, data_extractor, front_extractor, side_extractor, top_extractor):
        data_extractor._front_extractor = front_extractor
        data_extractor._side_extractor = side_extractor
        data_extractor._top_extractor = top_extractor