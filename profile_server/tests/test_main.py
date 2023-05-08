import pytest
import mongomock
import io
from unittest.mock import patch
import requests
import main

from .helpers import generate_access_token

@pytest.fixture()
def app():
    with patch.object(main, 'get_db_client', return_value=mongomock.MongoClient()):
        yield main.create_app()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def access_header():
    return {'Authorization': f"Bearer {generate_access_token(111)}"}

@pytest.fixture()
def access_header_2():
    return {'Authorization': f"Bearer {generate_access_token(222)}"}

#Test function to test the create_user function
def test_create_user(client, access_header):
    data = {"username" : "Amogus123"}
    response = client.post("/profile/create_user", json=data, headers=access_header)
    assert response.status_code == 200

# Test function to test if proper error is returned
def test_create_user_duplicate(client, access_header):
    data = {"username" : "Amogus123"}
    response = client.post("/profile/create_user", json=data, headers=access_header)
    assert response.status_code == 200

    response = client.post("/profile/create_user", headers=access_header)
    assert response.status_code == 400

#Test function to test update_user_pfp function
def test_update_user_pfp(client, access_header):
    data = {"username" : "Amogus123"}
    response = client.post("/profile/create_user", json=data, headers=access_header)
    data = {"pfp" : 1234}
    response = client.post("/profile/update_user_pfp", data=data, headers=access_header)
    assert response.status_code == 200

# If user doesn't yet exist, return error
def test_update_user_pfp_2(client, access_header):
    data = {"pfp" : 1234}
    response = client.post("/profile/update_user_pfp", data=data, headers=access_header)
    assert response.status_code == 404

def test_receive_user_data(client, access_header):
    data = {"username" : "Amogus123"}
    response = client.post("/profile/create_user", json=data, headers=access_header)
    assert response.status_code == 200

    response = client.get("/profile/get_user_info?user_id=111")
    assert response.status_code == 200
    assert response.json['user_id'] == 111
    assert response.json['user_name'] == "Amogus123"

# Test if following and unfollowing people work
def test_followers_flow(client, access_header, access_header_2):
    data = {"username" : "Amogus123"}
    response = client.post("/profile/create_user", json=data, headers=access_header)
    assert response.status_code == 200
    assert response.json['user_id'] == 111

    data = {"username" : "CatLover_1"}
    response = client.post("/profile/create_user", json=data, headers=access_header_2)
    assert response.status_code == 200
    assert response.json['user_id'] == 222

    data = {"user_to_follow" : 222}
    response = client.post("/profile/follow_user", json=data, headers=access_header)
    assert response.status_code == 200

    data = {"user_to_follow" : 333}
    response = client.post("/profile/follow_user", json=data, headers=access_header)
    assert response.status_code == 404

    response = client.get("/profile/get_followers?user_id=222")
    assert response.status_code == 200
    assert len(response.json['followers']) == 1

    response = client.get("/profile/get_follows?user_id=111")
    assert response.status_code == 200
    assert len(response.json['follows']) == 1

    data = {"user_to_unfollow" : 222}
    response = client.post("/profile/unfollow_user", json=data, headers=access_header)

    data = {"user_id" : 222}
    response = client.get("/profile/get_followers?user_id=222")
    assert response.status_code == 200
    assert len(response.json['followers']) == 0

    response = client.get("/profile/get_follows?user_id=111")
    assert response.status_code == 200
    assert len(response.json['follows']) == 0