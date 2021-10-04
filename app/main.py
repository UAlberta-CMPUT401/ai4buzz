from typing import Optional

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


from app.database import SessionLocal, engine
from app.database import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users")
def create_user(db: Session = Depends(get_db)):
    fake_hashed_password = "notreallyhashed"
    email = "testemail@test.com"
    db_user = models.User(email=email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user