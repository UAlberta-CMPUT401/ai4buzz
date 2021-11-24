""" The main filoe that is the entry for the program."""

from typing import *
from concurrent.futures import ProcessPoolExecutor
from fastapi import FastAPI, Depends, status, Response, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image
import base64
import gzip

from api import schemas
from api.image_features.image_describer import ImageDescriber, ImageInfo
from api.image_features.report_generator import ReportGenerator
from api.image_features.image_feature_model_factory import ImageFeatureModelFactory
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

@app.post('/users', response_model=schemas.response.AccessToken)
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

@app.post('/token', response_model=schemas.response.AccessToken)
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
async def get_features(features: str = None, files: List[UploadFile] = File(...), user: str = Depends(verify_jwt)):
    """ Endpoint to get analysis of multiple images

    Args:
        features (str): List of features to be extracted as a comma separated string
        files (List[UploadFile], optional): Array of UploadFiles that are the images to analyze
        user (str): [description]. Defaults to Depends(verify_jwt).

    Returns:
        JSONResponse: JSON response containing analysis summary
    """
    # check for types of analysis to perform
    requested_features = None
    if features:
        requested_features = tuple(features.split(','))
        supported_feature_analysis = ImageInfo.image_features
        for feature in requested_features:
            if feature not in supported_feature_analysis:
                return Response(content=f'\'{feature}\' analysis not supported', status_code=status.HTTP_400_BAD_REQUEST)

    # read image file bytes into array
    image_infos = []
    for file in files:
        # ensure files are images
        extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not extension:
            return Response(content='File type must be .jpeg, .jpg or .png', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if requested_features == None:
            image_infos.append(
                ImageInfo(id=file.filename, pil_image=Image.open(BytesIO(await file.read())).convert('RGB'))
            )
        else:
            image_infos.append(
                ImageInfo(id=file.filename, pil_image=Image.open(BytesIO(await file.read())).convert('RGB'), image_features=requested_features)
            )

    # perform and return analysis
    image_describer = ImageDescriber(ImageFeatureModelFactory(), ReportGenerator(), ProcessPoolExecutor())
    image_features = image_describer.get_features_by_image(image_infos)
    return JSONResponse(content=jsonable_encoder(image_features))

@app.post('/getImageFeaturesBase64', response_model=schemas.GetImageFeaturesResponse)
async def get_features(files: List[schemas.Base64Image], features: str = None, user: str = Depends(verify_jwt)):
    """ Endpoint to get analysis of multiple base64 images

    Args:
        features (str): List of features to be extracted as a comma separated string
        files (List[schemas.Base64Image]): List of Base64Images
        user (str): [description]. Defaults to Depends(verify_jwt).

    Returns:
        JSONResponse: JSON response containing analysis summary
    """
    # check for types of analysis to perform
    requested_features = None
    if features:
        requested_features = tuple(features.split(','))
        supported_feature_analysis = ImageInfo.image_features
        for feature in requested_features:
            if feature not in supported_feature_analysis:
                return Response(content=f'\'{feature}\' analysis not supported', status_code=status.HTTP_400_BAD_REQUEST)

    # read base64 into images array
    image_infos = []
    for file in files:
        try:
            image = file.img64
            gzipped_image = base64.b64decode(image)
            image_str = gzip.decompress(gzipped_image).decode("utf-8")
            image = Image.open(BytesIO(base64.b64decode(image_str))).convert('RGB') 
            if requested_features == None:
                image_infos.append(
                    ImageInfo(id=file.id, pil_image=image)
                )
            else:
                image_infos.append(
                    ImageInfo(id=file.id, pil_image=image, image_features=requested_features)
                )
        except Exception as e:
            print(e)
            return Response(content=f'{file.id} base64 image string could not be processed', status_code=status.HTTP_400_BAD_REQUEST)

    # perform and return analysis
    image_describer = ImageDescriber(ImageFeatureModelFactory(), ReportGenerator(), ProcessPoolExecutor())
    image_features = image_describer.get_features_by_image(image_infos)
    return JSONResponse(content=jsonable_encoder(image_features))
