import pytest


def test_create_device(client):
    response = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "switch"})
    obj = response.get_json()
    matter_id = obj['matter_id']
    name = obj['name']
    _type = obj['type']
    assert response.status_code == 201 and len(matter_id) == 18 and matter_id == "fake-matter-device" and name == "Fake Matter Device" and _type == "switch"

    return obj


def test_get_device_by_id(client):
    obj = test_create_device(client)
    response = client.get("/target_devices/"+obj['matter_id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['matter_id'] == device['matter_id'] and obj['name'] == device['name'] and obj['type'] == device['type']


def test_get_device(client):
    obj1 = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "switch"}).get_json()
    obj2 = client.post("/target_devices", json={"matter_id": "fake-matter-device 2", "name": "Fake Matter Device 2", "type": "switch"}).get_json()

    response = client.get("/target_devices")
    device_list = response.get_json()
    id_list = [device['matter_id'] for device in device_list]
    assert response.status_code == 200 and obj1['matter_id'] in id_list and obj2['matter_id'] in id_list


@pytest.mark.skip(reason="Not implemented")
def test_empty_id(client):
    obj = client.post("/target_devices", json={"matter_id": "", "name": "Fake Matter Device", "type": "switch"}).get_json()
    with pytest.raises(TypeError) as e:
        matter_id = obj['matter_id']
    msg = e.value.args[0]



@pytest.mark.skip(reason="Not implemented")
def test_empty_name(client):
    obj = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "", "type": "switch"}).get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]



@pytest.mark.skip(reason="Not implemented")
def test_empty_type(client):
    obj = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": ""}).get_json()
    with pytest.raises(TypeError) as e:
        type = obj['type']
    msg = e.value.args[0]



@pytest.mark.skip(reason="Not implemented")
def test_too_long_id(client):
    obj = client.post("/target_devices", json={"matter_id": "a"*1000, "name": "Fake Matter Device", "type": ""}).get_json()
    with pytest.raises(TypeError) as e:
        matter_id = obj['matter_id']
    msg = e.value.args[0]



@pytest.mark.skip(reason="Not implemented")
def test_too_long_name(client):
    obj = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "a"*1000, "type": "switch"}).get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]



@pytest.mark.skip(reason="Not implemented")
def test_too_long_type(client):
    obj = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "a"*1000}).get_json()
    with pytest.raises(TypeError) as e:
        type = obj['type']
    msg = e.value.args[0]



@pytest.mark.skip(reason="server response needs change, it wrongly returns None")
def test_duplicate_id(client):
    client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "switch"}).get_json()
    response2 = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device 2", "type": "switch"}).get_json()
    assert b"Device already exists" in response2.data


@pytest.mark.skip(reason="Not implemented")
def test_duplicate_name(client):
    client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "switch"}).get_json()
    response2 = client.post("/target_devices", json={"matter_id": "fake-matter-device-2", "name": "Fake Matter Device", "type": "switch"}).get_json()
    assert b"Device already exists" in response2.data
