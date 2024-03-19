import pytest


def test_create_device(client):
    response = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device", "type": "switch"})
    obj = response.get_json()
    assert response.status_code == 201 and obj['matter_id'] == "switch.fake-matter-device" and obj['name'] == "Fake Matter Device" and obj['type'] == "switch"
  

def test_get_device_by_id(client):
    obj = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device", "type": "switch"}).get_json()
    response = client.get("/target_devices/"+obj['matter_id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['matter_id'] == device['matter_id'] and obj['name'] == device['name'] and obj['type'] == device['type']


def test_get_device(client):
    obj1 = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device", "type": "switch"}).get_json()
    obj2 = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device 2", "name": "Fake Matter Device 2", "type": "switch"}).get_json()

    response = client.get("/target_devices")
    device_list = response.get_json()
    id_list = [device['matter_id'] for device in device_list]
    assert response.status_code == 200 and obj1['matter_id'] in id_list and obj2['matter_id'] in id_list


def test_empty_id(client):
    response = client.post("/target_devices", json={"matter_id": None, "name": "Fake Matter Device", "type": "switch"})
    assert b"No matter id provided" in response.data


def test_empty_name(client):
    response = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": None, "type": "switch"})
    assert b"No device name provided" in response.data


def test_empty_type(client):
    response = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device", "type": None})
    assert b"No device type provided" in response.data


def test_duplicate_id(client):
    response1 = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device", "type": "switch"})
    response2 = client.post("/target_devices", json={"matter_id": "switch.fake-matter-device", "name": "Fake Matter Device 2", "type": "switch"})
    assert b"Device already exists" in response2.data
