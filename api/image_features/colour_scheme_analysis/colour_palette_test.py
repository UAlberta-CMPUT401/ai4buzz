"""Tests for colour palette"""
from unittest import TestCase
from unittest import mock
import unittest
from PIL import Image

import colour_palette


class ColourPaletteTest(TestCase):

    def test_get_descreptions(self):
        
        mock_image = Image.open('/home/alex/Documents/comput401/new repo/ai4buzz/api/image_features/colour_scheme_analysis/colour_test.jpg')  # test image
        
       

        actual_detections_description = colour_palette.ColorSchemeAnalyzer(
        ).get_descriptions(mock_image)

        
        self.assertEqual(237, actual_detections_description["colors"][0]["red"])
        self.assertEqual(27, actual_detections_description["colors"][0]["green"])
        self.assertEqual(36, actual_detections_description["colors"][0]["blue"])
        
        

   


if __name__ == '__main__':
    unittest.main()