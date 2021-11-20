"""Contains the ImageDescriber class.

This class is used to describe a givem image by running various models on the image."""
import dataclasses
from typing import Any, Dict, List, Tuple
from concurrent.futures import ProcessPoolExecutor

from api.image_features.image_feature_model_factory import ImageFeatureModelFactory
from api.image_features.report_generator import ReportGenerator


@dataclasses.dataclass(frozen=True)
class ImageInfo:
    id: str
    pil_image: Any
    image_features: Tuple[str] = ('color_scheme_analysis', 'object_detection',
                                 'image_classification', 'sentiment_analysis',
                                 'text_recognition', 'face_analysis'
    )


class ImageDescriber:
    """Does all feature analysis on an image."""
    _image_feature_model_factory: ImageFeatureModelFactory
    _report_generator: ReportGenerator
    _process_pool_executor: ProcessPoolExecutor

    def __init__(self, image_feature_model_factory_: ImageFeatureModelFactory,
        report_generator_: ReportGenerator, process_pool_executor_: ProcessPoolExecutor) -> None:
        self._image_feature_model_factory = image_feature_model_factory_
        self._report_generator = report_generator_
        self._process_pool_executor = process_pool_executor_

    def get_features_by_image(self, image_infos: List[ImageInfo]) -> Dict[str, Any]:
        feature_analysis_results = []
        for image_info in image_infos:
            features_analyses = self._analyze_image(image_info)
            feature_analysis_results.append(features_analyses)

        collage_generator = self._image_feature_model_factory.create_and_get_feature_model('collage')
        collage = collage_generator.generate([image_info.pil_image for image_info in image_infos])
        collage_image_string = self._report_generator.generate_collage_report(collage)

        return {
            "feature_analysis_results": feature_analysis_results,
            "collage_image_string": collage_image_string
        }

    def _analyze_image(self, image_info: ImageInfo) -> Dict[str, Any]:
        features_analyses = {'id': image_info.id}
        with self._process_pool_executor as pool:
            image_feature_futures = {}
            for image_feature in image_info.image_features:
                image_feature_model = self._image_feature_model_factory\
                    .create_and_get_feature_model(image_feature)
                image_feature_future = pool.submit(
                    image_feature_model.get_descriptions, image_info.pil_image
                )
                image_feature_futures[image_feature] = image_feature_future
            
            for image_feature, image_feature_future in image_feature_futures.items():
                image_feature_description = image_feature_future.result()
                image_feature_report = self._report_generator.generate_report(image_feature_description)
                features_analyses[image_feature] = image_feature_report
        return features_analyses
