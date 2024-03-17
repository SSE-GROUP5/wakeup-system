import math
import requests
import base64
import cv2 as cv

def check_connection(client, config):
    try:
        response = client.get(config["WAKEUP_SERVER_URL"], timeout=1)
        if response.status_code == 200:
            return b'OK' in response.content
    except requests.ConnectionError:
        return False
    return False


def update_env_vars(config, msg):
    for key in config.keys():
        if key in msg:
            config[key] = msg[key]
            print(f'Updated {key} to {msg[key]}')
    with open('env_trigger.txt', 'w') as f:
        for key in config.keys():
            f.write(f'{key}={config[key]}\n')
    return config
  


def confirm_to_server(client, config):
    try:
        request = client.post(config["WAKEUP_SERVER_URL"]+"/triggers/confirm", json={'id': config["ID"]})
        if request.status_code == 200:
            print('Confirmed to wakeup server')
        elif request.status_code == 404:
            print('Device id not registered in wakeup server')
        elif request.status_code != 200:
            print('Error confirming to wakeup server')
    except Exception as e:
        print(e)
        

def get_angle_between_points(p1, p2):
    if p1 is None or p2 is None:
        return None
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return 0
    if p1[0] == p2[0]:
        return 90
    if p1[1] == p2[1]:
        return 0
      
    x1, y1 = p1
    x2, y2 = p2
    return 180 - abs(math.atan2(y2-y1, x2-x1) * 180 / math.pi)
  
def get_falling_side(p1, p2):
    if p1 is None or p2 is None:
        return None
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return 0
    if p1[0] == p2[0]:
        return 90
    if p1[1] == p2[1]:
        return 0
      
    x1, y1 = p1
    x2, y2 = p2
    angle = math.atan2(y2-y1, x2-x1) * 180 / math.pi
    return "left" if angle < 0 else "right"


def save_picture(frame, file_name):
    cv.imwrite(file_name, frame)

def send_signal(client, config, frame):
    filename = f'{config["ID"]}_fall.png'
    save_picture(frame, filename)
    try:
        picture_string = None
        with open(filename, 'rb') as img:
            picture_string = base64.b64encode(img.read()).decode('utf-8')
         
        request = client.post(
            config["WAKEUP_SERVER_URL"]+"/signals", 
            json={'id': config["ID"], 
                  'action': 'vision_upper_body_fall', 
                  'num_actions': "alert", 
                  'picture': picture_string}
        )
        
        print(request.status_code)
        print(request.content)
    except Exception as e:
        print(e)