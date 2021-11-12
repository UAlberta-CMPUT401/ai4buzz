"""Contains the ImageDescriber class.

This class is used to describe a givem image by running various models on the image."""

from api.image_features.collage_generator import CollageGenerator
from api.image_features.dendrogram_generator import DendrogramGenerator
from api.image_features.report_generator import ReportGenerator
from api.image_features.colour_scheme_analysis.colour_palette import ColorSchemeAnalyzer
from api.image_features.object_detection.object_detector import ObjectDetector
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.image_classification.image_classifiier import ImageClassifier
from api.image_features.tf_hub_client import TFHubClient
from api.image_features.text_recognition.text_recognizer import TextRecognizer


class ImageDescriber():

    def get_features_by_image(self, images):
        """ perform analysis and data extraction on image 

        :param image: PIL image object
        :return: dict containing formatted analysis data
        """
        report_generator_ = ReportGenerator()

        colorSchemeAnalyzer = ColorSchemeAnalyzer()
        color_scheme_analysis = colorSchemeAnalyzer.get_descriptions(images[0])

        object_detector = ObjectDetector(TFHubClient())
        object_detections_descriptions = object_detector.get_descriptions(images[0])
        object_detection_report = report_generator_.generate_report(object_detections_descriptions)

        image_classifier = ImageClassifier(TFHubClient())
        image_classification_descreptions = image_classifier.get_descriptions(images[0])
        image_classification_report = report_generator_.generate_report(image_classification_descreptions)

        sentiment_analyzer = SentimentAnalyzer(batch_size=len(images))
        sentiment_analysis = sentiment_analyzer.get_descriptions(images)

        text_recognizer = TextRecognizer()
        text = text_recognizer.get_descriptions(images[0])

        collage_generator = CollageGenerator()
        collage = collage_generator.generate(images)

        # TODO: convert to base64 encoded string
        # feature_analysis_results['collage'] = collage_base64_string

        feature_analysis_results = {
            "color_scheme_analysis": color_scheme_analysis,
            "object_detection": object_detection_report,
            "sentiment_analysis": sentiment_analysis,
            "image_classification": image_classification_report,
            "text_recognition": text,
        }

        dendrogram_generator = DendrogramGenerator()
        dendrogram = dendrogram_generator.generate(feature_analysis_results) 
        # TODO: convert to base64 encoded string
        # feature_analysis_results['dendrogram'] = dendrogram_base64_string

        return feature_analysis_results
