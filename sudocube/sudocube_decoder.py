#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudocube_factory import SudocubeFactory


class SudocubeDecoder(object):
    def __init__(self):
        self._init_dependencies()

    def _init_dependencies(self):
        self._sudocube_factory = SudocubeFactory()

    def compute_solved_sudocube_and_digit_to_draw(self, image):
        try:
            sudocube = self._sudocube_factory.create_sudocube_from_image(image)
            sudocube.solve()
            return sudocube
        except Exception as e:
            raise UnableToProcessSudocubeError("Error in solving the sudocube : " + e)


class UnableToProcessSudocubeError(RuntimeError):
    pass