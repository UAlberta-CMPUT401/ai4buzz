"""Tests for facial detection"""
#Different machines may return different values
import unittest
from PIL import Image
import facial_detector

class FaceAnalysisTest(unittest.TestCase):


    def test_get_descreption(self):       
        image = Image.open('face_test.jpg')
        actual_face = facial_detector.FaceDetector().get_descriptions(image)

        self.assertEqual(actual_face['count'], 1)

        self.assertEqual(actual_face['analysis']['dominant_emotion'], 'happy')
        self.assertEqual(actual_face['analysis']['likely age'], 30.0)
        self.assertEqual(actual_face['analysis']['estimated_race'], 'middle eastern')

if __name__ == '__main__':
    unittest.main()