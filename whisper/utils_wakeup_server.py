from requests import Session
from requests.exceptions import ConnectionError
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

client = Session()
client.headers.update({'Content-Type': 'application/json'})
client.headers.update({'Accept': 'application/json'})

def update_env_vars(config, msg):
    for key in config.keys():
        if key in msg:
            config[key] = msg[key]
            print(f'Updated {key} to {msg[key]}')
    with open('env_trigger.txt', 'w') as f:
        for key in config.keys():
            f.write(f'{key}={config[key]}\n')
    return config

def send_signal(num_action, config):
    print(config)
    data = {
        "id": str(config["ID"]),
        "action": 'sound_whisper',
        "num_actions": num_action
    }
    url = f"{config['WAKEUP_SERVER_URL']}/signals"
    try:
        response = client.post(f"{url}", json=data)
        print(response.content)
        print(response)
    except Exception as e:
        print(e)

def confirm_to_server(config):
    try:
        request = client.post(config["WAKEUP_SERVER_URL"]+"/triggers/confirm", json={'id': config["ID"]})
        print(request.status_code)
        if request.status_code == 200:
            print("Server confirmed")
        elif request.status_code == 404:
            print("Device not registered with server, please register the device first")
    except Exception as e:
        print(e)

def check_connection(config):
    try:
        response = client.get(config["WAKEUP_SERVER_URL"], timeout=1)
        if response.status_code == 200:
            return b'OK' in response.content
    except ConnectionError:
        return False
    return False
  