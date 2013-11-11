#coding: utf-8

import unittest
from mock import MagicMock
from Kinocto.sudocube.sudocube_decoder import SudocubeDecoder


class TestSudocubeDecoder(unittest.TestCase):
    def setUp(self):
        self._image = "AN IMAGE"
        self._sudocube_mock = MagicMock(name="sudocube")
        self._sudocube_factory_mock = MagicMock(name="sudocube_factory")

        self._sudocube_factory_mock.create_sudocube_from_image.return_value = self._sudocube_mock

        self._sudocube_decoder = SudocubeDecoder()
        self._sudocube_decoder._init_dependencies = self._fake_init_dependencies(self._sudocube_decoder,
                                                                                 self._sudocube_factory_mock)
        self._solved_sudocube = self._sudocube_decoder.compute_solved_sudocube_and_digit_to_draw(self._image)

    def test_should_create_sudocube_with_factory(self):
        self._sudocube_factory_mock.create_sudocube_from_image.assert_called_once_with(self._image)

    def test_should_tell_sudocube_to_solve_itself(self):
        self._sudocube_mock.solve.assert_called_once_with()

    def test_should_return_solved_sudocube(self):
        self.assertEqual(self._sudocube_mock, self._solved_sudocube)

    #Monkey patch to mock dependencies
    def _fake_init_dependencies(self, sudocube_decoder, sudocube_factory):
        sudocube_decoder._sudocube_factory = sudocube_factory