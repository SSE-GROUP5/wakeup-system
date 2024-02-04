

def test_create_device(client):
    response = client.post("/interactive_devices", json={"type": "SOUND"})
    assert response.status_code == 201
    obj = response.get_json()
    id = obj['id']
    _type = obj['type']
    
    assert len(id) == 36
    assert _type == "SOUND"