from gesture_class.Gesture import Gesture

class MultiGestures:
    """
    MultiGestures manages a collection of gestures for recognition
    and provides methods for matching input recordings against known gestures.
    """
    def __init__(self, gestures):
        self.gestures = gestures
    
    def load_gesture(self, filepath):
        """Load a gesture from a JSON file and add it to the collection"""
        gesture = Gesture.load_from_json(filepath)
        self.gestures.append(gesture)
    
    def best_match(self, compared_recording):
        """Find the best matching gesture for the given recording"""
        best_gesture = None
        best_score = float("inf")
        for gesture in self.gestures:
            score = gesture.compare_all(compared_recording)
            if score < best_score:
                best_gesture = gesture
                best_score = score
        return best_gesture.name, best_score