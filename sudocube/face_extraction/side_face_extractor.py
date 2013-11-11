#coding: utf-8
from Kinocto.sudocube.face_extraction.face_extractor import FaceExtractor


class SideFaceExtractor(FaceExtractor):
    def _calculate_cutoffs(self, top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner):
        x_cutoffs = (bottom_left_corner[0], top_right_corner[0])
        y_cutoffs = (top_right_corner[1] + 25, bottom_left_corner[1])
        return x_cutoffs, y_cutoffs