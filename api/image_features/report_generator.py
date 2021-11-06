"""Contains ReportGenerator class.

This class is used to generate report for the image based on the
returned descriptions from the models."""

from typing import Dict, List, Union
from api.image_features import descriptions


class ReportGenerator:
    """Generates report for each image feature extraction model."""

    def generate_report(self, descriptions_: descriptions.Descriptions) -> \
        Dict[str, Union[int, List[float]]]:
        if descriptions_.feature == 'Object Detection':
            return self._generate_report_for_object_detection(descriptions_)
        elif descriptions_.feature == 'Image Classification':
            return self._generate_report_for_image_classification(descriptions_)
        else:
            return {}

    def  _generate_report_for_object_detection(self, descriptions_: descriptions.Descriptions) -> \
        Dict[str, Dict[str, Union[int, List[float]]]]:
        objects = dict()
        for obj_class, obj_confidence in descriptions_.descriptions:
            if obj_class not in objects:
                objects[obj_class] = {
                    "freq": 1,
                    "confidences": [obj_confidence] 
                }
            else:
                objects[obj_class]["freq"] += 1
                objects[obj_class]["confidences"].append(obj_confidence)
        return objects

    def  _generate_report_for_image_classification(self,
        descriptions_: descriptions.Descriptions) -> Dict[str, float]:
        classes = dict()
        for image_class, class_confidence in descriptions_.descriptions:
            classes[image_class] = class_confidence
        return classes
