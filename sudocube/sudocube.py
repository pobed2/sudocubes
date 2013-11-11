#!/usr/bin/env python
# -*- coding: utf-8 -*-

from adjustable_parameters import red_square
from adjustable_parameters import top_face, front_face, side_face
from sudocube_solving.norvig_solver import NorvigSolver


class Sudocube(object):
    def __init__(self, data):
        self._data = data
        self._solved = False
        self._init_dependencies()

    def _init_dependencies(self):
        self._solver = NorvigSolver()

    def __hash__(self):
        return hash((tuple(self.get_sudocube_list()), self.get_red_square_index()))

    def __eq__(self, other):
        return (tuple(self.get_sudocube_list()), self.get_red_square_index()) == (
            tuple(other.get_sudocube_list()), other.get_red_square_index())

    def solve(self):
        if not self._solved:
            self._solved_data = self._solver.solve_sudocube(self._data)
            self._digit = self._find_digit_to_draw()
            self._solved = True

    def _find_digit_to_draw(self):
        face, number = self._data[red_square]
        digit = self._solved_data[face][number]
        return digit

    def get_digit_to_draw(self):
        self.solve()
        return int(self._digit)

    def get_solved_data(self):
        self.solve()
        return self._solved_data

    def get_sudocube_list(self):
        sudocube_list = list()
        for number in self._solved_data[top_face]:
            sudocube_list.append(number)
        for number in self._solved_data[front_face]:
            sudocube_list.append(number)
        for number in self._solved_data[side_face]:
            sudocube_list.append(number)
        return sudocube_list

    def get_red_square_index(self):
        face, number = self._data[red_square]
        if face == top_face:
            return number
        elif face == front_face:
            return number + 16
        else:
            return number + 32

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()

    def _to_string(self):
        string = ""

        data = self._solved_data[top_face]
        for i in range(0, len(data), 4):
            string = string + data[i] + " " + data[i + 1] + " " + data[i + 2] + " " + data[i + 3] + "\n"

        front = self._solved_data[front_face]
        side = self._solved_data[side_face]

        for i in range(0, len(front), 4):
            string = string + front[i] + " " + front[i + 1] + " " + front[i + 2] + " " + front[i + 3] + " " + \
                     side[i] + " " + side[i + 1] + " " + side[i + 2] + " " + side[i + 3] + "\n"

        string = string + "Carré Rouge: " + self._digit

        return string