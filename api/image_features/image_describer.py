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
<<<<<<< HEAD
=======
from api.image_features.facial_analysis.facial_detector import FaceDetector
>>>>>>> will-face
import base64
from io import BytesIO


class ImageDescriber():
    """Extracts features for images."""
    def get_features_by_image(self, images):
        """ perform analysis and data extraction on image 

        :param image: PIL image object
        :return: dict containing formatted analysis data
        """
        report_generator_ = ReportGenerator()
        tf_hub_client = TFHubClient()
        colorSchemeAnalyzer = ColorSchemeAnalyzer()
        object_detector = ObjectDetector(tf_hub_client)
        image_classifier = ImageClassifier(tf_hub_client)
<<<<<<< HEAD
        text_recognizer = TextRecognizer()
        sentiment_analyzer = SentimentAnalyzer(batch_size=1)
=======
        sentiment_analyzer = SentimentAnalyzer(batch_size=1)
        text_recognizer = TextRecognizer()
        face_detector = FaceDetector()
>>>>>>> will-face

        feature_analysis_results = {}
        for idx, image in enumerate(images):
            color_scheme_analysis = colorSchemeAnalyzer.get_descriptions(image)
           
            object_detections_descriptions = object_detector.get_descriptions(image)
            object_detection_report = report_generator_.generate_report(object_detections_descriptions)
<<<<<<< HEAD

            image_classification_descreptions = image_classifier.get_descriptions(image)
            image_classification_report = report_generator_.generate_report(image_classification_descreptions)
          
            text = text_recognizer.get_descriptions(image)
=======
           
            image_classification_descreptions = image_classifier.get_descriptions(image)
            image_classification_report = report_generator_.generate_report(image_classification_descreptions)
          
>>>>>>> will-face
       
            sentiment_analysis = sentiment_analyzer.get_descriptions([image])
            text = text_recognizer.get_descriptions(image)
            face_analysis = face_detector.get_descriptions(image)

            feature_analysis_results["image_" + str(idx + 1)] = {
                "color_scheme_analysis": color_scheme_analysis,
                "object_detection": object_detection_report,
                "sentiment_analysis": sentiment_analysis,
                "image_classification": image_classification_report,
                "text_recognition": text,
                "face_analysis": face_analysis,
            }

        collage_generator = CollageGenerator()
        collage = collage_generator.generate(images)

        # convert to base64
        buffer = BytesIO()
        collage_rgb = collage.convert('RGB')
        collage_rgb.save(buffer, format="JPEG")
        collage_image_string = base64.b64encode(buffer.getvalue())

        # TODO: convert to base64 encoded string
        feature_analysis_results['collage'] = collage_base64_string

        dendrogram_generator = DendrogramGenerator()
        dendrogram = dendrogram_generator.generate(feature_analysis_results) 
        # TODO: convert to base64 encoded string
        # feature_analysis_results['dendrogram'] = dendrogram_base64_string

        return {
            "feature_analysis_results": feature_analysis_results,
            "collage_image_string": collage_image_string
        }
