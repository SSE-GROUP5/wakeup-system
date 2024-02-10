import pytest

def test_create_trigger(client):
    response = client.post("/triggers", json={"name": "test_create_device", "type": "SOUND"})
    obj = response.get_json()
    target_id = obj['id']
    name = obj['name']
    _type = obj['type']
    assert response.status_code == 201 and len(target_id) == 36 and name == name and _type == "SOUND"



def test_get_device_by_id(client):
    res = response = client.post("/triggers", json={"name": "test_get_device_by_id", "type": "SOUND"})
    obj = res.get_json()
    response = client.get("/triggers/"+obj['id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['id'] == device['id'] and obj['name'] == device['name'] and obj['type'] == device['type']


def test_get_device(client):
    res1 = response = client.post("/triggers", json={"name": "test_get_device_1", "type": "SOUND"})
    res2 = response = client.post("/triggers", json={"name": "test_get_device_2", "type": "SOUND"})
    obj1 = res1.get_json()
    obj2 = res2.get_json()

    response = client.get("/triggers")
    device_list = response.get_json()
    id_list = [device['id'] for device in device_list]
    assert response.status_code == 200 and obj1['id'] in id_list and obj2['id'] in id_list


@pytest.mark.skip(reason="Not implemented")
def test_empty_name(client):
    response = client.post("/triggers", json={"name": "", "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]
    assert 'NoneType' in msg


@pytest.mark.skip(reason="Not implemented")
def test_too_long_name(client):
    response = client.post("/triggers", json={"name": "a"*1000, "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]
    assert 'NoneType' in msg


@pytest.mark.skip(reason="Not implemented")
def test_duplicate_name(client):
    response = client.post("/triggers", json={"name": "test_1", "type": "SOUND"})
    response2 = client.post("/triggers", json={"name": "test_1", "type": "SOUND"})
    assert b"Device already exists" in response2.data


def test_too_long_type(client):
    response = client.post("/triggers", json={"type": "sound"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _ = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg


def test_empty_type(client):
    response = client.post("/triggers", json={"type": ""})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _type = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg