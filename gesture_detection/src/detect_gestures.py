import os
import mediapipe as mp
import cv2
import time
from gesture_class.Gesture import Gesture
from gesture_class.GestureRecording import GestureRecording
from gesture_class.gesture_frame import create_gesture_frame
from gesture_class.MultiGestures import MultiGestures

# Constants
FPS = 15
FRAME_TIME = 1.0 / FPS
SECONDS_ANALYZED = 1

# Global variables for initialization
all_gestures = {}
hands_model = mp.solutions.hands
drawing = mp.solutions.drawing_utils
hands = hands_model.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
video_capture = None
recording = None

def load_all_gestures():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    gesture_dir = os.path.join(project_root, "gesture_files")
    
    for filename in os.listdir(gesture_dir):
        if filename.endswith(".json"):
            name = os.path.splitext(filename)[0]
            try:
                gesture = Gesture.load_from_json(name)
                all_gestures[name] = gesture
            except Exception as e:
                print(f"Error loading gesture '{name}': {str(e)}")

load_all_gestures()

def initialize_capture():
    global video_capture, recording
    
    if video_capture is None or not video_capture.isOpened():
        video_capture = cv2.VideoCapture(2)
        cv2.namedWindow('Gesture Capture', cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('Gesture Capture', 960, 720)
    
    recording = GestureRecording(max_length=int(FPS*SECONDS_ANALYZED))
    
    return video_capture.isOpened()

initialize_capture() 

def release_resources():
    global video_capture
    
    if video_capture is not None and video_capture.isOpened():
        video_capture.release()
        cv2.destroyAllWindows()
        video_capture = None

def detect_gestures(multi_gesture, gesture_scores, gesture_periods, detect_period=None):
    if not initialize_capture():
        print("Failed to initialize video capture.")
        return "null"
    
    frames_processed = 0
    infinite_mode = detect_period is None
    total_frames = float('inf') if infinite_mode else int(FPS * detect_period)
    
    # Track consecutive frames where each gesture meets its score threshold
    gesture_consecutive_frames = {gesture_name: 0 for gesture_name in gesture_scores}
    
    # Calculate required frames for each gesture's period
    gesture_required_frames = {gesture_name: int(FPS * period) 
                             for gesture_name, period in gesture_periods.items()}
    
    while video_capture.isOpened() and frames_processed < total_frames:
        frame_start = time.time()
        ret, frame = video_capture.read()
        
        if not ret:
            break
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                drawing.draw_landmarks(frame, hand_landmarks, hands_model.HAND_CONNECTIONS)
        
        if infinite_mode:
            cv2.putText(frame, f"Frames: {frames_processed}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Frames: {frames_processed}/{total_frames}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        
        gesture_frame = create_gesture_frame(results.multi_hand_landmarks, results.multi_handedness)
        recording.add_frame(gesture_frame)
        best_name, best_score = multi_gesture.best_match(recording)
        
        # Track gesture performance
        for gesture_name in gesture_scores:
            if best_name == gesture_name and best_score <= gesture_scores[gesture_name]:
                gesture_consecutive_frames[gesture_name] += 1
                
                # Check if we've met the required period
                if gesture_consecutive_frames[gesture_name] >= gesture_required_frames[gesture_name]:
                    # Return the gesture name if it meets criteria
                    return gesture_name
            else:
                # Reset counter if not matching this gesture or above score threshold
                gesture_consecutive_frames[gesture_name] = 0
        
        # Display recognized gesture and score
        cv2.putText(frame, f"Gesture: {best_name}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Score: {best_score:.2f}", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Display frame counts for each gesture
        y_pos = 150
        for gesture_name, frames in gesture_consecutive_frames.items():
            required = gesture_required_frames[gesture_name]
            cv2.putText(frame, f"{gesture_name}: {frames}/{required}", (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            y_pos += 30
        
        cv2.imshow('Gesture Capture', frame)
        
        if infinite_mode:
            print(f"Frame {frames_processed}: {best_name}, {best_score}")
        else:
            print(f"Frame {frames_processed}/{total_frames}: {best_name}, {best_score}")
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
            
        frames_processed += 1
        
        elapsed_frame = time.time() - frame_start
        time.sleep(max(0, FRAME_TIME - elapsed_frame))
    
    # If we've completed the detection period without returning a gesture
    return "null"

def detect_signs(gestures, detect_period=None):
    gesture_scores = {
        "null" : -1,
        "exit" : 3.7, #/
        "teacher" : 5.5, #/
        "how_are_you": 4.2,
        "robot" : -1                 
    }
    gesture_periods = {
        "null" : 10,
        "exit" : 0.2,
        "teacher" : 0.2,
        "how_are_you": 0.2,
        "robot" : 501                   
    }
    
    gestures = [all_gestures[gesture] for gesture in gestures]
    
    multi_gesture = MultiGestures(gestures)
    return detect_gestures(multi_gesture, gesture_scores, gesture_periods, detect_period)

if __name__ == "__main__":
    # Example: detect signs with their threshold scores and required periods
    # Format: (gesture_name, max_score_threshold, period_in_seconds)
    gestures = [ "exit", "how_are_you"]
    result = detect_signs(gestures, None)  # Run indefinitely
    print(f"Detection result: {result}")