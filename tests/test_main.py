import pytest
from unittest.mock import patch
from main import app
from tests.data import token_json, mock_users
from fastapi.testclient import TestClient   


client = TestClient(app)


@pytest.mark.asyncio
async def test_get_users_success():
    # Mock the dependency `get_authenticated_user`
    # Assume the authenticated user is a dummy UUID for testing purposes
    
    # Patch both `decode_token` and `get_all_users`
    with patch("utils.jwt_handler.decode_token", return_value=token_json), \
         patch("services.user_services.get_all_users_db", return_value=mock_users):
        
        headers = {
            "Authorization": "Bearer ahjfkodsljh2o3o23"
        }
        response = client.get("/get_users", headers=headers)
        # Assert that the response is correct
        assert response.status_code == 200
        assert len(response.json()) == 4
        assert response.json()[0]["name"] == "Govind"
        assert response.json()[1]["email"] == "Narendra@gmail.com"


@pytest.mark.asyncio
async def test_get_users_failure():
    # Mock the `get_authenticated_user` and force `get_all_users` to raise an exception
    with patch("utils.jwt_handler.decode_token", return_value=token_json), \
         patch("services.user_services.get_all_users_db", side_effect=Exception("Database error")):
        
        headers = {
            "Authorization": "Bearer ahjfkodsljh2o3o23"
        }
        response = client.get("/get_users", headers=headers)
        
        # Assert the response is a 500 error as expected when there's an exception
        assert response.status_code == 500
        assert response.json() == {"detail": "Error getting users"}


@pytest.mark.asyncio
async def test_get_users_decode_empty():
    # Mock the `get_authenticated_user` and force `get_all_users` to raise an exception
    with patch("utils.jwt_handler.decode_token", return_value={}), \
         patch("services.user_services.get_all_users_db", return_value=mock_users):
        
        headers = {
            "Authorization": "Bearer ahjfkodsljh2o3o23"
        }
        response = client.get("/get_users", headers=headers)
        
        # Assert the response is a 500 error as expected when there's an exception
        assert response.status_code == 401
        assert response.json() == {'detail': 'Malformed token'}


@pytest.mark.asyncio
async def test_get_users_by_id():
    # Mock the dependency `get_authenticated_user`
    # Assume the authenticated user is a dummy UUID for testing purposes
    
    # Patch both `decode_token` and `get_user_by_id`
    with patch("utils.jwt_handler.decode_token", return_value=token_json), \
         patch("services.user_services.get_user_by_id_into_db", return_value=mock_users[0]):
        
        headers = { 
             "Authorization": "Bearer ahjfkodsljh2o3o23"
        }

        response = client.get(f"/users/{mock_users[0].user_id}", headers=headers)
        # Assert that the response is correct
        assert response.status_code == 200
        assert response.json()["name"] == "Govind"
        assert response.json()["email"] == "govind@gmail.com"


@pytest.mark.asyncio
async def test_get_users_by_id_not_found():
    # Mock the dependency `get_authenticated_user`
    # Assume the authenticated user is a dummy UUID for testing purposes
    
    # Patch both `decode_token` and `get_user_by_id`
    with patch("utils.jwt_handler.decode_token", return_value=token_json), \
         patch("services.user_services.get_user_by_id_into_db", return_value=None):
        
        headers = { 
             "Authorization": "Bearer ahjfkodsljh2o3o23"
        }           
        response = client.get(f"/users/123e4567-e89b-12d3-a456-426614174000", headers=headers)
        # Assert that the response is correct
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found for id: 123e4567-e89b-12d3-a456-426614174000"} 


@pytest.mark.asyncio
async def test_delete_user_success():
    # Mock the dependency `get_authenticated_user`
    # Assume the authenticated user is a dummy UUID for testing purposes
    
    # Patch both `decode_token` and `delete_user_by_id`
    with patch("utils.jwt_handler.decode_token", return_value=token_json), \
         patch("routes.user_routes.delete_user_by_id", return_value=True):
        
        headers = { 
             "Authorization": "Bearer ahjfkodsljh2o3o23"
        }         
        response = client.delete("/user", headers=headers)
        # Assert that the response is correct
        assert response.status_code == 200
        assert response.json() == {"message": "User deleted successfully", "user_id": token_json["user_id"]}
