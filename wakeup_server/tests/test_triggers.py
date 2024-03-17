import pytest

def test_create_trigger(client):
    response = client.post("/triggers", json={"name": "test_create_device", "type": "vision_morse"})
    obj = response.get_json()
    assert response.status_code == 201 and len(obj['id']) == 36 and obj['name'] == "test_create_device" and obj['type'] == "vision_morse"


def test_get_device_by_id(client):
    res = response = client.post("/triggers", json={"name": "test_get_device_by_id", "type": "vision_morse"})
    obj = res.get_json()
    response = client.get("/triggers/"+obj['id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['id'] == device['id'] and obj['name'] == device['name'] and obj['type'] == device['type']


def test_get_device(client):
    res1 = response = client.post("/triggers", json={"name": "test_get_device_1", "type": "vision_morse"})
    res2 = response = client.post("/triggers", json={"name": "test_get_device_2", "type": "vision_morse"})
    obj1 = res1.get_json()
    obj2 = res2.get_json()

    response = client.get("/triggers")
    device_list = response.get_json()
    id_list = [device['id'] for device in device_list]
    assert response.status_code == 200 and obj1['id'] in id_list and obj2['id'] in id_list


@pytest.mark.skip(reason="need ZMQ server")
def test_update_trigger(client):
    response1 = client.post("/triggers", json={"name": "test_update_trigger", "type": "vision_morse"})
    obj1 = response1.get_json()
    response2 = client.put("/triggers/"+obj1['id'], json={"name": "modified", "type": "vision_morse"})
    obj2 = response2.get_json()
    assert obj2['name'] == "modified"


@pytest.mark.skip(reason="Not implemented")
def test_empty_name(client):
    response = client.post("/triggers", json={"name": "", "type": "vision_morse"})
    assert b"No name provided" in response.data


def test_name_with_space(client):
    response = client.post("/triggers", json={"name": "a b c", "type": "vision_morse"})
    assert b"Device name cannot contain spaces" in response.data


def test_duplicate_name(client):
    response = client.post("/triggers", json={"name": "test_1", "type": "vision_morse"})
    response2 = client.post("/triggers", json={"name": "test_1", "type": "vision_morse"})
    assert b"Device name already used" in response2.data


@pytest.mark.skip(reason="Not implemented")
def test_illegal_type(client):
    response = client.post("/triggers", json={"name": "test_illegal_type", "type": "cheems"})
    assert b"Unknown error" in response.data


@pytest.mark.skip(reason="Not implemented")
def test_empty_type(client):
    response = client.post("/triggers", json={"name": "test_empty_type", "type": ""})
    assert b"No type provided" in response.data
   