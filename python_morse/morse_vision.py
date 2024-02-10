from vision_constants import LEFT_EYE, RIGHT_EYE
import cv2 as cv
import mediapipe as mp
import time
import vision_utils as vision_utils
import numpy as np
from morse_functions import decode_morse_letter
from dotenv import load_dotenv
import os
import sys
import requests


current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer
import beepy


if not os.path.exists('.env.morse_vision'):
    print('Please create .env.morse_vision file \n In the file, please set WAKEUP_SERVER_URL and ID')
    exit(1)

load_dotenv('.env.morse_vision')

# variables for wakeup server that must be set in .env.morse_vision
__WAKEUP_SERVER_URL= os.getenv('WAKEUP_SERVER_URL')
__ID= os.getenv('ID') 
__ZMQ_SERVER= os.getenv('ZMQ_SERVER')

if __WAKEUP_SERVER_URL is None or __ID is None or __ZMQ_SERVER is None:
    print('Please set WAKEUP_SERVER_URL and ID and ZMQ_SERVER in .env.morse_vision file')
    exit(1)

client = requests.session()
config = {
    "WAKEUP_SERVER_URL": __WAKEUP_SERVER_URL,
    "ID": __ID,
    "CHANNEL": int(os.getenv('CHANNEL')) or 0,
    "CLOSED_EYES_FRAME":  float(os.getenv('CLOSED_EYES_FRAME')) or 3,
    "BLINKING_RATIO": float(os.getenv('BLINKING_RATIO')) or 4.5,
    "MIN_BLINKING_TIME": float(os.getenv('MIN_BLINKING_TIME')) or 0.1,
    "MAX_SHORT_BLINKING_TIME": float(os.getenv('MAX_SHORT_BLINKING_TIME')) or 0.6,
    "TIMEOUT_MORSE_READER": float(os.getenv('TIMEOUT_MORSE_READER')) or 1.5,
    "ZMQ_SERVER": __ZMQ_SERVER
}

mqServer = ZeroMQServer(config["ZMQ_SERVER"])

# constants for blinking
CAMERA = cv.VideoCapture(config["CHANNEL"])
FONTS =cv.FONT_HERSHEY_COMPLEX
MAP_FACE_MESH= mp.solutions.face_mesh

# variables for blinking
cef_counter= 0
last_blinking_time=time.time()

# variables for morse code
has_started_close_eyes = False
has_bell_rung = False
can_start_morse = False
start_blinking_time = time.time()
letter = ''


def check_connection():
    try:
        client.get(config["WAKEUP_SERVER_URL"])
        return True
    except requests.ConnectionError:
        return False


def update_env_vars(config, msg):
    for key in config.keys():
        if key in msg:
            config[key] = msg[key]
            print(f'Updated {key} to {msg[key]}')
    with open('.env.morse_vision', 'w') as f:
        for key in config.keys():
            f.write(f'{key}={config[key]}\n')
    return config

with MAP_FACE_MESH.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:

    last_health_check = time.time()
    is_connected = check_connection()
    while True:
       
        message = mqServer.receive()
        if message != None:
            topic, msg = message
            if topic == config["ID"]:
                config = update_env_vars(config, msg)
        ret, frame = CAMERA.read() 
        
        if not ret: 
            break # no more frames break
        
        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)

        frame_height, frame_width= frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)
        
        # Check if the server is still connected
        if time.time() - last_health_check > 5:
            last_health_check = time.time()
            is_connected = check_connection()
        
        color_server = vision_utils.GREEN if is_connected else vision_utils.RED
        frame = vision_utils.colorBackgroundText(frame,  f'WAKEUP SERVER: {is_connected}', FONTS, 1.7, (0, 50), 2, color_server, pad_x=6, pad_y=6, )
            
        if results.multi_face_landmarks:
            mesh_coords = vision_utils.landmarksDetection(frame, results, False)
            ratio = vision_utils.blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE)
            
            if ratio > config["BLINKING_RATIO"]:
                # Eyes Closed
                cef_counter +=1
                vision_utils.colorBackgroundText(frame,  f'Blink', FONTS, 1.7, (int(frame_height/2), 100), 2, vision_utils.YELLOW, pad_x=6, pad_y=6, )
      
                if not has_bell_rung and not has_started_close_eyes and cef_counter > 30:
                  has_bell_rung = True
                  beepy.beep(sound=5)


                if not can_start_morse and has_bell_rung:
                  can_start_morse = True
                  has_started_close_eyes = False
                
                if can_start_morse and not has_started_close_eyes:
                  has_started_close_eyes = True
                  start_blinking_time = time.time()
                  
            else:
                # Eyes Open
                if cef_counter > config["CLOSED_EYES_FRAME"]:
                    last_blinking_time = time.time()
                    cef_counter = 0
                  

                    ## Start Morse Code Reader
                    if has_started_close_eyes:
                      blinking_time = last_blinking_time - start_blinking_time

                      if config["MIN_BLINKING_TIME"] < blinking_time <= config["MAX_SHORT_BLINKING_TIME"]:
                        print('Short Blink')
                        letter += '.'
                      elif blinking_time > config["MAX_SHORT_BLINKING_TIME"]:
                        print('Long Blink')
                        letter += '-'
                      has_started_close_eyes = False

                    
                if len(letter) > 1 and time.time() - last_blinking_time > config["TIMEOUT_MORSE_READER"]:
                    letter += ' '
                    # remove first letter because it is the start signal
                    letter = letter[1:]
                    print(f'Morse Code: {letter}')
                    decoded_letter = decode_morse_letter(letter)
                    print(f'Decoded Letter: {decoded_letter}')
                    letter = ''
                    has_bell_rung = False
                    can_start_morse = False
                    if decoded_letter and is_connected:
                        client.post(config["WAKEUP_SERVER_URL"]+"/signals", json={'name': config["ID"], 'action': 'morse', 'num_actions': decoded_letter}) 
                  
            if len(letter) > 0:
              frame = vision_utils.rectTrans(frame, (mesh_coords[LEFT_EYE[8]][0]-150, mesh_coords[LEFT_EYE[8]][1]-150), (mesh_coords[LEFT_EYE[8]][0]-100, mesh_coords[LEFT_EYE[8]][1]-100), vision_utils.GREEN, -1, 0.5)
                ## End Morse Code Reader
                    

                
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in LEFT_EYE ], dtype=np.int32)], True, vision_utils.GREEN, 1, cv.LINE_AA)
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in RIGHT_EYE ], dtype=np.int32)], True, vision_utils.GREEN, 1, cv.LINE_AA)
        else:
            vision_utils.colorBackgroundText(frame,  f'No Face Detected', FONTS, 2.5, (int(frame_height/2)-200, 200), 2, vision_utils.RED, pad_x=6, pad_y=6, )


        cv.imshow('frame', frame)
        key = cv.waitKey(2)
        if key==ord('q') or key ==ord('Q'):
            break
    
    cv.destroyAllWindows()
    CAMERA.release()
    

    
    
    
