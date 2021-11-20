"""Contains tests for ImageDescriber."""

import unittest
import numpy
from unittest import TestCase, mock
from PIL import Image

from api.image_features.image_describer import ImageDescriber, ImageInfo

class ImageDescriberTest(TestCase):

    _mock_object_detection_model = mock.MagicMock()
    _mock_image_classification_model = mock.MagicMock()
    _mock_collage_model = mock.MagicMock()
    _mock_object_detection_future = mock.MagicMock()
    _mock_image_classification_future = mock.MagicMock()
    _mock_np_image = (numpy.random.rand(30,30,3) * 255).astype('uint8')
    _mock_image = Image.fromarray(_mock_np_image).convert('RGB')  # Random image
    _mock_object_detection = {'person': 98}
    _mock_image_classification = {'man': 80}
    _mock_collage = '9j'
    
    def test_get_features_by_image(self):
        mock_factory = self._get_mock_image_feature_model_factory()
        mock_report_generator = self._get_mock_report_generator()
        mock_process_pool_executor = self._get_mock_pool_executor()
        image_infos = [ImageInfo("1", self._mock_image, ('object_detection', 'image_classification'))]

        image_describer = ImageDescriber(mock_factory, mock_report_generator, mock_process_pool_executor)
        image_features = image_describer.get_features_by_image(image_infos)

        self._assert_as_expected_mock_pool_executor(mock_process_pool_executor)
        self._assert_as_expected_mock_image_feature_model_factory(mock_factory)
        self._assert_as_expected_futures()
        self._assert_as_expected_report_generator(mock_report_generator)
        self._assert_as_expected_image_features(image_features)
    
    def _assert_as_expected_mock_pool_executor(self,
        mock_pool_executor: mock.MagicMock) -> None:
        actual_submit_calls = mock_pool_executor.__enter__().submit.call_args_list
        expected_submit_calls = [mock.call(self._mock_object_detection_model.get_descriptions, self._mock_image),
            mock.call(self._mock_image_classification_model.get_descriptions, self._mock_image)
        ]
        self.assertEqual(expected_submit_calls, actual_submit_calls)

    def _assert_as_expected_mock_image_feature_model_factory(self,
        mock_factory: mock.MagicMock) -> None:
        expected_calls = [mock.call.create_and_get_feature_model('object_detection'),
            mock.call.create_and_get_feature_model('image_classification'),
            mock.call.create_and_get_feature_model('collage')]
        mock_factory.assert_has_calls(expected_calls, any_order=False)

    def _assert_as_expected_futures(self) -> None:
        self._mock_object_detection_future.result.assert_called_once_with()
        self._mock_image_classification_future.result.assert_called_once_with()

    def _assert_as_expected_report_generator(self, mock_report_generator: mock.MagicMock) -> None:
        expected_generate_report_calls = [mock.call(self._mock_object_detection),
            mock.call(self._mock_image_classification),
        ]
        mock_report_generator.generate_report.assert_has_calls(expected_generate_report_calls)
        mock_report_generator.generate_collage_report.assert_called_once_with(self._mock_collage)

    def _assert_as_expected_image_features(self, image_features) -> None:
        expected_feature_analysis_results = [
            {
            'id': '1',
            'object_detection': self._mock_object_detection,
            'image_classification': self._mock_image_classification,
            }
        ]
        expected_image_features = {
            'feature_analysis_results': expected_feature_analysis_results,
            'collage_image_string': self._mock_collage
        }
        print(image_features)
        self.assertEqual(expected_image_features, image_features)

    def _get_mock_image_feature_model_factory(self) -> mock.MagicMock:
        mock_factory = mock.MagicMock()
        self._mock_collage_model.generate.return_value = self._mock_collage
        mock_factory.create_and_get_feature_model.side_effect = [
            self._mock_object_detection_model, self._mock_image_classification_model,
            self._mock_collage_model
        ]
        return mock_factory

    def _get_mock_pool_executor(self) -> mock.MagicMock:
        mock_pool_executor = mock.MagicMock()
        self._mock_object_detection_future.result.return_value = self._mock_object_detection
        self._mock_image_classification_future.result.return_value = self._mock_image_classification
        mock_pool_executor.__enter__().submit.side_effect = [
            self._mock_object_detection_future, self._mock_image_classification_future]
        return mock_pool_executor

    def _get_mock_report_generator(self) -> mock.MagicMock:
        mock_report_generator = mock.MagicMock()
        mock_report_generator.generate_report.side_effect = self._mock_generate_report
        mock_report_generator.generate_collage_report.return_value = self._mock_collage
        return mock_report_generator
    
    def _mock_generate_report(self, description):
        return description

if __name__ == '__main__':
    unittest.main()
