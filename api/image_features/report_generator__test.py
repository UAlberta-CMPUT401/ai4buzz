"""Tests for ReportGenerator."""

from unittest import TestCase
from unittest import mock
import unittest

from api.image_features import report_generator
from api.image_features import descriptions

class ReportGeneratorTest(TestCase):

    def test_generate_report_object_detection(self):
        object_detections_description = descriptions.Descriptions(feature='Object Detection',
            model_name='Mock Model', descriptions=[('person', 98), ('bicycle', 97), ('bicycle', 47)],
            processed_image='9j'
        )
        expected_report = {'person': {'freq': 1, 'confidences': [98]},
                            'bicycle': {'freq': 2, 'confidences': [97, 47]},
                            'processes_bounding_boxes_image_as_base64_string': '9j'
        }

        report_generator_ = report_generator.ReportGenerator()
        actual_report = report_generator_.generate_report(object_detections_description)

        self.assertEqual(expected_report, actual_report)

    def test_generate_report_for_image_classification(self):
        classification_description = descriptions.Descriptions(feature='Image Classification',
            model_name='Mock Model', descriptions=[('person', 98), ('bicycle', 97), ('bike', 47)]
        )
        expected_report = {'person': 98, 'bicycle': 97, 'bike': 47}

        report_generator_ = report_generator.ReportGenerator()
        actual_report = report_generator_.generate_report(classification_description)

        self.assertEqual(expected_report, actual_report)

    def test_generate_resport_for_dict(self):
        expected_report = {'person': 98, 'bicycle': 97, 'bike': 47}

        report_generator_ = report_generator.ReportGenerator()
        actual_report = report_generator_.generate_report(expected_report)

        self.assertEqual(expected_report, actual_report)

    def test_generate_resport_for_str(self):
        expected_report = 'test string'

        report_generator_ = report_generator.ReportGenerator()
        actual_report = report_generator_.generate_report(expected_report)

        self.assertEqual(expected_report, actual_report)

if __name__ == '__main__':
    unittest.main()
