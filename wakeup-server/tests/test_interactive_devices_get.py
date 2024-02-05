import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from test_interactive_devices_add import test_create_device

def test_get_device_by_id(client):
    obj1 = test_create_device(client)
    obj2 = test_create_device(client)

    response = client.get("/interactive_devices")
    device_list = response.get_json()
    id_list = [device['id'] for device in device_list]
    assert response.status_code == 200 and obj1['id'] in id_list and obj2['id'] in id_list