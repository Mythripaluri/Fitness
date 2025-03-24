import cv2
import threading
import queue
import PoseModule as pm

# Initialize global variables
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height
detector = pm.poseDetector()

frame_queue = queue.Queue(maxsize=1)  # Stores the latest frame

def video_capture_thread():
    """ Continuously captures frames from the webcam and adds to queue. """
    print("🎥 Video Capture Thread Started!")

    while True:
        ret, img = cap.read()
        if not ret:
            print("⚠️ Warning: Cannot read frame!")
            continue
        
        img = detector.findPose(img, False)

        if frame_queue.full():
            frame_queue.get()  # Remove old frame to avoid memory issues
        frame_queue.put(img)

# Start the video capture in a separate thread
video_thread = threading.Thread(target=video_capture_thread, daemon=True)
video_thread.start()
