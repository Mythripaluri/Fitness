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
direction = 0
reps = 0
sets = 0
last_audio_message = None  
message_timer = 0  

# Function to play audio
def play(filename):
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
    pyglet.app.run()

def play_audio(text):
    global last_audio_message, message_timer  
    last_audio_message = text  
    message_timer = time.time()  
    
    tts = gTTS(text=text, lang='en')
    filename = "message.mp3"
    tts.save(filename)
    
    audio_thread = threading.Thread(target=play, args=(filename,))
    audio_thread.start()

def right_curl(target_reps, target_sets):
    global reps, sets, direction, last_audio_message, message_timer
    final_message_shown = False  
    start_time = time.time()  

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  
    cap.set(4, 720)
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
            elbow = detector.findAngle(img, 12, 14, 16)  # Right elbow
            shoulder = detector.findAngle(img, 14, 12, 24)  # Right shoulder
            
            if elbow > 155:  # Arm fully extended (UP position)
                feedback = "UP"
                if direction == 0:  # Only count once when reaching UP
                    direction = 1  
            
            elif elbow < 50 and direction == 1:  # Arm fully bent (DOWN position)
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
                        final_message_shown = True  
                        play_audio("Target Achieved!!") 

        # Info Panel
        info_panel = np.zeros((150, 1280, 3), dtype=np.uint8)
        cv2.putText(info_panel, f"Sets: {sets}/{target_sets}", (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Reps: {reps}", (50, 90), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Feedback: {feedback}", (50, 130), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        info_panel = cv2.resize(info_panel, (img.shape[1], info_panel.shape[0]))
        final_frame = np.vstack((img, info_panel))

        # Display Audio Message at the Top (for 3 seconds)
        if last_audio_message and (time.time() - message_timer < 3):
            cv2.putText(final_frame, last_audio_message, (200, 50),  
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        ret, jpeg = cv2.imencode('.jpg', final_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        # Track elapsed time correctly
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1800:  # 30 minutes
            play_audio("Time's up! Exercise Complete.")
            break  

    cap.release()
    cv2.destroyAllWindows()