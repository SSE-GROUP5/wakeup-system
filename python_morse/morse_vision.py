from vision_constants import LEFT_EYE, RIGHT_EYE
import cv2 as cv
import mediapipe as mp
import time
import vision_utils as vision_utils, math
import numpy as np
from requests import Session
from morse_functions import decode_morse_letter
config = {
    'CLOSED_EYES_FRAME':3,
    'BLINKING_RATIO':4.50,
    'TIMEOUT_SEC':1,
    'WAKEUP_SERVER_URL':'http://localhost:5001',
    'ID':'sound_device_1',
    'task':'3_taps',
    'action':'2_taps',
    'DEVICE_ID':'andy_vision',
}

def landmarksDetection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]
    return mesh_coord

def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

def blinkRatio(img, landmarks, right_indices, left_indices):
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2
    return ratio 

# variables 
frame_counter =0
CEF_COUNTER =0
TOTAL_BLINKS =0
MIN_BLINKING_TIME = 0.1
MAX_SHORT_BLINKING_TIME= 0.5

start_blinking_time = time.time()
has_started_close_eyes = False
FONTS =cv.FONT_HERSHEY_COMPLEX
LAST_BLINKING_TIME = time.time()

map_face_mesh = mp.solutions.face_mesh
camera = cv.VideoCapture(0)
letter = ''

with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:

    start_time = time.time()
    while True:
        frame_counter +=1 # frame counter
        ret, frame = camera.read() # getting frame from camera 
        if not ret: 
            break # no more frames break
        
        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        frame_height, frame_width= frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results, False)
            ratio = blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE)
            vision_utils.colorBackgroundText(frame,  f'Ratio : {round(ratio,2)}', FONTS, 0.7, (30,100),2, vision_utils.PINK, vision_utils.YELLOW)

            if ratio > config['BLINKING_RATIO']:
                CEF_COUNTER +=1
                vision_utils.colorBackgroundText(frame,  f'Blink', FONTS, 1.7, (int(frame_height/2), 100), 2, vision_utils.YELLOW, pad_x=6, pad_y=6, )
                if not has_started_close_eyes:
                  start_blinking_time = time.time()
                  has_started_close_eyes = True
            else:
                if CEF_COUNTER > config['CLOSED_EYES_FRAME']:
                    TOTAL_BLINKS +=1
                    LAST_BLINKING_TIME = time.time()
                    CEF_COUNTER = 0
                
                    if has_started_close_eyes:
                      blinking_time = LAST_BLINKING_TIME - start_blinking_time
                      if MIN_BLINKING_TIME < blinking_time <= MAX_SHORT_BLINKING_TIME:
                        # print('Short Blink')
                        letter += '.'
                      elif blinking_time > MAX_SHORT_BLINKING_TIME:
                        # print('Long Blink')
                        letter += '-'
                      has_started_close_eyes = False
                    
                if len(letter) > 0 and time.time() - LAST_BLINKING_TIME > 1.5:
                    letter += ' '
                    break
                    
              
            
            vision_utils.colorBackgroundText(frame,  f'Total Blinks: {TOTAL_BLINKS}', FONTS, 0.7, (30,150),2)
            
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in LEFT_EYE ], dtype=np.int32)], True, vision_utils.GREEN, 1, cv.LINE_AA)
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in RIGHT_EYE ], dtype=np.int32)], True, vision_utils.GREEN, 1, cv.LINE_AA)
        
        
        
        else:
            vision_utils.colorBackgroundText(frame,  f'No Face Detected', FONTS, 2.5, (int(frame_height/2)-200, 200), 2, vision_utils.RED, pad_x=6, pad_y=6, )


        # calculating  frame per seconds FPS
        end_time = time.time()-start_time
        fps = frame_counter/end_time

        frame =vision_utils.textWithBackground(frame,f'FPS: {round(fps,1)}',FONTS, 1.0, (30, 50), bgOpacity=0.9, textThickness=2)

        cv.imshow('frame', frame)
        key = cv.waitKey(2)
        if key==ord('q') or key ==ord('Q'):
            break
    cv.destroyAllWindows()
    camera.release()
    
    print(f'Morse Code: {letter}')
    decoded_letter = decode_morse_letter(letter)
    print(f'Decoded Letter: {decoded_letter}')
    
    
    
