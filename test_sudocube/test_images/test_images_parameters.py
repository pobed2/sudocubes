#coding: utf-8

import os

import numpy as np


_images_directory = os.path.dirname(__file__)

first_front_image_path = _images_directory + "/cube_front1.jpg"
first_front_image_corners = {
    'top': {'bl': np.array([80., 296.]), 'tl': np.array([224., 203.]), 'tr': np.array([431., 252.]),
            'br': np.array([256., 364.])},
    'side': {'bl': np.array([257., 550.]), 'tl': np.array([256., 364.]), 'tr': np.array([431., 252.]),
             'br': np.array([433., 463.])},
    'front': {'bl': np.array([85., 501.]), 'tl': np.array([80., 296.]), 'tr': np.array([256., 364.]),
              'br': np.array([257., 550.])}}
first_front_image_expected = {'red square': ("front", 0),
                              'top': [None, None, None, '8', None, '1', None, None, None, None, None, None, '3', None,
                                      None, '5'],
                              'side': ['6', None, None, None, None, '7', None, None, '4', None, None, '1', None, None,
                                       '2', None],
                              'front': [None, None, None, '7', None, None, '5', None, '2', None, None, '6', None, '7',
                                        None, None]}

second_front_image_path = _images_directory + "/cube_front2.jpg"
second_front_image_corners = {
    'top': {'bl': np.array([37., 303.]), 'tl': np.array([185., 198.]), 'tr': np.array([368., 252.]),
            'br': np.array([206., 354.])},
    'side': {'bl': np.array([212., 527.]), 'tl': np.array([206., 354.]), 'tr': np.array([368., 252.]),
             'br': np.array([369., 436.])},
    'front': {'bl': np.array([47., 485.]), 'tl': np.array([37., 303.]), 'tr': np.array([206., 354.]),
              'br': np.array([212., 527.])}}

second_front_image_expected = {'red square': ("front", 12),
                               'top': [None, '7', None, None, None, None, '8', None, None, None, None, None, None, None,
                                       None, None],
                               'side': [None, None, None, None, None, None, '3', None, '7', None, '4', None, None, '1',
                                        None, None],
                               'front': [None, None, None, '1', None, None, None, None, None, '3', None, None, None,
                                         None, '2', '6']}

first_multiple_image_path = _images_directory + "/multiple1.jpg"
second_multiple_image_path = _images_directory + "/multiple2.jpg"
third_multiple_image_path = _images_directory + "/multiple3.jpg"

first_unable_image_path = _images_directory + "/unable1.jpg"
second_unable_image_path = _images_directory + "/unable2.jpg"