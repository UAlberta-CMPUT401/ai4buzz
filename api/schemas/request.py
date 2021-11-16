from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class Base64Image(BaseModel):
    id: str
    img64: str
