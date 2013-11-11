#coding: utf-8

import unittest
from Kinocto.sudocube.face_extraction.front_face_extractor import FrontFaceExtractor
from Kinocto.sudocube.face_extraction.side_face_extractor import SideFaceExtractor
from Kinocto.sudocube.face_extraction.top_face_extractor import TopFaceExtractor


class TestFrontFaceExtractor(unittest.TestCase):
    def setUp(self):
        self._top_left_corner = [1, 2]
        self._top_right_corner = [3, 4]
        self._bottom_left_corner = [5, 6]
        self._bottom_right_corner = [7, 8]

        self._face_extractor = FrontFaceExtractor()
        self.x_cutoffs, self.y_cutoffs = self._face_extractor._calculate_cutoffs(self._top_left_corner,
                                                                                 self._top_right_corner,
                                                                                 self._bottom_left_corner,
                                                                                 self._bottom_right_corner)

    def test_should_return_right_x_and_y_axis_cutoffs(self):
        self.assertEqual(self.x_cutoffs, (1, 7))
        self.assertEqual(self.y_cutoffs, (2, 8))


class TestSideFaceExtractor(unittest.TestCase):
    def setUp(self):
        self._top_left_corner = [1, 2]
        self._top_right_corner = [3, 4]
        self._bottom_left_corner = [5, 6]
        self._bottom_right_corner = [7, 8]

        self._face_extractor = SideFaceExtractor()
        self.x_cutoffs, self.y_cutoffs = self._face_extractor._calculate_cutoffs(self._top_left_corner,
                                                                                 self._top_right_corner,
                                                                                 self._bottom_left_corner,
                                                                                 self._bottom_right_corner)

    def test_should_return_right_x_and_y_axis_cutoffs(self):
        self.assertEqual(self.x_cutoffs, (5, 3))
        self.assertEqual(self.y_cutoffs, (4 + 25, 6))


class TestTopFaceExtractor(unittest.TestCase):
    def setUp(self):
        self._top_left_corner = [1, 2]
        self._top_right_corner = [3, 4]
        self._bottom_left_corner = [5, 6]
        self._bottom_right_corner = [7, 8]

        self._face_extractor = TopFaceExtractor()
        self.x_cutoffs, self.y_cutoffs = self._face_extractor._calculate_cutoffs(self._top_left_corner,
                                                                                 self._top_right_corner,
                                                                                 self._bottom_left_corner,
                                                                                 self._bottom_right_corner)

    def test_should_return_right_x_and_y_axis_cutoffs(self):
        self.assertEqual(self.x_cutoffs, (5 - 10, 3 - 10))
        self.assertEqual(self.y_cutoffs, (2, 8 - 10))