#coding: utf-8
from Kinocto.sudocube.adjustable_parameters import top_face, front_face, side_face


class SudocubeAdapter(object):
    def get_grid(self, data):
        return self._get_grid_from_data(data)

    def get_solved_dict(self, solved_grid):
        faces = {top_face: "A", front_face: "B", side_face: "C"}
        transformed = {top_face: [], front_face: [], side_face: []}
        for face, value in faces.iteritems():
            for i in range(16):
                transformed[face].append(solved_grid[faces[face] + str(i)])
        return transformed

    def _get_grid_from_data(self, data):
        front = data[front_face]
        side = data[side_face]
        top = data[top_face]

        grid = ""

        for d in top:
            grid = self._add_right_number_to_grid(d, grid)

        for d in front:
            grid = self._add_right_number_to_grid(d, grid)

        for d in side:
            grid = self._add_right_number_to_grid(d, grid)

        return grid

    def _add_right_number_to_grid(self, digit, grid):
        if digit is None:
            grid += "."
        else:
            grid = grid + digit
        return grid
