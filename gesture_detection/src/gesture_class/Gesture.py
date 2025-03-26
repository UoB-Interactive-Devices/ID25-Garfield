from gesture_class.GestureRecording import GestureRecording, recording_distance
import json
import os

class Gesture:
    """
    Gesture represents a collection of gesture recordings for a specific gesture type.
    Each gesture can have multiple example recordings to compare against.
    """

    def __init__(self, name, one_handed=False):
        self.name = name
        self.one_handed = one_handed
        self.recordings = []
    
    def add_recording(self, new_recording):
        self.recordings.append(new_recording)
    
    def compare_all(self, compared_recording):
        """Compare a new recording against all examples and return the minimum distance"""
        min_distance = float("inf")
        for recording in self.recordings:
            dist = recording_distance(recording.get_recording(), compared_recording.get_recording(), one_handed=self.one_handed)
            if dist < min_distance:
                min_distance = dist
        return min_distance
    
    def to_dict(self):
        return {
            "name": self.name,
            "one_handed": self.one_handed,
            "recordings": [recording.to_dict() for recording in self.recordings]
        }
    
    @classmethod
    def from_dict(cls, data):
        gesture = cls(data["name"], data["one_handed"])
        gesture.recordings = [GestureRecording.from_dict(rec_data) for rec_data in data["recordings"]]
        return gesture
    
    def save_as_json(self, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels

        filepath = os.path.join(project_root ,"gesture_files", name + ".json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f)
        
        print("Saved gesture as "+name+".json" )

    @classmethod
    def load_from_json(cls, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels

        filepath = os.path.join(project_root ,"gesture_files", name + ".json")
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)