import pytest


def test_create_user(client):
    response = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    user = response.get_json()
    id = user['id']
    first_name = user['first_name']
    last_name = user['last_name']
    gosh_id = user['gosh_id']
    assert response.status_code == 200 and len(id) == 36 and first_name == "test" and last_name == "user" and gosh_id == "001"


def test_get_user_by_id(client):
    obj = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"}).get_json()
    response = client.get("/users/"+obj['id'])
    user = response.get_json()
    assert response.status_code == 200 and obj['first_name'] == user['first_name'] and obj['last_name'] == user['last_name'] and obj['gosh_id'] == user['gosh_id']


def test_get_user(client):
    obj1 = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"}).get_json()
    obj2 = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "002"}).get_json()
    response = client.get("/users")
    user_list = response.get_json()
    id_list = [user['id'] for user in user_list]
    assert response.status_code == 200 and obj1['id'] in id_list and obj2['id'] in id_list


def test_empty_first_name(client):
    response = client.post("/users", json = {"first_name": "", "last_name": "user", "gosh_id": "001"})
    assert b"Unknown error" in response.data


def test_empty_last_name(client):
    response = client.post("/users", json = {"first_name": "test", "last_name": "", "gosh_id": "001"})
    assert b"Unknown error" in response.data


@pytest.mark.skip(reason="Not implemented")
def test_empty_gosh_id(client):
    response = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": ""})
    assert b"Unknown error" in response.data


@pytest.mark.skip(reason="Not implemented")
def test_duplicate_name(client):
    response = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    response2 = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "002"})
    assert b"User already exists" in response2.data


def test_duplicate_gosh_id(client):
    response = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    response2 = client.post("/users", json = {"first_name": "test2", "last_name": "user2", "gosh_id": "001"})
    assert b"A user with this GOSH ID already exists" in response2.data


def test_delete_user(client):
    obj = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"}).get_json()
    response = client.delete("/users/"+obj['id'])
    assert b"User deleted successfully" in response.data


def test_update_user(client):
    obj = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"}).get_json()
    response = client.put("/users/"+obj['id'], json = {"first_name": "update", "last_name": "modified", "gosh_id": "XXX"})
    assert b"User updated successfully" in response.data