import numpy as np

MAX_HAND_DIST = 4

def create_gesture_frame(multi_landmarks, multi_handedness):
    """
    Given data from a Landmarked frame from mediapipes GestureFrame stores useful angles and distances for comparison.
    as a np array of length 23, type float32:
    - 0-10: Left hand data (or NaN's if no left hand)
    - 11-21: Right hand data (or NaN's if no right hand)
    - 22: Distance between hands
    """

    data = np.full(23, np.nan, dtype=np.float32)
    left_hand = data[0:11]
    right_hand = data[11:22]
    distance = data[22:23]
    
    if multi_landmarks is None or len(multi_handedness) == 0:
        return data
    
    # Process first hand
    landmarks_0 = None
    landmarks_1 = None
    if len(multi_handedness) > 0:
        if (multi_handedness[0].classification[0].label == "left"):
            landmarks_0 = format_landmarks(multi_landmarks[0])
            calculate_hand(left_hand, landmarks_0)
        else:
            landmarks_0 = format_landmarks(multi_landmarks[0])
            calculate_hand(right_hand, landmarks_0)
    
    # Process second hand if exists
    if len(multi_handedness) > 1:
        if (multi_handedness[1].classification[0].label == "left"):
            landmarks_1 = format_landmarks(multi_landmarks[1])
            calculate_hand(left_hand, landmarks_1)
            calc_hand_distance(distance, landmarks_0, landmarks_1) #also calculate hand distance (since two hands found)
        else:
            landmarks_1 = format_landmarks(multi_landmarks[1])
            calculate_hand(right_hand, landmarks_1)
            calc_hand_distance(distance, landmarks_0, landmarks_1) #also calculate hand distance
    
    return data

def format_landmarks(unformatted_landmarks):
    """Convert mediapipe landmarks to numpy array"""
    return np.array([[lm.x, lm.y, lm.z] for lm in list(unformatted_landmarks.landmark)], dtype=np.float32)

def calculate_hand(hand_array, landmarks):
    """
    Populates a hand_array using landmarks as follows:
    [4 * between angles, 5 * each angles, 1 * horizon angle, 1 * camera angle]
    """
    calc_between_angles(hand_array[0:4], landmarks)
    calc_each_angles(hand_array[4:9], landmarks)  
    calc_horizon_angle(hand_array[9:10], landmarks)
    calc_camera_angle(hand_array[10:11], landmarks)

def point_angle(landmarks, v1, v2, v3):
    """ 
    Calculates the angle between 3 landmark points (between 0 and pi)
    Used for between and each
    """
    vec1 = landmarks[v1] - landmarks[v2]
    vec2 = landmarks[v3] - landmarks[v2]
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)
    return np.arccos(np.dot(vec1_norm, vec2_norm))

def vec_angle(landmarks, v1, v2, vector):
    """
    Calculate the angle between 2 landmark points and a vector.
    Used for horizon and camera angles
    """
    vec1 = landmarks[v1] - landmarks[v2]
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vector / np.linalg.norm(vector)
    return np.arccos(np.dot(vec1_norm, vec2_norm))

def calc_between_angles(between_array, landmarks):
    between_array[0] = point_angle(landmarks, 1, 0, 5) # angle between thumb and index
    between_array[1] = point_angle(landmarks, 5, 0, 9) # angle between index and middle
    between_array[2] = point_angle(landmarks, 19, 0, 13) # angle between middle and ring
    between_array[3] = point_angle(landmarks, 13, 0, 17) # angle between ring and pinkie

def calc_each_angles(each_array, landmarks):
    each_array[0] = point_angle(landmarks, 0, 2, 4) # thumb angle
    each_array[1] = point_angle(landmarks, 5, 6, 8) # index angle
    each_array[2] = point_angle(landmarks, 9, 10, 12) # middle angle
    each_array[3] = point_angle(landmarks, 13, 14, 16) # ring angle
    each_array[4] = point_angle(landmarks, 17, 18, 20) # pinkie angle

def calc_horizon_angle(horizon_angle, landmarks):
    # Angle between palm and horizon
    horizon_angle[0] = vec_angle(landmarks, 5, 17, np.array([1, 0, 0]))

def calc_camera_angle(camera_angle, landmarks):
    # Angle between palm and camera
    camera_angle[0] = vec_angle(landmarks, 5, 17, np.array([0, 0, 1]))

def calc_hand_distance(dist_between, landmarks1, landmarks2):
    """
    Distance between hands, in terms of the size of the hands.
    """
    hand_size1 = np.linalg.norm(landmarks1[9] - landmarks1[0])  # middle finger base to wrist
    hand_size2 = np.linalg.norm(landmarks2[9] - landmarks2[0])  # middle finger base to wrist
    
    avg_hand_size = (hand_size1 + hand_size2) / 2
    
    if avg_hand_size < 0.1:
        return np.nan
    
    #distance between wrist points
    true_dist = np.linalg.norm(landmarks1[0] - landmarks2[0])
    
    dist_between[0] = min(dist_between / avg_hand_size, MAX_HAND_DIST)

def to_dict(gesture_frame):
    return [None if np.isnan(x) else float(x) for x in gesture_frame]

def from_dict(data):
    return np.array([np.nan if x is None else x for x in data], dtype=np.float32)

def print(gesture_frame):
    """display in a readable way"""

    descriptions = [
        "Angle between thumb and index", "Angle between index and middle", 
        "Angle between middle and ring", "Angle between ring and pinkie",
        "Thumb angle", "Index angle", "Middle angle", "Ring angle", 
        "Pinkie angle", "Horizon angle", "Camera angle"
    ]
    
    for hand, start_idx in [("Left Hand", 0), ("Right Hand", 11)]:
        print(f"{hand}:")
        data = gesture_frame[start_idx:start_idx+11]
        if np.isnan(data[0]):
            print(f" is empty.")
        else:
            for i, value in enumerate(data):
                if not np.isnan(value):
                    print(f" {descriptions[i]}: {value} radians")
        print()
    
    print(f"Distance: {gesture_frame[22]}" if not np.isnan(gesture_frame[22]) else "No distance.")