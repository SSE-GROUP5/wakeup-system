

def test_empty_name(client):
    response = client.post("/interactive_devices", json={"name": "", "type": "SOUND"})
    obj = response.get_json()
    name = obj['name']
    assert name == ""


def test_too_long_name(client):
    response = client.post("/interactive_devices", json={"name": "a"*1000, "type": "SOUND"})
    obj = response.get_json()
    name = obj['name']
    assert name == "a"*1000


def test_too_long_type(client):
    response = client.post("/interactive_devices", json={"type": "sound"})
    obj = response.get_json()
    assert obj == None



def test_empty_type(client):
    response = client.post("/interactive_devices", json={"type": ""})
    obj = response.get_json()
    assert obj == None


