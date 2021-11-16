from typing import *
from fastapi import FastAPI, Depends, status, Response, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image
import base64

from api import schemas
from api.image_features.image_describer import ImageDescriber
from api.database import engine, SessionLocal
from api.database import models
from api.utils.hashing import Hash, pwd_cxt
from api.middleware.auth import verify_jwt
from api.utils.auth import sign_jwt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://[2605:fd00:4:1001:f816:3eff:fe67:1ff9]', 'http://localhost', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """ Create user, or sign up, endpoint

    Args:
        request (schemas.User): Body of request containing email and password
        db (Session): Middleware function to establish db connection

    Returns:
        JSONResponse: JSON response containing token
    """ 
    # check if user exists
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if db_user:
        return Response(content='email already exists', status_code=status.HTTP_400_BAD_REQUEST)

    # create and commit new user with hashed password
    new_user = models.User(email = request.email, hashed_password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # generate and return JWT
    access_token = sign_jwt({"user": request.email})
    response_data = {'access_token': access_token}
    return JSONResponse(content=jsonable_encoder(response_data))

@app.post('/token')
def login_user(user: schemas.User, db: Session = Depends(get_db)):
    """ Token, or login, endpoint

    Args:
        user (schemas.User): Body of request containing email and password
        db (Session): Middleware function to establish db connection

    Returns:
        JSONResponse: JSON response containing token
    """
    # check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        return Response(content='email doesn\'t exist', status_code=status.HTTP_404_NOT_FOUND)
    
    # check password 
    verified = pwd_cxt.verify(user.password, db_user.hashed_password)
    if not verified:
        return Response(content='Wrong password', status_code=status.HTTP_401_UNAUTHORIZED)
    
    # generate and return JWT
    access_token = sign_jwt({"user": user.email})
    response_data = {'access_token': access_token}
    return JSONResponse(content=jsonable_encoder(response_data))

@app.post('/getImageFeatures', response_model=schemas.GetImageFeaturesResponse)
async def get_features(files: List[UploadFile] = File(...), user: str = Depends(verify_jwt)):
    """ Endpoint to get analysis of multiple images

    Args:
        files (List[UploadFile], optional): Array of UploadFiles that are the images to analyze
        user (str): [description]. Defaults to Depends(verify_jwt).

    Returns:
        JSONResponse: JSON response containing analysis summary
    """
    # read image file bytes into array
    image_bytes = []
    for file in files:
        # ensure files are images
        extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not extension:
            return Response(content='File type must be .jpeg, .jpg or .png', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        image_bytes.append({"id": file.filename , "bytes": Image.open(BytesIO(await file.read())).convert('RGB')})

    # perform and return analysis
    image_describer = ImageDescriber()
    image_features = image_describer.get_features_by_image(image_bytes)
    return JSONResponse(content=jsonable_encoder(image_features))

@app.post('/getImageFeaturesBase64')
async def get_features(files: List[schemas.Base64Image], user: str = Depends(verify_jwt)):
    """ Endpoint to get analysis of multiple base64 images

    Args:
        files (List[schemas.Base64Image]): List of Base64Images
        user (str): [description]. Defaults to Depends(verify_jwt).

    Returns:
        JSONResponse: JSON response containing analysis summary
    """
    # read base64 into images array
    images = []
    for file in files:
        try:
            image_bytes = Image.open(BytesIO(base64.b64decode(file.img64))).convert('RGB') 
            images.append({"id": file.id, "bytes": image_bytes})
        except:
            return Response(content=f'{file.id} base64 image string could not be processed', status_code=status.HTTP_400_BAD_REQUEST)

    # perform and return analysis
    image_describer = ImageDescriber()
    image_features = image_describer.get_features_by_image(images)
    return JSONResponse(content=jsonable_encoder(image_features))
