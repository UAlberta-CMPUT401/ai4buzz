from pydantic import BaseModel

class ImageDescription(BaseModel):
    sentiment_analysis: dict
    color_scheme_analysis: dict
    object_detection: dict
