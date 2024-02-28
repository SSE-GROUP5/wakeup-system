
import cv2 as cv
import mediapipe as mp
import time
import utils
from utils import landmarksDetection, blinkRatio
import numpy as np
from constants import Constants
from requests import Session, ConnectionError
from constants import LEFT_EYE, RIGHT_EYE
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))

def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"
  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer
import beepy

def send_signal(num_action: str):
    data = {
        "id": config.env_vars["ID"],
        "action": 'blink',
        "num_actions": num_action
    }
    url = f"{config.env_vars['WAKEUP_SERVER_URL']}/signals"
    response = client.post(f"{url}/signals", json=data)
    time.sleep(3)
    print(response.content)
    print(response)

def confirm_to_server():
    try:
        request = client.post(config.env_vars["WAKEUP_SERVER_URL"]+"/triggers/confirm", json={'id': config.env_vars["ID"]})
        print(request.status_code)
        if request.status_code == 200:
            print("Server confirmed")
        elif request.status_code == 404:
            print("Device not registered with server, please register the device first")
    except Exception as e:
        print(e)

def check_connection():
    try:
        response = client.get(config.env_vars["WAKEUP_SERVER_URL"], timeout=1)
        if response.status_code == 200:
            return b'OK' in response.content
    except ConnectionError:
        return False
    return False
  
# variables 
frame_counter =0
CEF_COUNTER =0
TOTAL_BLINKS =0

python_executable_dir = os.path.dirname(sys.executable)
config_path = os.path.join(python_executable_dir, '../blink_detect/') if is_exe_file() else current_dir
config_path = os.path.normpath(config_path)
config_path = os.path.join(config_path, 'env_trigger.txt')
  
if not os.path.exists(config_path):
    print(f'Please create env_trigger.txt file in {config_path} with the following content:')
    print("In the file, please set WAKEUP_SERVER_URL, ID, ZMQ_SERVER")
    exit(1)
    
config = Constants(envFilename = config_path)


FONTS =cv.FONT_HERSHEY_COMPLEX
LAST_BLINKING_TIME = time.time()
client = Session()
client.headers.update({'Content-Type': 'application/json'})
client.headers.update({'Accept': 'application/json'})
mqServer = ZeroMQServer("tcp://*:5556")


map_face_mesh = mp.solutions.face_mesh
# camera object 
camera = cv.VideoCapture(0)
has_bell_rung = False
has_repoen_eyes = False

with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:

    # starting time here 
    start_time = time.time()
    # starting Video loop here.
    
    last_health_check = time.time()
    is_connected = check_connection()
    confirm_to_server()
    while True:
        frame_counter +=1 # frame counter
        ret, frame = camera.read() # getting frame from camera 
        if not ret: 
            break # no more frames break
        #  resizing frame

        message = mqServer.receive()
        if message != None:
            topic, msg = message
            if topic == config.env_vars["ID"]:
                config.updateEnvFile(msg)

        # Check if the server is still connected
        if time.time() - last_health_check > 5:
            last_health_check = time.time()
            is_connected = check_connection()
        
        color_server = utils.GREEN if is_connected else utils.RED
        frame = utils.colorBackgroundText(frame,  f'WAKEUP SERVER: {is_connected}', FONTS, 1.7, (0, 50), 2, color_server, pad_x=6, pad_y=6, )
            
        
        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        frame_height, frame_width= frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results, False)
            ratio = blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE)
            # cv.putText(frame, f'ratio {ratio}', (100, 100), FONTS, 1.0, utils.GREEN, 2)
            utils.colorBackgroundText(frame,  f'Ratio : {round(ratio,2)}', FONTS, 0.7, (30,100),2, utils.PINK, utils.YELLOW)

            if ratio > float(config.env_vars["BLINKING_RATIO"]):
                CEF_COUNTER +=1
                # cv.putText(frame, 'Blink', (200, 50), FONTS, 1.3, utils.PINK, 2)
                utils.colorBackgroundText(frame,  f'Blink', FONTS, 1.7, (int(frame_height/2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6, )

                if (not has_bell_rung) and CEF_COUNTER > int(config.env_vars["CLOSED_EYES_FRAME"]):
                      has_bell_rung = True
                      beepy.beep(sound=5)
          

            else:
                if CEF_COUNTER > int(config.env_vars["CLOSED_EYES_FRAME"]):
                    TOTAL_BLINKS +=1
                    LAST_BLINKING_TIME = time.time()
                    has_bell_rung = False
                    has_repoen_eyes = False
                
                CEF_COUNTER = 0
                
                    
            # cv.putText(frame, f'Total Blinks: {TOTAL_BLINKS}', (100, 150), FONTS, 0.6, utils.GREEN, 2)
            utils.colorBackgroundText(frame,  f'Total Blinks: {TOTAL_BLINKS}', FONTS, 0.7, (30,150),2)
            
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in LEFT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in RIGHT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
        else:
            utils.colorBackgroundText(frame,  f'No Face Detected', FONTS, 2.5, (int(frame_height/2)-200, 200), 2, utils.RED, pad_x=6, pad_y=6, )

        if(TOTAL_BLINKS > 0 and time.time() - LAST_BLINKING_TIME > int(config.env_vars["TIMEOUT_SEC"])):
            print('Sending signal')
            send_signal(TOTAL_BLINKS)
            TOTAL_BLINKS = 0


        # calculating  frame per seconds FPS
        end_time = time.time()-start_time
        fps = frame_counter/end_time

        frame =utils.textWithBackground(frame,f'FPS: {round(fps,1)}',FONTS, 1.0, (30, 50), bgOpacity=0.9, textThickness=2)
        # writing image for thumbnail drawing shape
        # cv.imwrite(f'img/frame_{frame_counter}.png', frame)
        cv.imshow('frame', frame)
        key = cv.waitKey(2)
        if key==ord('q') or key ==ord('Q'):
            break
    cv.destroyAllWindows()
    camera.release()