import pytest

def test_create_device(client):
    response = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    obj = response.get_json()
    id = obj['id']
    name = obj['name']
    _type = obj['type']
    assert response.status_code == 201 and len(id) == 36 and name == "test_1" and _type == "SOUND"

    return obj


def test_get_device_by_id(client):
    obj = test_create_device(client)
    response = client.get("/interactive_devices/"+obj['id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['id'] == device['id'] and obj['name'] == device['name'] and obj['type'] == device['type']


def test_get_device(client):
    obj1 = test_create_device(client)
    obj2 = test_create_device(client)

    response = client.get("/interactive_devices")
    device_list = response.get_json()
    id_list = [device['id'] for device in device_list]
    assert response.status_code == 200 and obj1['id'] in id_list and obj2['id'] in id_list


@pytest.mark.skip(reason="Not implemented")
def test_empty_name(client):
    response = client.post("/interactive_devices", json={"name": "", "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]
    assert 'NoneType' in msg


@pytest.mark.skip(reason="Not implemented")
def test_too_long_name(client):
    response = client.post("/interactive_devices", json={"name": "a"*1000, "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]
    assert 'NoneType' in msg


@pytest.mark.skip(reason="Not implemented")
def test_duplicate_name(client):
    response = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    response2 = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    assert b"Device already exists" in response2.data


def test_too_long_type(client):
    response = client.post("/interactive_devices", json={"type": "sound"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _ = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg


def test_empty_type(client):
    response = client.post("/interactive_devices", json={"type": ""})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _type = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg