import mediapipe as mp
import cv2
import time
import os
from gesture_class.Gesture import Gesture
from gesture_class.GestureRecording import GestureRecording
from gesture_class.gesture_frame import create_gesture_frame

FPS = 15 #frames per secound for mediapipes capture
FRAME_TIME = 1.0 / FPS #how long each frame is
COUNT_DOWN = 3

def record_gesture(name, filename, one_handed=False):
    print(
        """
        Tool for recording gestures
        press a to start and stop recording
        press q to quit and save
        """
    )
    hands_model = mp.solutions.hands
    drawing = mp.solutions.drawing_utils
    hands = hands_model.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
    
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow('Gesture Capture', cv2.WINDOW_GUI_NORMAL)
    
    gesture = Gesture(name, one_handed=one_handed)
    recording = GestureRecording()
    is_recording = False
    
    while video_capture.isOpened():
        # capture video and landmark using mediapipes
        frame_start = time.time()
        ret, frame = video_capture.read()
        if not ret:
            break
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # visualize landmarking
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                drawing.draw_landmarks(frame, hand_landmarks, hands_model.HAND_CONNECTIONS)
        
        cv2.imshow('Gesture Capture', frame)
        
        # record frame
        if is_recording:
            gesture_frame = create_gesture_frame(results.multi_hand_landmarks, results.multi_handedness)
            recording.add_frame(gesture_frame)
        
        # check for keyboard inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            gesture.save_as_json(filename)
            break
            
        if results.multi_hand_landmarks:
            if key == ord('a'):
                if is_recording:
                    gesture.add_recording(recording)
                    recording = GestureRecording()
                    print("STOPPED recording")
                    is_recording = False
                else:
                    print("Recording in: " + str(COUNT_DOWN))
                    for i in range(COUNT_DOWN, 0, -1):
                        time.sleep(1)
                        print(i)
                    print("STARTED recording!")
                    is_recording = True
        
        # maintain FPS
        elapsed_frame = time.time() - frame_start
        time.sleep(max(0, FRAME_TIME - elapsed_frame))
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_gesture("wave", "wave", one_handed=True)