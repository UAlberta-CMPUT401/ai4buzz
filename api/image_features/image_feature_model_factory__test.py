"""Tests for ImageFeatureModelFactory."""

import unittest
from unittest import TestCase
from api.image_features.image_classification.image_classifiier import ImageClassifier

from api.image_features.collage_generator import CollageGenerator
from api.image_features.image_feature_model_factory import ImageFeatureModelFactory
from api.image_features.colour_scheme_analysis.colour_palette import ColorSchemeAnalyzer
from api.image_features.object_detection.object_detector import ObjectDetector
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.image_classification.image_classifiier import ImageClassifier
from api.image_features.tf_hub_client import TFHubClient
from api.image_features.text_recognition.text_recognizer import TextRecognizer
from api.image_features.facial_analysis.facial_detector import FaceDetector


class ImageFeatureModelFactoryTest(TestCase):
    
    def test_create_and_get_feature_model(self):
        factory = ImageFeatureModelFactory()
        self.assertIsInstance(factory.create_and_get_feature_model('color_scheme_analysis'), ColorSchemeAnalyzer)
        self.assertIsInstance(factory.create_and_get_feature_model('object_detection'), ObjectDetector)
        self.assertIsInstance(factory.create_and_get_feature_model('image_classification'), ImageClassifier)
        self.assertIsInstance(factory.create_and_get_feature_model('sentiment_analysis'), SentimentAnalyzer)
        self.assertIsInstance(factory.create_and_get_feature_model('text_recognition'), TextRecognizer)
        self.assertIsInstance(factory.create_and_get_feature_model('face_analysis'), FaceDetector)
        self.assertIsInstance(factory.create_and_get_feature_model('collage'), CollageGenerator)



if __name__ == '__main__':
    unittest.main()
