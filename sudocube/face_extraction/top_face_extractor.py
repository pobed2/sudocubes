#coding: utf-8

from Kinocto.sudocube.face_extraction.face_extractor import FaceExtractor


class TopFaceExtractor(FaceExtractor):
    def _calculate_cutoffs(self, top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner):
        tolerance = -10 #FIXME hack un peu louche pour réduire la taille des carreaux
        x_cutoffs = (bottom_left_corner[0] + tolerance, top_right_corner[0] + tolerance)
        y_cutoffs = (top_left_corner[1], bottom_right_corner[1] + tolerance)

        return x_cutoffs, y_cutoffs