from fastapi import FastAPI, Depends, status, Response, HTTPException, File, UploadFile
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image

from api import schemas
from api.models.image_describer import ImageDescriber
from api.database import engine, SessionLocal
from api.database import models
from api.utils.hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    """ database connection middleware
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/getImageFeatures', response_model=schemas.ImageDescription)
async def get_features(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return Response(content='File type must be jpeg or png', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    image = Image.open(BytesIO(await file.read()))
    image_describer = ImageDescriber()
    image_features = image_describer.get_features_by_image(image)
    return image_features

@app.post('/users')
def create_user(request: schemas.User, db: Session = Depends(get_db) ):
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if db_user:
        return Response(content='email already exists', status_code=status.HTTP_400_BAD_REQUEST)
    new_user = models.User(email = request.email, hashed_password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
