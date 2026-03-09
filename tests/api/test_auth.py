import pytest
from requests import Response

@pytest.mark.asyncio
async def test_successful_login(test_client, auth_data):
    session, base_url = test_client
    response: Response = session.post(
        f"{base_url}/login",
        json=auth_data
    )
    assert response.status_code == 200
    assert response.json()["login_success"] is True
    assert "account" in session.cookies

@pytest.mark.asyncio
async def test_failed_login_invalid_password(test_client, invalid_auth_data):
    session, base_url = test_client
    invalid_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    response: Response = session.post(
        f"{base_url}/login",
        json=invalid_data
    )
    assert response.status_code == 200
    assert response.json()["login_success"] is False
    assert "account" not in session.cookies

@pytest.mark.asyncio
async def test_failed_login_nonexistent_user(test_client, invalid_auth_data):
    session, base_url = test_client
    response: Response = session.post(
        f"{base_url}/login",
        json=invalid_auth_data
    )
    assert response.status_code == 200
    assert response.json()["login_success"] is False
    assert "account" not in session.cookies

@pytest.mark.asyncio
async def test_failed_login_missing_data(test_client):
    session, base_url = test_client
    response: Response = session.post(
        f"{base_url}/login",
        json={}
    )
    assert response.status_code == 200
    assert response.json()["login_success"] is False
    assert "account" not in session.cookies