from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash 


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/getImageFeatures')
def getFeatures():
    return {'Got Image Features'}


@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db) ):
    new_user = models.User(name= request.name, email = request.email, 
    password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user