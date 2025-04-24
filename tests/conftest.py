import os
import pytest
from app import create_app
from app.database import db
from app.config import Config
from flask.testing import FlaskClient

@pytest.fixture
def app():
    config = Config()
    config.TESTING = True
    config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    config.RATELIMIT_ENABLED = False
    config.REDIS_URL = os.getenv("REDIS_URL_DEVELOPMENT", "redis://localhost:6379/0")

    app = create_app(config)
    print(app.config.values())

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # Create a new user
    client.post("/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "buyer"
    })

    # Login for get the token
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    print(response)
    token = response.get_json()["token"]
    return token
