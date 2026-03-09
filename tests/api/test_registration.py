import pytest
from requests import Response

@pytest.mark.asyncio
async def test_successful_registration(test_client):
    session, base_url = test_client
    new_user = {
        "firstname": "Test",
        "lastname": "User",
        "username": "testuser",
        "password": "testpass123"
    }
    response: Response = session.post(
        f"{base_url}/register",
        json=new_user
    )
    assert response.status_code == 200
    assert response.json()["registration_success"] is True
    assert response.json()["error_msg"] is None

@pytest.mark.asyncio
async def test_failed_registration_existing_username(test_client):
    session, base_url = test_client
    existing_user = {
        "firstname": "Admin",
        "lastname": "User",
        "username": "admin",
        "password": "admin123"
    }
    response: Response = session.post(
        f"{base_url}/register",
        json=existing_user
    )
    assert response.status_code == 200
    assert response.json()["registration_success"] is False
    assert response.json()["error_msg"] == "Username is already in use"

@pytest.mark.asyncio
async def test_failed_registration_missing_fields(test_client):
    session, base_url = test_client
    incomplete_user = {
        "firstname": "Test",
        "username": "testuser"
    }
    response: Response = session.post(
        f"{base_url}/register",
        json=incomplete_user
    )
    assert response.status_code == 200
    assert response.json()["registration_success"] is False
    assert response.json()["error_msg"] == "Mandatory information missing"

@pytest.mark.asyncio
async def test_failed_registration_invalid_data(test_client):
    session, base_url = test_client
    invalid_user = {
        "firstname": "",
        "lastname": "",
        "username": "a" * 1000,
        "password": "short"
    }
    response: Response = session.post(
        f"{base_url}/register",
        json=invalid_user
    )
    assert response.status_code == 200
    assert response.json()["registration_success"] is False
    assert response.json()["error_msg"] is not None