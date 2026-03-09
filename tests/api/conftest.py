import os
import pytest
import requests
from requests.auth import HTTPBasicAuth

@pytest.fixture(scope="session")
def test_client():
    base_url = os.getenv('TEST_BASE_URL', 'http://localhost:8080')
    session = requests.Session()
    yield session, base_url
    session.close()

@pytest.fixture
def auth_data():
    return {
        "username": "admin",
        "password": "admin123"
    }

@pytest.fixture
def invalid_auth_data():
    return {
        "username": "invalid",
        "password": "wrong"
    }

@pytest.fixture
def test_data():
    return {
        "valid_user": {
            "firstname": "Test",
            "lastname": "User",
            "username": "testuser",
            "password": "testpass123"
        },
        "invalid_user": {
            "firstname": "",
            "lastname": "",
            "username": "a" * 1000,
            "password": "short"
        }
    }