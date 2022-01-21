# https://google.github.io/mediapipe/solutions/hands

import cv2
import mediapipe as mp
import numpy as np
# import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# Webcam input
cap = cv2.VideoCapture(0)

def get_camera_size():
    sw  = cap.get(3)  # width of camera
    sh = cap.get(4)  # height of camera
    return sw, sh


def open_video():
    sw, sh = get_camera_size()
    with mp_hands.Hands(
        max_num_hands = 1,
        model_complexity=0, 
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands: 
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
                
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)

            results = hands.process(image)

            # Draw the hand annotations on the image
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            background = np.zeros((int(sh),int(sw),3), np.uint8)
            background[:] = (0,0,0)

            if results.multi_hand_landmarks:
                # print(results.multi_hand_landmarks[0])
                
                # Cordinates for the landmarks
                for hand_landmarks in results.multi_hand_landmarks:
                    # print(mp_hands.HAND_CONNECTIONS)
                    x_top, y_top = hand_landmarks.landmark[9].x*sw, hand_landmarks.landmark[9].y*sh

                    x_bottom, y_bottom = hand_landmarks.landmark[0].x*sw, hand_landmarks.landmark[0].y*sh
                    x, y = (x_top + x_bottom)/2, (y_top + y_bottom)/2

                    cv2.circle(background, (int(x), int(y)), 10, (255,255,0), -1) # Palm
                    
                    # pyautogui.moveTo(x,y)
                    
                    # mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
                    mp_drawing.draw_landmarks(background, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=4), # circles
                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2) # lines
                    )
    

                def rescale_frame(frame, percent=75):
                    width = int(frame.shape[1] * percent/ 100)
                    height = int(frame.shape[0] * percent/ 100)
                    dim = (width, height)
                    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
                    
                scaled_down_background = rescale_frame(background, percent=25)


                cv2.imshow('Hands', scaled_down_background)
        
                # return x,y
            return x,y


        #     if cv2.waitKey(1) == ord('q'):
        #         break
        
        # cap.release()
        # cv2.destroyAllWindows()