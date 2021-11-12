"""Tests for ImageClassifier"""
import tensorflow as tf
from PIL import Image
from unittest import TestCase
from unittest import mock
import unittest
import numpy

from api.image_features import descriptions
from api.image_features.image_classification import image_classifiier

class ImageClassifierTest(TestCase):

    @mock.patch("tensorflow.nn.softmax", return_value = tf.constant([[70, 9, 8, 1, 7, 5]]))
    def test_get_descreptions(self, _):
        a = numpy.random.rand(30,30,3) * 255
        mock_image = Image.fromarray(a.astype('uint8')).convert('RGB')  # Random image
        mock_tf_hub_client = self._get_mock_tf_hub()
        mock_model_name = 'Mock Model'

        actual_detections = image_classifiier.ImageClassifier(
            mock_tf_hub_client, mock_model_name).get_descriptions(mock_image)

        expected_detections = descriptions.Descriptions(feature='Image Classification',
            model_name=mock_model_name,
            descriptions=[('p', 70), ('q', 9), ('r', 8), ('t', 7), ('u', 5)]
        )

        self.assertEqual(expected_detections, actual_detections)
        mock_tf_hub_client.get_imagenet_classes.assert_called_once_with()
        mock_tf_hub_client.get_image_classification_model_from_cache_else_load.\
            assert_called_once_with(mock_model_name)

    def _get_mock_tf_hub(self):
        mock_image_classification_model = mock.MagicMock()
        mock_model_results = tf.constant([[11., 5., 4., 0.1, 3., 1., 0.25]])
        mock_image_classification_model.return_value = mock_model_results
        mock_tf_hub = mock.MagicMock()
        mock_tf_hub.get_image_classification_model_from_cache_else_load\
            .return_value = mock_image_classification_model
        mock_tf_hub.get_imagenet_classes.return_value = ['p', 'q', 'r', 's', 't', 'u', 'v']
        return mock_tf_hub


if __name__ == '__main__':
    unittest.main()
