from PIL import Image
import numpy as np

from .experimental.colour.colour_palette import ColorSchemeAnalyzer
from .experimental.object.object_detector import ObjectDetector
from .experimental.sentiment.sentiment_analyzer import SentimentAnalyzer
from .experimental.object.image_classifiier import ImageClassifier
from .experimental.object.tf_hub_client import TFHubClient
#from .experimental.object.face_detection import FaceDetector

class ImageDescriber():
    def get_features_by_image(self, image):
        """ perform analysis and data extraction on image 

        :param image: PIL image object
        :return: dict containing formatted analysis data
        """
        colorSchemeAnalyzer = ColorSchemeAnalyzer()
        color_scheme_analysis = colorSchemeAnalyzer.get_descriptions(image)
        object_detector = ObjectDetector(TFHubClient())
        object_detections = object_detector.get_descriptions(image)
        image_classifier = ImageClassifier(TFHubClient())
        image_classification = image_classifier.get_descriptions(image)

        objects = dict()
        for obj_name, confidence in image_classification.descriptions:
            if obj_name not in objects:
                objects[obj_name] = confidence.item() 

        print(objects)

        sentiment_analyzer = SentimentAnalyzer(batch_size=1)
        sentiment_analysis = sentiment_analyzer.get_descriptions([image])
        #facialDetector = FaceDetector()
        #facial_analysis = facialDetector.get_descriptions(image)

        return {
            "color_scheme_analysis": color_scheme_analysis,
            "object_detection": object_detections,
            "sentiment_analysis": sentiment_analysis,
            "image_classification": objects
            #"facial_analysis": facial_analysis
        }

    def _preprocess_image(self, image):
        """ convert image into an np array

        :param Image: the image to be analyzed
        :return: numpy array
        """
        return np.array(image)
