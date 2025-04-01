import mediapipe as mp
import cv2
import time
from gesture_class.GestureRecording import GestureRecording
from gesture_class.gesture_frame import create_gesture_frame
from gesture_class.MultiGestures import MultiGestures

FPS = 15 #frames per secound for mediapipes capture
FRAME_TIME = 1.0 / FPS #how long each frame is

SECONDS_ANALYZED = 1.5  # how many seconds of capture is analyzed and compared with gestures
def recognise_gestures(multi_gesture):
    """
    Continuously capture video input and recognize gestures
    """
    hands_model = mp.solutions.hands
    drawing = mp.solutions.drawing_utils
    hands = hands_model.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
    
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow('Gesture Capture', cv2.WINDOW_GUI_NORMAL)
    
    recording = GestureRecording(max_length=int(FPS*SECONDS_ANALYZED))
    
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
        
        # find best match
        gesture_frame = create_gesture_frame(results.multi_hand_landmarks, results.multi_handedness)
        recording.add_frame(gesture_frame)
        
        best_name, best_score = multi_gesture.best_match(recording)
        print(best_name, best_score)
        
        # check for keyboard inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        # maintain FPS
        elapsed_frame = time.time() - frame_start
        time.sleep(max(0, FRAME_TIME - elapsed_frame))
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    multi_gesture = MultiGestures()
    multi_gesture.load_gesture("wave")
    recognise_gestures(multi_gesture)