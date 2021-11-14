from typing import List
from pydantic import BaseModel

from api import image_features

class ImageDescription(BaseModel):
    sentiment_analysis: dict
    color_scheme_analysis: dict
    object_detection: dict
    image_classification: dict
    text_recognition: str

class GetImageFeaturesResponse(BaseModel):
    feature_analysis_results: dict
    collage_image_string: str
