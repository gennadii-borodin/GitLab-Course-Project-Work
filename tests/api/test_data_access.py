import pytest
from requests import Response

@pytest.mark.asyncio
async def test_get_things_public(test_client):
    session, base_url = test_client
    response: Response = session.get(f"{base_url}/things")
    assert response.status_code == 200
    assert isinstance(response.json()["things"], list)

@pytest.mark.asyncio
async def test_get_current_user_unauthenticated(test_client):
    session, base_url = test_client
    response: Response = session.get(f"{base_url}/user/current")
    assert response.status_code == 401
    assert response.json() == {'Access denied'}

@pytest.mark.asyncio
async def test_get_user_by_username_unauthenticated(test_client):
    session, base_url = test_client
    response: Response = session.get(f"{base_url}/user/admin")
    assert response.status_code == 401
    assert response.json() == {'Access denied'}

@pytest.mark.asyncio
async def test_get_current_user_authenticated(test_client, auth_data):
    session, base_url = test_client
    # Login first
    login_response = session.post(
        f"{base_url}/login",
        json=auth_data
    )
    assert login_response.json()["login_success"] is True

    # Then get current user
    response: Response = session.get(f"{base_url}/user/current")
    assert response.status_code == 200
    assert response.json() is not None

@pytest.mark.asyncio
async def test_get_user_by_username_as_admin(test_client, auth_data):
    session, base_url = test_client
    # Login as admin
    login_response = session.post(
        f"{base_url}/login",
        json=auth_data
    )
    assert login_response.json()["login_success"] is True

    # Get user info
    response: Response = session.get(f"{base_url}/user/admin")
    assert response.status_code == 200
    assert response.json() is not None