import json
from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal, engine
from app.model import User
from app.schemas import UserCreate
from app.auth.auth_handler import sign_jwt

import pytest

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(test_db):
    user_data = UserCreate(fullname="Test User", email="test@example.com", password="testpassword")
    user = User(**user_data.dict())
    test_db.add(user)
    test_db.commit()
    return user

def test_signup(client):
    response = client.post("/signup", json={"fullname": "John Doe", "email": "johndoe@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_signup_existing_email(client, test_user):
    response = client.post("/signup", json={"fullname": "John Doe", "email": test_user.email, "password": "secret"})
    assert response.status_code == 400 

def test_auth(client, test_user):
    response = client.post("/auth", json={"email": test_user.email, "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_auth_invalid_credentials(client):
    response = client.post("/auth", json={"email": "invalid@email.com", "password": "invalidpassword"})
    assert response.status_code == 401 

def test_validate_token(client, test_user):
    token = sign_jwt(test_user.email)
    response = client.post("/validate-token", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 200
    assert response.json() == {"data": "Token válido"}

def test_validate_token_invalid_token(client):
    response = client.post("/validate-token", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 403 

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Acesse /docs para visualizar a documentação"}
