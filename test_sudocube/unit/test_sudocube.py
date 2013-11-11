#coding: utf-8

import unittest
from mock import MagicMock
from Kinocto.sudocube.adjustable_parameters import front_face, side_face, top_face, red_square
from Kinocto.sudocube.sudocube import Sudocube


class TestSudocube(unittest.TestCase):
    def setUp(self):
        self._data = {front_face: [1, None, 3, None], side_face: [None, 6, None, 8], top_face: [None, None, None, 8],
                      red_square: (front_face, 2)}
        self._solved_data = {front_face: [1, 2, 3, 4], side_face: [5, 6, 7, 8], top_face: [9, 1, 2, 8]}
        self._expected_digit = 3

        self._sudocube_solver_mock = MagicMock()
        self._sudocube_solver_mock.solve_sudocube.return_value = self._solved_data

        self._sudocube = Sudocube(self._data)
        self._sudocube._init_dependencies = self._fake_init_dependencies(self._sudocube, self._sudocube_solver_mock)


    def test_should_tell_sudocube_solver_to_solve_if_not_already_solved(self):
        self._sudocube.solve()
        self._sudocube_solver_mock.solve_sudocube.assert_called_once_with(self._data)

    def test_should_call_solver_when_getting_digit(self):
        self._sudocube.get_digit_to_draw()
        self._sudocube_solver_mock.solve_sudocube.assert_called_once_with(self._data)

    def test_should_return_right_digit_when_getting_digit(self):
        digit = self._sudocube.get_digit_to_draw()
        self.assertEqual(self._expected_digit, digit)

    def test_should_call_solver_when_getting_solved_data(self):
        self._sudocube.get_digit_to_draw()
        self._sudocube_solver_mock.solve_sudocube.assert_called_once_with(self._data)

    def test_should_return_right_solved_data(self):
        solved_sudocube = self._sudocube.get_solved_data()
        self.assertEqual(self._solved_data, solved_sudocube)

    def _fake_init_dependencies(self, sudocube, solver):
        sudocube._solver = solver
