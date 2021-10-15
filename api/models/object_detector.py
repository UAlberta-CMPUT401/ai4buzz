"""Contains class to detect objects in an image."""
import requests
from PIL import Image
from io import BytesIO

import numpy as np

import descriptions
import object_detection_models_map
import tf_hub_client


class ObjectDetector:
    """Used to detect objects present in a image using TF HUB models
        trained on the COCO 2017 dataset."""

    _model_name: str
    _tf_hub_client: tf_hub_client.TFHubClient

    def __init__(self, tf_hub_client: tf_hub_client.TFHubClient, 
        model_name: str = 'Faster R-CNN Inception ResNet V2 1024x1024') -> None:
        self._tf_hub_client = tf_hub_client
        self._model_name = model_name

    def get_descriptions(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        image = self._process_image_for_model(image)
        predictions = self._make_prediction(image)
        return descriptions.Descriptions(feature="Object Detection", 
            model_name=self._model_name, descriptions=predictions)

    def _process_image_for_model(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        """Returns: numpy.ndarray"""
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (1, im_height, im_width, 3)).astype(np.uint8)

    def _make_prediction(self, image):
        object_detector = self._tf_hub_client.get_object_detection_model_from_cahce_else_load(self._model_name)
        results = object_detector(image)

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
    print(ObjectDetector(tf_hub_client.TFHubClient()).get_descriptions(image).descriptions)
