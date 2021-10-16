from PIL import Image
import numpy as np

from .experimental.colour.colour_palette import ColorSchemeAnalyzer
from .experimental.object.object_detector import ObjectDetector

class ImageDescriber():
    def __init__(self):
        pass

    def get_features_by_image(self, image):
        colorSchemeAnalyzer = ColorSchemeAnalyzer()
        color_scheme_analysis = colorSchemeAnalyzer.get_descriptions(image)
        object_detector = ObjectDetector()
        object_detections = object_detector.get_descriptions(image)
        return {
            "color_scheme_analysis": color_scheme_analysis,
            "object_detection": object_detections
        }

    def _get_descriptions(self):
        pass

    def _preprocess_image(self, image):
        """ convert image into an np array

        :param Image: the image to be analyzed
        :return: numpy array
        """
        return np.array(image)

    def _generate_report(self):
        pass