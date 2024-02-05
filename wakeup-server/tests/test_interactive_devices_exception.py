import pytest


def test_empty_name(client):
    response = client.post("/interactive_devices", json={"name": "", "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        name = obj['name']
    msg = e.value.args[0]
    assert 'NoneType' in msg


def test_too_long_name(client):
    response = client.post("/interactive_devices", json={"name": "a"*1000, "type": "SOUND"})
    obj = response.get_json()
    with pytest.raises(Error) as e:
        name = obj['name']
        assert name == "a"*1000


def test_duplicate_name(client):
    response = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    with pytest.raises(IntegrityError) as e:
        response2 = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    msg =  e.value.args[0]
    assert msg == "Device already exists"


def test_too_long_type(client):
    response = client.post("/interactive_devices", json={"type": "sound"})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _type = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg


def test_empty_type(client):
    response = client.post("/interactive_devices", json={"type": ""})
    obj = response.get_json()
    with pytest.raises(TypeError) as e:
        _type = obj['type']
    msg = e.value.args[0]
    assert 'NoneType' in msg


