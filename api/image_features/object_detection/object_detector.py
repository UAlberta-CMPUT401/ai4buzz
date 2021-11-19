"""Contains class to detect objects in an image."""
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from typing import Any, Dict, List, Tuple

from api.image_features import descriptions
from api.image_features import tf_hub_client
from api.image_features.object_detection import object_detection_models_map
from api.image_features.object_detection.object_detection.utils import visualization_utils as viz_utils

class ObjectDetector:
    """Used to detect objects present in a image using TF HUB models
        trained on the COCO 2017 dataset."""

    _model_name: str
    _tf_hub_client: tf_hub_client.TFHubClient
    _MINIMUM_THRESHOLD_CONFIDENCE = 0.40

    def __init__(self, tf_hub_client: tf_hub_client.TFHubClient, 
        model_name: str = 'Faster R-CNN Inception ResNet V2 1024x1024') -> None:
        self._tf_hub_client = tf_hub_client
        self._model_name = model_name

    def get_descriptions(self, image):
        """image: PIL.JpegImagePlugin.JpegImageFile
        returns: Descreptions(descreptions=[('person', 0.99), ('boat', 0.77), ...])"""
        np_image = self._process_image_for_model(image)
        result = self._run_model_on_image(np_image)
        predictions = self._get_predictions(result)
        bounded_box_np_image = self._get_bounded_box_image(np_image, result)
        image_string = self._encode_image_as_base64(bounded_box_np_image)
        return descriptions.Descriptions(feature="Object Detection", 
            model_name=self._model_name, descriptions=predictions, processed_image=image_string)

    def _process_image_for_model(self, image) -> np.ndarray:
        """image: PIL.JpegImagePlugin.JpegImageFile"""
        """Returns: numpy.ndarray"""
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (1, im_height, im_width, 3)).astype(np.uint8)

    def _run_model_on_image(self, np_image: np.ndarray) -> Dict[str, Any]:
        object_detector = self._tf_hub_client.get_object_detection_model_from_cahce_else_load(self._model_name)
        results = object_detector(np_image)
        result = {key:value.numpy() for key,value in results.items()}
        return result

    def _get_predictions(self, result: Dict[str, Any]) -> List[Tuple[str, float]]:
        predictions = []
        category_index = object_detection_models_map.COOC_CATEGORY_INDEX
        for i in range(int(result['num_detections'][0])):
            detection_class = category_index[result['detection_classes'][0][i]]['name']
            # .item() to convert from numpy.float32 to float
            detection_confidence = result['detection_scores'][0][i].item()
            if detection_confidence > self._MINIMUM_THRESHOLD_CONFIDENCE:
                predictions.append((detection_class, detection_confidence))
        return predictions

    def _get_bounded_box_image(self, np_image: np.ndarray, result: Dict[str, Any]) -> np.ndarray:
        image_np_with_detections = np_image.copy()

        # Use keypoints if available in detections
        keypoints, keypoint_scores = None, None
        if 'detection_keypoints' in result:
            keypoints = result['detection_keypoints'][0]
            keypoint_scores = result['detection_keypoint_scores'][0]

        category_index = object_detection_models_map.COOC_CATEGORY_INDEX
        keypoint_edges = object_detection_models_map.COCO17_HUMAN_POSE_KEYPOINTS
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections[0],
            result['detection_boxes'][0],
            (result['detection_classes'][0]).astype(int),
            result['detection_scores'][0],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.30,
            agnostic_mode=False,
            keypoints=keypoints,
            keypoint_scores=keypoint_scores,
            keypoint_edges=keypoint_edges)
        return image_np_with_detections[0]

    def _encode_image_as_base64(self, np_image: np.ndarray) -> bytes:
        image = Image.fromarray(np_image)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str
