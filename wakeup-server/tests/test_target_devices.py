import pytest


def test_create_device(client):
    response = client.post("/target_devices", json={"matter_id": "fake-matter-device", "name": "Fake Matter Device", "type": "switch"})
    obj = response.get_json()
    matter_id = obj['matter_id']
    name = obj['name']
    _type = obj['type']
    assert response.status_code == 201 and name == "Fake Matter Device" and _type == "switch"
    return obj