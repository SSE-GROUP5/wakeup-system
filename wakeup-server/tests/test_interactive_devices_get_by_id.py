import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from test_interactive_devices_add import test_create_device


def test_get_device_by_id(client):
    obj = test_create_device(client)
    response = client.get("/interactive_devices/"+obj['id'])
    device = response.get_json()
    assert response.status_code == 200 and obj['id'] == device['id'] and obj['name'] == device['name'] and obj['type'] == device['type']


