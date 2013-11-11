#coding: utf-8

import unittest
from Kinocto.sudocube.sudocube_solving.norvig_solver import NorvigSolver


class ModuleTestSolving(unittest.TestCase):
    def setUp(self):
        self.solver = NorvigSolver()

    def test_should_solve_a_sudocube(self):
        grid = {'front': [None, None, None, '7', None, None, '5', None, '2', None, None, '6', None, '7', None, None],
                'top': [None, None, None, '8', None, '1', None, None, None, None, None, None, '3', None, None, '5'],
                'side': ['6', None, None, None, None, '7', None, None, '4', None, None, '1', None, None, '2', None],
                'red square': ('front', 0)}

        expected = {'front': ['1', '3', '8', '7', '4', '6', '5', '2', '2', '8', '3', '6', '5', '7', '1', '4'],
                    'top': ['7', '5', '2', '8', '6', '1', '4', '3', '8', '4', '6', '1', '3', '2', '7', '5'],
                    'side': ['6', '2', '5', '4', '1', '7', '8', '3', '4', '5', '7', '1', '8', '3', '2', '6']}

        solved = self.solver.solve_sudocube(grid)

        self.assertEqual(expected, solved)