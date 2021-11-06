"""Contains TFHubClient class that provides access to TF HUB."""
import os
import tensorflow as tf
import tensorflow_hub as hub

from typing import Tuple, List

from api.image_features.image_classification import image_classification_models_map
from api.image_features.object_detection import object_detection_models_map

class TFHubClient:
    """Allows us to get models from TFHUB."""

    def get_image_classification_model_from_cache_else_load(self, model_name: str):
        is_model_cahced, model_path = self._is_model_cached("image_classification", model_name)
        if is_model_cahced:
            classifier = tf.saved_model.load(model_path)
        else:
            model_handle = image_classification_models_map.MODEL_HANDLE_MAP[model_name]
            classifier = hub.load(model_handle)
            tf.saved_model.save(classifier, model_path)
        return classifier

    def get_object_detection_model_from_cahce_else_load(self, model_name: str):
        is_model_cahced, model_path = self._is_model_cached("object_detection", model_name)
        if is_model_cahced:
            object_detector = tf.saved_model.load(model_path)
        else:
            model_handle = object_detection_models_map.MODEL_HANDLE_MAP[model_name]
            object_detector = hub.load(model_handle)
            tf.saved_model.save(object_detector, model_path)
        return object_detector

    def get_imagenet_classes(self) -> List[str]:
        labels_file = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
        # Download labels and creates a maps
        downloaded_file = tf.keras.utils.get_file("labels.txt", origin=labels_file)
        classes = []
        i = 0
        with open(downloaded_file) as f:
            labels = f.readlines()
            classes = [l.strip() for l in labels[1:]]
            i += 1
        return classes

    def _is_model_cached(self, model_type: str, model_name: str) -> Tuple[bool, str]:
        current_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_path, "cached_tf_models", model_type, model_name)
        return (os.path.isdir(model_path), model_path)

