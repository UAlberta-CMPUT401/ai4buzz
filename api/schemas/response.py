from typing import List
from pydantic import BaseModel

from api import image_features

class ImageDescription(BaseModel):
    id: str
    sentiment_analysis: dict
    color_scheme_analysis: dict
    object_detection: dict
    image_classification: dict
    text_recognition: str
    face_analysis: dict

class GetImageFeaturesResponse(BaseModel):
    feature_analysis_results: dict
    collage_image_string: str
