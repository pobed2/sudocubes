#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from math import fabs
from Kinocto.sudocube.sudocube_solving.sudocube_adapter import SudocubeAdapter


class NorvigSolver(object):
    def __init__(self):
        self.digits = '12345678'
        faces = 'ABC'
        face_numbers = range(16)
        self.squares = self._cross(faces, face_numbers)
        self.units = self._get_units(self.squares)
        self.peers = dict((s, set(self.units[s]) - {s}) for s in self.squares)

    def solve_sudocube(self, sudocube_data):
        grid = SudocubeAdapter().get_grid(sudocube_data)
        propagated = self._propagate_constraint(grid)

        solved = self.search(propagated)

        if not solved:
            raise SolvingError('Was not able to solve')

        return SudocubeAdapter().get_solved_dict(solved)

    #Algorithm helper methods
    def _propagate_constraint(self, grid):
        assigned_grid = dict((s, self.digits) for s in self.squares) #Assign all the values to all the squares
        grid_values = self.grid_values(grid) #Values from the grid

        #Assign values from starting grid. Propagating constant
        for square, digit in grid_values.items():
            self.assign(assigned_grid, square, digit)
        return assigned_grid

    def grid_values(self, grid):
        """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
        chars = [c for c in grid if c in self.digits or c in '.']
        return dict(zip(self.squares, chars))

    def assign(self, values, square, digit):
        """Eliminate all the other values (except d) from values[s] and propagate.
        Return values, except return False if a contradiction is detected."""
        if digit != ".":
            other_values = values[square].replace(digit, '') #get values in square that are not the digit
            if all(self.eliminate(values, square, d2) for d2 in other_values):
                return values
            else:
                return False

    def eliminate(self, values, s, d):
        """Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected."""
        if d not in values[s]:
            return values ## Already eliminated
        values[s] = values[s].replace(d, '')
        ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            return False ## Contradiction: removed last value
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all(self.eliminate(values, s2, d2) for s2 in self.peers[s]):
                return False
                ## (2) If a unit u is reduced to only one place for a value d, then put it there.
        dplaces = [s2 for s2 in self.units[s] if d in values[s2]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
            if not self.assign(values, dplaces[0], d):
                return False
        return values

    def search(self, values):
        """Using depth-first search and propagation, try all possible values."""
        if values is False:
            #raise SolvingError("Failed earlier")
            return False
        if all(len(values[s]) == 1 for s in self.squares):
            return values ## Solved!

        ## Chose the unfilled square s with the fewest possibilities
        n, s = min((len(values[s]), s) for s in self.squares if len(values[s]) > 1)
        return self._some(self.search(self.assign(values.copy(), s, d)) for d in values[s])

    def _some(self, seq):
        """Return some element of seq that is true."""
        for e in seq:
            if e:
                return e
        return False

    def _cross(self, A, B):
        """Cross product of elements in A and elements in B."""
        return [str(a) + str(b) for a in A for b in B]

    def _get_units(self, squares):
        units = {}
        for square in squares:
            unit = []
            if 'A' in square:
                digit = int(square.replace('A', ''))
                for other in squares:
                    if 'A' in other:
                        other_digit = int(other.replace('A', ''))
                        if (fabs(other_digit - digit)) % 4 == 0: #This is in the same column
                            unit.append(other)
                        elif digit // 4 == other_digit // 4: #This is the same line
                            unit.append(other)
                        elif digit % 2 == 0: #Column is first column of rectangular group
                            if (fabs(other_digit - digit - 1)) % 4 == 0:#Other column is column to the right
                                unit.append(other)
                        elif digit % 2 == 1: #Column is second column of rectangular group
                            if (fabs(other_digit - digit + 1)) % 4 == 0: #Other column is column to the left
                                unit.append(other)
                    if 'B' in other:
                        other_digit = int(other.replace('B', ''))
                        if (fabs(other_digit - digit)) % 4 == 0: #This is in the same column
                            unit.append(other)
                    if 'C' in other:
                        other_digit = int(other.replace('C', ''))
                        if 0 <= digit <= 3 and other_digit % 4 == 3:
                            unit.append(other)
                        elif 4 <= digit <= 7 and other_digit % 4 == 2:
                            unit.append(other)
                        elif 8 <= digit <= 11 and other_digit % 4 == 1:
                            unit.append(other)
                        elif 12 <= digit <= 15 and other_digit % 4 == 0:
                            unit.append(other)
            if 'B' in square:
                digit = int(square.replace('B', ''))
                for other in squares:
                    if 'A' in other:
                        other_digit = int(other.replace('A', ''))
                        if (fabs(other_digit - digit)) % 4 == 0: #This is in the same column
                            unit.append(other)
                    if 'B' in other:
                        other_digit = int(other.replace('B', ''))
                        if (fabs(other_digit - digit)) % 4 == 0: #This is in the same column
                            unit.append(other)
                        elif (digit >= 8 and other_digit >= 8) or (
                                    digit < 8 and other_digit < 8): #This is the same 8 square unit and on same line
                            unit.append(other)
                    if 'C' in other:
                        other_digit = int(other.replace('C', ''))
                        if 3 >= digit >= 0 <= other_digit <= 3:
                            unit.append(other)
                        elif 7 >= digit >= 4 <= other_digit <= 7:
                            unit.append(other)
                        elif 11 >= digit >= 8 <= other_digit <= 11:
                            unit.append(other)
                        elif 15 >= digit >= 12 <= other_digit <= 15:
                            unit.append(other)
            if 'C' in square:
                digit = int(square.replace('C', ''))
                for other in squares:
                    if 'A' in other:
                        other_digit = int(other.replace('A', ''))
                        if 0 <= other_digit <= 3 and digit % 4 == 3:
                            unit.append(other)
                        elif 4 <= other_digit <= 7 and digit % 4 == 2:
                            unit.append(other)
                        elif 8 <= other_digit <= 11 and digit % 4 == 1:
                            unit.append(other)
                        elif 12 <= other_digit <= 15 and digit % 4 == 0:
                            unit.append(other)
                    if 'B' in other:
                        other_digit = int(other.replace('B', ''))
                        if 0 <= other_digit <= 3 and 0 <= digit <= 3:
                            unit.append(other)
                        elif 4 <= other_digit <= 7 and 4 <= digit <= 7:
                            unit.append(other)
                        elif 8 <= other_digit <= 11 and 8 <= digit <= 11:
                            unit.append(other)
                        elif 12 <= other_digit <= 15 and 12 <= digit <= 15:
                            unit.append(other)
                    if 'C' in other:
                        other_digit = int(other.replace('C', ''))

                        if (fabs(other_digit - digit)) % 4 == 0: #This is in the same column
                            unit.append(other)
                        elif digit // 4 == other_digit // 4: #This is the same line
                            unit.append(other)
                        elif digit % 2 == 0: #Column is first column of rectangular group
                            if (fabs(other_digit - digit - 1)) % 4 == 0:#Other column is column to the right
                                unit.append(other)
                        elif digit % 2 == 1: #Column is second column of rectangular group
                            if (fabs(other_digit - digit + 1)) % 4 == 0: #Other column is column to the left
                                unit.append(other)

            units[square] = list(set(unit))
        return units


class SolvingError(Exception):
    pass