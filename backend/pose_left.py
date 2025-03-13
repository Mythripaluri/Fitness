import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
from gtts import gTTS
import os
import pyglet
import threading
import time

# Global variables
reps = 0
sets = 0
direction = 0
form = 1  
last_audio_message = None  
message_timer = 0  
count = 0

def play(filename):
    """Play the saved audio file using pyglet."""
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
    pyglet.app.run()

def play_audio(text):
    """Convert text to speech and play it in a separate thread to reduce delay."""
    global last_audio_message, message_timer  
    last_audio_message = text  
    message_timer = time.time()  

    tts = gTTS(text=text, lang='en')
    filename = "message.mp3"
    tts.save(filename)

    # ✅ Use threading instead of multiprocessing to reduce delay
    audio_thread = threading.Thread(target=play, args=(filename,))
    audio_thread.start()

def left_curl(target_reps, target_sets):
    global reps, sets, direction, form, last_audio_message, message_timer, count
    final_message_shown = False  
    start_time = time.time()  

    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    feedback = "KEEP YOUR BACK STRAIGHT"

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break  

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)  
            shoulder = detector.findAngle(img, 13, 11, 23) 

            # ✅ Provide feedback based on elbow angle
            if elbow > 155:  
                feedback = "UP"
                if direction == 0:  
                    direction = 1  
            
            elif elbow < 40 and direction == 1:  
                feedback = "DOWN"
                reps += 1  
                direction = 0  
                print(f"Rep {reps}/{target_reps}, Set {sets}/{target_sets}")  

                if reps >= target_reps:
                    if sets < target_sets:
                        sets += 1  
                        reps = 0  
                        play_audio("You have completed a set!")  

                    if sets >= target_sets and not final_message_shown:
                        final_message_shown = True  # ✅ Prevent multiple calls
                        play_audio("Target Achieved!!") 

            # ✅ Calculate posture accuracy (placeholder logic)
            posture_accuracy = max(0, min(100, 100 - abs(90 - shoulder)))  # Example: based on shoulder angle

            # ✅ Provide feedback based on accuracy
            if posture_accuracy > 85:
                feedback = "Perfect Form!"
            elif 60 <= posture_accuracy <= 85:
                feedback = "Good, but adjust slightly."
            else:
                feedback = "Fix Your Posture!"

        # Info Panel
        info_panel = np.zeros((150, 1280, 3), dtype=np.uint8)
        cv2.putText(info_panel, f"Sets: {sets}/{target_sets}", (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Reps: {reps}", (50, 90), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Feedback: {feedback}", (50, 130), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Display feedback
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        # ✅ Show the frame properly (instead of Flask's yield method)
        cv2.imshow("Live Feed", img)

        # ✅ Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage:
# left_curl(10, 3)  # Uncomment this line to run
