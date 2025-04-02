import cv2
import os
import subprocess

def list_available_cameras():
    # Method 1: List video devices in /dev
    video_devices = [f for f in os.listdir('/dev') if f.startswith('video')]
    print(f"Available video devices: {video_devices}")
    
    # Method 2: Get camera details using v4l2-ctl (more info)
    try:
        result = subprocess.run(['v4l2-ctl', '--list-devices'], 
                               capture_output=True, text=True)
        print("\nDetailed camera information:")
        print(result.stdout)
    except FileNotFoundError:
        print("v4l2-ctl not found. Install with: sudo apt install v4l-utils")

    # Method 3: Try to open each camera and get properties
    for i in range(10):  # Try first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera {i} is working:")
                print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
                print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS)}")
            else:
                print(f"Camera {i} opened but can't read frames")
            cap.release()
        else:
            print(f"Camera {i} cannot be opened")

list_available_cameras()