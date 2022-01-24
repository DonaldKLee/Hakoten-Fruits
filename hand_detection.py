import cv2
import mediapipe as mp
import numpy as np

# Imports the machine learning model that detects hands
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Webcam input
cap = cv2.VideoCapture(0)

# Gets the size of the user's camera (The size of the game is dependent on the size of the camera)
def get_camera_size():
    sw  = cap.get(3)  # width of camera
    sh = cap.get(4)  # height of camera
    return sw, sh

# Opens the video camera and detects hands, then returns the cordinates of the palm
def open_video():
    sw, sh = get_camera_size()
    # Sets the parameters for the machine learning model
    with mp_hands.Hands(
        max_num_hands = 1, # Makes it so that we can only detect one hand
        model_complexity=0, 
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands: 
        # While the camera is on
        while cap.isOpened():
            success, image = cap.read()
            if not success:  # If camera does not work
                continue
            
            image.flags.writeable = False
            # Flip the image so that the hand movement is not inversed
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            results = hands.process(image)

            # Allows drawing the hand annotations on the image
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Creates a black background where the hand annotations will be drawn on
            background = np.zeros((int(sh),int(sw),3), np.uint8)
            background[:] = (0,0,0)

            # If hand detected
            if results.multi_hand_landmarks:
                # Cordinates for the landmarks
                for hand_landmarks in results.multi_hand_landmarks:
                    # Calculates the cordinates of the palm using the top finger's landmark, and the wrist's landmark
                    x_top, y_top = hand_landmarks.landmark[9].x*sw, hand_landmarks.landmark[9].y*sh
                    x_bottom, y_bottom = hand_landmarks.landmark[0].x*sw, hand_landmarks.landmark[0].y*sh
                    x, y = (x_top + x_bottom)/2, (y_top + y_bottom)/2


                    # Draws a blue circle on the palm
                    cv2.circle(background, (int(x), int(y)), 10, (255,255,0), -1)
                    
                    # Draws the hand annotations
                    mp_drawing.draw_landmarks(background, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=4), # circles
                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2) # lines
                    )
    
                # Scales down the window that shows the video so it doesn't take up too much of the screen
                def rescale_frame(frame, percent=75):
                    width = int(frame.shape[1] * percent/ 100)
                    height = int(frame.shape[0] * percent/ 100)
                    dim = (width, height)
                    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
                

                # Runs the scale down function and scale it down by 75%
                scaled_down_background = rescale_frame(background, percent=25)

                # Opens the window that shows the video and hand annotations
                cv2.imshow('Hands', scaled_down_background)
        
            # Returns the cordinates of the palm
            return x,y