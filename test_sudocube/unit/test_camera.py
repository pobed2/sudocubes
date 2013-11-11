#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mock import patch

from Kinocto.devices.vision.camera import FakeCamera


class TestFakeCamera(unittest.TestCase):
    def setUp(self):
        self.image = "an image"

        self._camera = FakeCamera("FAKE PATH")

    @patch('cv2.imread')
    def test_should_return_RGB_image_cube_front_when_taking_picture(self, imread_mock):
        imread_mock.return_value = self.image

        image = self._camera.take_image()

        self.assertEqual(self.image, image)



