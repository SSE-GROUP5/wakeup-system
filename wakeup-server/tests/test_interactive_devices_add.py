

def test_create_device(client):
    response = client.post("/interactive_devices", json={"name": "test_1", "type": "SOUND"})
    obj = response.get_json()
    id = obj['id']
    name = obj['name']
    _type = obj['type']
    assert response.status_code == 201 and len(id) == 36 and name == "test_1" and _type == "SOUND"

    return obj
