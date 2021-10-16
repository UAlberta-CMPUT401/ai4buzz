"""Contains class to detect objects in an image."""
import tensorflow as tf
import tensorflow_hub as hub

import requests
from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np

from . import descriptions
from . import object_detection_models_map
from api.models.feature_analyzer import FeatureAnalyzer


class ObjectDetector(FeatureAnalyzer):
    """Used to detect objects present in a image using TF HUB models
        trained on the COCO 2017 dataset."""

    _model_name: str

    def __init__(self, model_name: str = 'Faster R-CNN Inception ResNet V2 1024x1024') -> None:
        self._model_name = model_name

    def get_descriptions(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        image = self._process_image_for_model(image)
        predictions = self._make_prediction(image)
        description = descriptions.Descriptions(feature="Object Detection", 
            model_name=self._model_name, descriptions=predictions)
        return self._format_description(description.descriptions)
    
    def _format_description(self, description):
        """
        format the description of the object detection result

        description: Descriptions
        :return: dict
        """
        objects = dict()
        for obj_name, confidence in description:
            if obj_name not in objects:
                objects[obj_name] = {
                    "freq": 1,
                    "confidences": [confidence.item()] 
                }
            else:
                objects[obj_name]["freq"] += 1
                objects[obj_name]["confidences"].append(confidence.item())
        return objects

    def _process_image_for_model(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        """Returns: numpy.ndarray"""
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (1, im_height, im_width, 3)).astype(np.uint8)

    def _make_prediction(self, image):
        model_handle = object_detection_models_map.MODEL_HANDLE_MAP[self._model_name]
        hub_model = hub.load(model_handle)
        results = hub_model(image)

        predictions = []
        for i in range(int(results['num_detections'][0].numpy())):
            predictions.append((
                object_detection_models_map.COOC_CATEGORY_INDEX[results['detection_classes'][0][i].numpy()]['name'],
                results['detection_scores'][0][i].numpy()))
        return predictions
    
if __name__=='__main__':
    image_path = 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Motorboat_at_Kankaria_lake.JPG'
    user_agent = {'User-agent': 'Colab Sample (https://tensorflow.org)'}
    response = requests.get(image_path, headers=user_agent)
    image = Image.open(BytesIO(response.content))
    # ObjectDetector().get_descriptions(image).descriptions returns [('person', 0.99), ('boat', 0.77), ...]
    print(ObjectDetector().get_descriptions(image).descriptions)