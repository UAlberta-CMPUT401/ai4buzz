"""Contains the ImageDescriber class.

This class is used to describe a givem image by running various models on the image."""
import base64
from io import BytesIO
from typing import Any, Dict
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from api.image_features import dendrogram_generator
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

def duplicate_remover(images):
    hash_size = 8
    hashes = {}
    duplicates = []
    print('\nFinding duplicate input images now:')
    for image in images:
        temp_hash = imagehash.average_hash(image['image'], hash_size)
        if temp_hash in hashes:
            duplicates.append(image)
        else:
            hashes[temp_hash] = image

    for d in duplicates:
        if d in images:
            images.remove(d)

    print("{} duplicates removed from {} input images\n".format(len(duplicates),len(duplicates)+len(images)))

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

class ImageDescriber():
    """Extracts features for images."""
    def get_features_by_image(self, images):
        """ perform analysis and data extraction on image 

        :param images: List of Dicts where Dict = {'id':int, 'image':PIL Image}
        :return: dict containing formatted analysis data
        """

        duplicate_remover(images)

        text_recognizer = TextRecognizer()
        face_detector = FaceDetector()

        feature_analysis_results = []
        for image_info in images:
            image = image_info["image"]
            image_string = {'pixels': image.tobytes(), 'size': image.size, 'mode': image.mode,}
            with ProcessPoolExecutor() as pool:
                future_color_scheme_analysis = pool.submit(color_scheme_analysis, image_string)
                future_object_detection = pool.submit(object_detection, image_string)
                future_image_classification = pool.submit(image_classification, image_string)
                future_sentiment_analysis = pool.submit(sentiment_analysis, image_string)

                color_scheme_analysis_report = future_color_scheme_analysis.result()
                object_detection_report = future_object_detection.result()
                image_classification_report = future_image_classification.result()
                sentiment_analysis_report = future_sentiment_analysis.result()
  
            text = text_recognizer.get_descriptions(image)
            face_analysis = face_detector.get_descriptions(image)

            feature_analysis_results.append({
                "id": image_info["id"],
                "color_scheme_analysis": color_scheme_analysis_report,
                "object_detection": object_detection_report,
                "sentiment_analysis": sentiment_analysis_report,
                "image_classification": image_classification_report,
                "text_recognition": text,
                "face_analysis": face_analysis,
            })

        collage_generator = CollageGenerator()
        collage = collage_generator.generate([img['image'] for img in images])

        # convert to base64
        buffer = BytesIO()
        collage_rgb = collage.convert('RGB')
        collage_rgb.save(buffer, format="JPEG")
        collage_image_string = base64.b64encode(buffer.getvalue())

        buffer = BytesIO()
        dendrogram_generator = DendrogramGenerator()
        dendrogram = dendrogram_generator.generate(feature_analysis_results)
        dendrogram_rgb = dendrogram.convert('RGB')
        dendrogram_rgb.save(buffer, format='JPEG')
        dendrogram_image_string = base64.b64encode(buffer.getvalue())


        return {
            "feature_analysis_results": feature_analysis_results,
            "collage_image_string": collage_image_string,
            "dendrogram_image_string": dendrogram_image_string,
        }
