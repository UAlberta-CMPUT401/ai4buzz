import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PIL import Image

from api.main import app, get_db
from api.database import Base

# setup mock local test db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# override db middleware
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

# setup and clean up database
@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_signup_user_success(test_db):
    """ should sign up user and return access token
    """
    response = client.post(
        "/users", json={"email": "test@test.com", "password": "password123"}
    )
    assert response.json()['access_token'] != None
    assert response.status_code == 200

def test_signup_user_failure(test_db):
    """ should not sign up a user and return an error indicating email exists
    """
    client.post(
        "/users", json={"email": "test@test.com", "password": "password123"}
    )
    response = client.post(
        "/users", json={"email": "test@test.com", "password": "password123"}
    )
    assert response.text == 'email already exists'
    assert response.status_code == 400

def test_login_user_success(test_db):
    """ should login user by returning an access token
    """
    client.post(
        "/users", json={"email": "test@test.com", "password": "password123"}
    )
    response = client.post(
        "/token", json={"email": "test@test.com", "password": "password123"}
    )
    assert response.json()['access_token'] != None
    assert response.status_code == 200

def test_login_user_wrong_password(test_db):
    """ should not login a user with a wrong password
    """
    client.post(
        "/users", json={"email": "test@test.com", "password": "password123"}
    )
    response = client.post(
        "/token", json={"email": "test@test.com", "password": "wrongpassword"}
    )
    assert response.text == 'Wrong password'
    assert response.status_code == 401

def test_login_user_email_not_found(test_db):
    """ should login with email that doesn't exist
    """
    response = client.post(
        "/token", json={"email": "non_existent@test.com", "password": "wrongpassword"}
    )
    assert response.text == "email doesn't exist"
    assert response.status_code == 404

def test_get_image_features_invalid_access_token():
    """ Should return a 401 error for invalid access token
    """
    response = client.post(
        f"/getImageFeatures?access_token=invalid_access_token", files={"files": "unexpected format"}
    )
    assert response.status_code == 401

def test_get_image_features_invalid_access_token():
    """ Should return a 401 error for invalid access token
    """
    response = client.post(
        f"/getImageFeatures?access_token=invalid_access_token", files={"files": "unexpected format"}
    )
    assert response.status_code == 401

def test_get_image_features_invalid_format(test_db):
    """ Should return a 422 error for invalid file upload format
    """
    signup_response = client.post(
        "/users", json={"email": "non_existent@test.com", "password": "wrongpassword"}
    )
    response = client.post(
        f"/getImageFeatures?access_token={signup_response.json()['access_token']}", files={"files": "unexpected format"}
    )
    assert response.status_code == 422

def test_get_image_features_success(test_db):
    """ Should return a 401 error for invalid access token
    """
    signup_response = client.post(
        "/users", json={"email": "non_existent@test.com", "password": "wrongpassword"}
    )
    response = client.post(
        f"/getImageFeatures?access_token={signup_response.json()['access_token']}", files={"files": ("test.png", open('test.png', 'rb'), 'image/png')}
    )
    assert response.status_code == 200
