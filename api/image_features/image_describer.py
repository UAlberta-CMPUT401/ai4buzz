"""Contains the ImageDescriber class.

This class is used to describe a givem image by running various models on the image."""

from api.image_features.report_generator import ReportGenerator
from api.image_features.colour_scheme_analysis.colour_palette import ColorSchemeAnalyzer
from api.image_features.object_detection.object_detector import ObjectDetector
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.image_classification.image_classifiier import ImageClassifier
from api.image_features.tf_hub_client import TFHubClient


class ImageDescriber():

    def get_features_by_image(self, image):
        """ perform analysis and data extraction on image 

        :param image: PIL image object
        :return: dict containing formatted analysis data
        """
        report_generator_ = ReportGenerator()

        colorSchemeAnalyzer = ColorSchemeAnalyzer()
        color_scheme_analysis = colorSchemeAnalyzer.get_descriptions(image)

        object_detector = ObjectDetector(TFHubClient())
        object_detections_descriptions = object_detector.get_descriptions(image)
        object_detection_report = report_generator_.generate_report(object_detections_descriptions)

        image_classifier = ImageClassifier(TFHubClient())
        image_classification_descreptions = image_classifier.get_descriptions(image)
        image_classification_report = report_generator_.generate_report(image_classification_descreptions)

        sentiment_analyzer = SentimentAnalyzer(batch_size=1)
        sentiment_analysis = sentiment_analyzer.get_descriptions([image])

        return {
            "color_scheme_analysis": color_scheme_analysis,
            "object_detection": object_detection_report,
            "sentiment_analysis": sentiment_analysis,
            "image_classification": image_classification_report,
        }
