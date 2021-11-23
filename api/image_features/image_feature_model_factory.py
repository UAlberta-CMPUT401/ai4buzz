"""Contains the ImageFeatureModelFacory class."""

from api.image_features.collage_generator import CollageGenerator
from api.image_features.feature_analyzer import FeatureAnalyzer
from api.image_features.colour_scheme_analysis.colour_palette import ColorSchemeAnalyzer
from api.image_features.object_detection.object_detector import ObjectDetector
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.image_classification.image_classifiier import ImageClassifier
from api.image_features.tf_hub_client import TFHubClient
from api.image_features.text_recognition.text_recognizer import TextRecognizer
from api.image_features.facial_analysis.facial_detector import FaceDetector


class ImageFeatureModelFactory:
    """Factory to construct and return appropriate models."""

    def create_and_get_feature_model(self, image_feature: str) -> FeatureAnalyzer:
        if image_feature == 'color_scheme_analysis':
            return ColorSchemeAnalyzer()
        elif image_feature == 'object_detection':
            return ObjectDetector(TFHubClient())
        elif image_feature == 'image_classification':
            return ImageClassifier(TFHubClient())
        elif image_feature == 'sentiment_analysis':
            return SentimentAnalyzer(batch_size=1)
        elif image_feature == 'text_recognition':
            return TextRecognizer()
        elif image_feature == 'face_analysis':
            return FaceDetector()
        elif image_feature == 'collage':
            return CollageGenerator()
