from pydantic import BaseModel

class ImageDescription(BaseModel):
    image_classification: list
    sentiment_analysis: dict
    color_scheme_analysis: dict
    object_detection: dict
