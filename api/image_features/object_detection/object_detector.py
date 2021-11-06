"""Contains class to detect objects in an image."""
import numpy as np

from api.image_features import descriptions
from api.image_features import tf_hub_client
from api.image_features.object_detection import object_detection_models_map

class ObjectDetector:
    """Used to detect objects present in a image using TF HUB models
        trained on the COCO 2017 dataset."""

    _model_name: str
    _tf_hub_client: tf_hub_client.TFHubClient
    _MINIMUM_THRESHOLD_CONFIDENCE = 0.60

    def __init__(self, tf_hub_client: tf_hub_client.TFHubClient, 
        model_name: str = 'Faster R-CNN Inception ResNet V2 1024x1024') -> None:
        self._tf_hub_client = tf_hub_client
        self._model_name = model_name

    def get_descriptions(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile
        returns: Descreptions(descreptions=[('person', 0.99), ('boat', 0.77), ...])"""
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
            detection_class = object_detection_models_map.COOC_CATEGORY_INDEX[results['detection_classes'][0][i].numpy()]['name']
            detection_confidence = results['detection_scores'][0][i].numpy()
            if detection_confidence > self._MINIMUM_THRESHOLD_CONFIDENCE:
                predictions.append((detection_class, detection_confidence))
        return predictions
