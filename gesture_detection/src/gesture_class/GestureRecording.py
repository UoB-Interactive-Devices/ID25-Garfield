import numpy as np
from gesture_class import gesture_frame
from fastdtw import fastdtw
import custom_distance


class GestureRecording:
    """
    Gesture recording represents a video of gesture frames, where get_recording returns a np.array suitable for fast dtw.

    A buffer of max_length is generated on init so don't set too large
    """
    def __init__(self, max_length=150): #at 15 fps, is 10 secounds which is long enough easy!
        self.max_length = max_length
        self.recording = np.full((max_length, 23), np.nan, dtype=np.float32)
        self.length = 0
    
    def add_frame(self, frame):
        if self.length < self.max_length: #not at max size
            self.recording[self.length] = frame
            self.length+=1
        else: #if at max size
            self.recording[:-1] = self.recording[1:] #cut of first element
            self.recording[-1] = frame

    def get_recording(self):
        return self.recording[:self.length]
    
    def to_dict(self):
        return [gesture_frame.to_dict(frame) for frame in self.get_recording()]

    @classmethod
    def from_dict(cls, data):
        recording = cls(max_length=len(data))
        for frame_data in data:
            frame = gesture_frame.from_dict(frame_data)
            recording.add_frame(frame)
        
        return recording
    
def recording_distance(recording1, recording2, one_handed=False):
    if one_handed:
        distance, _ = fastdtw(recording1, recording2, dist=custom_distance.one_handed)
        return distance
    else:
        distance, _ = fastdtw(recording1, recording2, dist=custom_distance.two_handed)
        return distance