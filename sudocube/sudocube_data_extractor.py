#coding: utf-8
from face_extraction.front_face_extractor import FrontFaceExtractor
from face_extraction.side_face_extractor import SideFaceExtractor
from face_extraction.top_face_extractor import TopFaceExtractor
from adjustable_parameters import front_face, side_face, top_face, red_square


class SudocubeDataExtractor(object):
    def __init__(self):
        self._init_dependencies()

    def _init_dependencies(self):
        self._front_extractor = FrontFaceExtractor()
        self._side_extractor = SideFaceExtractor()
        self._top_extractor = TopFaceExtractor()

    def extract_data_from_image_with_corner_info(self, image, corners):
        front_data, front_red_square = self._front_extractor.extract_data(image, corners[front_face])
        side_data, side_red_square = self._side_extractor.extract_data(image, corners[side_face])
        top_data, top_red_square = self._top_extractor.extract_data(image, corners[top_face])
        red_square_position = self._get_red_square_position(front_red_square, side_red_square, top_red_square)

        print top_data
        print front_data
        print side_data
        print red_square_position

        return {front_face: front_data, side_face: side_data, top_face: top_data, red_square: red_square_position}

    def _get_red_square_position(self, front, side, top):
        if front is not None:
            position = (front_face, front)
        elif side is not None:
            position = (side_face, side)
        elif top is not None:
            position = (top_face, top)

        return position