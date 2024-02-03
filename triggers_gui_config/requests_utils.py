import requests

def test_connection(wakeup_server_url):
    try:
        # Attempt to connect to the server
        requests.get(f"{wakeup_server_url}")
        return True
    except requests.exceptions.RequestException as e:
        return False
      
def create_interactive_device(wakeup_server_url, device_type):
    try:
        response = requests.post(f"{wakeup_server_url}/interactive_devices", json={"type": device_type})
        if response.status_code == 201:
            print(f"Device created successfully. ID: {response.json()['id']}")
            return response.json()["id"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None