"""Tests for facial detection"""
#Different machines may return different values
import unittest
from PIL import Image
import facial_detector

class FaceAnalysisTest(unittest.TestCase):


    def test_get_descreption(self):       
        image = Image.open('face_test.jpg')
        actual_face = facial_detector.FaceDetector().get_descriptions(image)
        if os.name == 'nt':
            #windows results
            self.assertEqual(actual_face['count'], 1)
            self.assertEqual(actual_face['analysis'][0]['emotion'], 
            {'angry': 0, 'disgust': 0, 'fear': 0, 
            'happy': 98.89170924787601, 'sad': 0, 'surprise': 0, 
            'neutral': 1.1082497598638248})
            self.assertEqual(actual_face['analysis'][0]['dominant_emotion'], 'happy')
            self.assertEqual(actual_face['analysis'][0]['likely age'], 36.666666666666664)
            self.assertEqual(actual_face['analysis'][0]['estimated gender'], 'male')
            self.assertEqual(actual_face['analysis'][0]['race'], 
            {'asian': 0, 'indian': 0, 'black': 0,
             'white': 99.9936540921529, 'middle eastern': 0.004135344837171337,
             'latino hispanic': 0.0022066935343900695})
            self.assertEqual(actual_face['analysis'][0]['estimated_race'], 'white')
        elif os.name == 'posix'
            #linux results
            self.assertEqual(actual_face['count'], 1)
            self.assertEqual(actual_face['analysis'][0]['emotion'], 
            {'angry': 0, 'disgust': 0, 'fear': 0, 
            'happy': 99.5799461758852, 'sad': 7.409249809739712e-05, 'surprise': 0, 
            'neutral': 0.41994712946584145})
            self.assertEqual(actual_face['analysis'][0]['dominant_emotion'], 'happy')
            self.assertEqual(actual_face['analysis'][0]['likely age'], 37.333333333333336)
            self.assertEqual(actual_face['analysis'][0]['estimated gender'], 'male')
            self.assertEqual(actual_face['analysis'][0]['race'], 
            {'asian': 0, 'indian': 0, 'black': 0,
             'white': 99.99056061052644, 'middle eastern': 0.006221890914964973,
             'latino hispanic': 0.0032200740658458386})
            self.assertEqual(actual_face['analysis'][0]['estimated_race'], 'white')

if __name__ == '__main__':
    unittest.main()
