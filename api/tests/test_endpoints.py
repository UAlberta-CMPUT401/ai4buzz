import pytest
import gzip
import base64
import os
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
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    response = client.post(
        f"/getImageFeatures?access_token={signup_response.json()['access_token']}", files={"files": "unexpected format"}
    )
    assert response.status_code == 422

def test_get_image_features_success(test_db):
    """ Should return a full analysis on the uploaded image
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './test.jpeg')
    response = client.post(
        f"/getImageFeatures?access_token={signup_response.json()['access_token']}", files={"files": ("test.jpeg", open(file_path, 'rb'), 'image/jpeg')}
    )
    assert response.status_code == 200

def test_get_image_feature_by_feature_param_success(test_db):
    """ Should return just the analysis for color scheme as specified in the feature query param
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './test.jpeg')
    response = client.post(
        f"/getImageFeatures?access_token={signup_response.json()['access_token']}&features=color_scheme_analysis", files={"files": ("test.jpeg", open(file_path, 'rb'), 'image/jpeg')}
    )
    analysis_results = response.json()
    assert "feature_analysis_results" in analysis_results
    assert "color_scheme_analysis" in analysis_results["feature_analysis_results"][0]
    assert response.status_code == 200

def test_get_image_features_base_64_success(test_db):
    """ Should return a full analysis on the uploaded gzipped base64 image
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './img_string.txt')
    with open(file_path, 'r') as f:
        img_str = f.readline()
        data = bytes(img_str, "utf-8")
        s_out = gzip.compress(data)
        b64_img = str(base64.b64encode(s_out), 'ascii')

        response = client.post(
            f"/getImageFeaturesBase64?access_token={signup_response.json()['access_token']}", json=[{"id": "test_image", "img64": b64_img}]
        )
        response.json() == ''
        assert response.status_code == 200

def test_get_image_features_base_64_by_feature_param_invalid_gzipped_base64_img_str(test_db):
    """ should return status code 400 for invalid gzipped base64 image string
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './img_string.txt')
    with open(file_path, 'r') as f:
        response = client.post(
            f"/getImageFeaturesBase64?access_token={signup_response.json()['access_token']}", json=[{"id": "test_image", "img64": "invalid_img_str"}]
        )
        assert response.status_code == 400

def test_get_image_features_base_64_by_feature_param_invalid_feature_string_list(test_db):
    """ should return status code 400 for invalid image features string
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './img_string.txt')
    with open(file_path, 'r') as f:
        img_str = f.readline()
        data = bytes(img_str, "utf-8")
        s_out = gzip.compress(data)
        b64_img = str(base64.b64encode(s_out), 'ascii')

        response = client.post(
            f"/getImageFeaturesBase64?access_token={signup_response.json()['access_token']}&features=invalid_list_item,thing2", json=[{"id": "test_image", "img64": b64_img}]
        )
        assert response.status_code == 400

def test_get_image_features_base_64_by_feature_param_success(test_db):
    """ Should return just the analysis for color scheme as specified in the feature query param from a gzipped base64 image string
    """
    signup_response = client.post(
        "/users", json={"email": "test@test.com", "password": "password"}
    )
    test = os.path.dirname(__file__)
    file_path = os.path.join(test, './img_string.txt')
    with open(file_path, 'r') as f:
        img_str = f.readline()
        data = bytes(img_str, "utf-8")
        s_out = gzip.compress(data)
        b64_img = str(base64.b64encode(s_out), 'ascii')

        response = client.post(
            f"/getImageFeaturesBase64?access_token={signup_response.json()['access_token']}&features=color_scheme_analysis", json=[{"id": "test_image", "img64": b64_img}]
        )
        analysis_results = response.json()
        assert "feature_analysis_results" in analysis_results
        assert "color_scheme_analysis" in analysis_results["feature_analysis_results"][0]
        assert response.status_code == 200
