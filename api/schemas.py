from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class ImageDescriptionResponse(BaseModel):
    image_classification: list
    sentiment_analysis: dict
    color_scheme_analysis: dict
    object_detection: dict
