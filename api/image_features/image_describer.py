"""Contains the ImageDescriber class.

This class is used to describe a givem image by running various models on the image."""
from typing import Any, Dict
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import imagehash

from api.image_features.collage_generator import CollageGenerator
from api.image_features.dendrogram_generator import DendrogramGenerator
from api.image_features.report_generator import ReportGenerator
from api.image_features.colour_scheme_analysis.colour_palette import ColorSchemeAnalyzer
from api.image_features.object_detection.object_detector import ObjectDetector
from api.image_features.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from api.image_features.image_classification.image_classifiier import ImageClassifier
from api.image_features.tf_hub_client import TFHubClient
from api.image_features.text_recognition.text_recognizer import TextRecognizer
from api.image_features.facial_analysis.facial_detector import FaceDetector


def color_scheme_analysis(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    color_scheme_analysis = ColorSchemeAnalyzer().get_descriptions(image)
    return color_scheme_analysis

def object_detection(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    object_detections_descriptions = ObjectDetector(TFHubClient()).get_descriptions(image)
    object_detection_report = ReportGenerator().generate_report(object_detections_descriptions)
    return object_detection_report

def image_classification(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    image_classification_descreptions = ImageClassifier(TFHubClient()).get_descriptions(image)
    image_classification_report = ReportGenerator().generate_report(image_classification_descreptions)
    return image_classification_report

def sentiment_analysis(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    sentiment_analysis = SentimentAnalyzer(batch_size=1).get_descriptions([image])
    return sentiment_analysis

def text_recognition(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    text_recognition = TextRecognizer().get_descriptions(image)
    return text_recognition

def face_detection(image_string: Dict[str, Any]) -> Dict[str, Any]:
    image = Image.frombytes(image_string['mode'], image_string['size'], image_string['pixels'])
    face_detection = FaceDetector().get_descriptions(image)
    return face_detection

def describe_an_image(image_info: Dict[str, Any]) -> Dict[str, Any]:
    """:param images: image_info = {'id':int, 'image':PIL Image}"""
    image = image_info["image"]
    image_string = {'pixels': image.tobytes(), 'size': image.size, 'mode': image.mode,}
    with ProcessPoolExecutor() as pool:
        future_color_scheme_analysis = pool.submit(color_scheme_analysis, image_string)
        future_object_detection = pool.submit(object_detection, image_string)
        future_image_classification = pool.submit(image_classification, image_string)
        future_sentiment_analysis = pool.submit(sentiment_analysis, image_string)
        future_text_recognition = pool.submit(text_recognition, image_string)
        future_face_detection = pool.submit(face_detection, image_string)

        color_scheme_analysis_report = future_color_scheme_analysis.result()
        object_detection_report = future_object_detection.result()
        image_classification_report = future_image_classification.result()
        sentiment_analysis_report = future_sentiment_analysis.result()
        text = future_text_recognition.result()
        face_analysis = future_face_detection.result()

    return {
        "id": image_info["id"],
        "color_scheme_analysis": color_scheme_analysis_report,
        "object_detection": object_detection_report,
        "sentiment_analysis": sentiment_analysis_report,
        "image_classification": image_classification_report,
        "text_recognition": text,
        "face_analysis": face_analysis,
    }

class ImageDescriber():
    """Extracts features for images."""
    def get_features_by_image(self, images_info):
        """ perform analysis and data extraction on image 

        :param images_info: List of Dicts where Dict = {'id':int, 'image':PIL Image}
        :return: dict containing formatted analysis data
        """
        self.remove_duplicates(images_info)

        feature_analysis_results = []
        with ProcessPoolExecutor(max_workers=4) as pool:
            for image_description in pool.map(describe_an_image, images_info):
                feature_analysis_results.append(image_description)
            
        collage_generator = CollageGenerator()
        collage = collage_generator.generate([img['image'] for img in images_info])
        collage_image_string = ReportGenerator().generate_collage_report(collage)

        return {
            "feature_analysis_results": feature_analysis_results,
            "collage_image_string": collage_image_string
        }

    def remove_duplicates(self, images):
        hash_size = 8
        hashes = {}
        duplicates = []
        for image in images:
            temp_hash = imagehash.average_hash(image['image'], hash_size)
            if temp_hash in hashes:
                duplicates.append(image)
            else:
                hashes[temp_hash] = image

        for d in duplicates:
            if d in images:
                images.remove(d)
