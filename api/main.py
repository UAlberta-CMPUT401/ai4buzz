from fastapi import FastAPI, Depends, status, Response, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image

from api import schemas
from api.image_features.image_describer import ImageDescriber
from api.database import engine, SessionLocal
from api.database import models
from api.utils.hashing import Hash, pwd_cxt
from api.middleware.auth import verify_jwt
from api.utils.auth import sign_jwt

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

@app.post('/users')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if db_user:
        return Response(content='email already exists', status_code=status.HTTP_400_BAD_REQUEST)
    new_user = models.User(email = request.email, hashed_password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/token')
def login_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        return Response(content='email doesn\'t exist', status_code=status.HTTP_404_NOT_FOUND)
    verified = pwd_cxt.verify(user.password, db_user.hashed_password)
    if not verified:
        return Response(content='Wrong password', status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = sign_jwt({"user": user.email})
    response_data = {'access_token': access_token}
    return JSONResponse(content=jsonable_encoder(response_data))

@app.post('/getImageFeatures', response_model=schemas.ImageDescription)
async def get_features(file: UploadFile = File(...), user: str = Depends(verify_jwt)):
    print('got here', user)
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return Response(content='File type must be jpeg or png', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    image = Image.open(BytesIO(await file.read()))
    image_describer = ImageDescriber()
    image_features = image_describer.get_features_by_image(image)
    return image_features
