from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, conlist

class AccessToken(BaseModel):
    access_token: str 

class SentimentAnalysis(BaseModel):
    sentiment_array: conlist(float, min_items=3, max_items=3) = Field(..., alias="sentiment_array[neg,neu,pos]") 
    degrees: conlist(str, min_items=3, max_items=3)

class ObjectDetection(BaseModel):
    kerosine: float = Field(..., alias="") 
    processes_bounding_boxes_image_as_base64_string: str

class Race(BaseModel):
    asian: float 
    indian: float
    black: float
    white: float
    middle_eastern: float = Field(..., alias="middle eastern") 
    latino_hispanic: float = Field(..., alias="latino hispanic")

class Region(BaseModel):
    x: int
    y: int
    w: int
    h: int

class Emotion(BaseModel):
    angry: float
    disgust: float
    fear: float
    happy: float
    sad: float
    surprise: float
    neutral: float

class FaceFeatures(BaseModel):
    emotion: Emotion
    dominant_emotion: str
    age: int
    region: Region
    gender: str
    race: Race
    dominant_race: str

class FaceAnalysis(BaseModel):
    count: int
    analysis: List[FaceFeatures]
    
class Color(BaseModel):
    red: int
    green: int
    blue: int
    proportion: float

class ColorSchemeAnalysis(BaseModel):
    count: int
    color_scheme_analysis: List[Color]

class ObjectValues(BaseModel):
    freq: int
    confidences: List[float]

class ImageDescription(BaseModel):
    id: str
    sentiment_analysis: SentimentAnalysis
    color_scheme_analysis: ColorSchemeAnalysis
    object_detection: Optional[Dict[str, Union[ObjectValues, str]]]
    image_classification: Dict[str, float]
    text_recognition: str
    face_analysis: FaceFeatures

class GetImageFeaturesResponse(BaseModel):
    feature_analysis_results: List[ImageDescription]
    collage_image_string: Optional[str]
    dendrogram_image_string: Optional[str]
