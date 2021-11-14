"""Tests for ObjectDetector"""
import tensorflow as tf
from PIL import Image
from unittest import TestCase
from unittest import mock
import unittest
import numpy

from api.image_features.object_detection import object_detector
from api.image_features import descriptions

class ObjectDetectorTest(TestCase):

    @mock.patch('base64.b64encode', return_value=b'9j')
    def test_get_descreptions(self, _):
        mock_np_image = (numpy.random.rand(30,30,3) * 255).astype('uint8')
        mock_image = Image.fromarray(mock_np_image).convert('RGB')  # Random image
        mock_tf_hub_client = self._get_mock_tf_hub()
        mock_model_name = 'Mock Model'

        with mock.patch.object(object_detector.ObjectDetector,
            '_get_bounded_box_image',return_value=mock_np_image):
            actual_detections_description = object_detector.ObjectDetector(
                mock_tf_hub_client, mock_model_name).get_descriptions(mock_image)

            expected_detections_description = descriptions.Descriptions(feature='Object Detection',
                model_name=mock_model_name, descriptions=[('person', 98), ('bicycle', 97)],
                processed_image=b'9j'
            )
            self.assertEqual(expected_detections_description, actual_detections_description)
            mock_tf_hub_client.get_object_detection_model_from_cahce_else_load.\
                assert_called_once_with(mock_model_name)

    def _get_mock_tf_hub(self):
        mock_object_detection_model = mock.MagicMock()
        mock_results = {'num_detections': tf.constant([2.0]),
                        'detection_classes': tf.constant([[1.0, 2.0]]),
                        'detection_scores': tf.constant([[98, 97]]),
                        'detection_boxes': mock.MagicMock(),
        }
        mock_object_detection_model.return_value = mock_results
        mock_tf_hub = mock.MagicMock()
        mock_tf_hub.get_object_detection_model_from_cahce_else_load.return_value = mock_object_detection_model
        return mock_tf_hub


if __name__ == '__main__':
    unittest.main()
