from flask import Flask, Response, render_template
import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
from gtts import gTTS
import threading
import time
import pyglet

app = Flask(__name__)

# Global variables
count = 0
sets = 0
direction = 0
form = 1  
last_audio_message = None  
message_timer = 0  
final_message_shown = False  

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

def lunges(target_reps, target_sets):
    global count, sets, direction, form, last_audio_message, message_timer, final_message_shown
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        feedback = "Step Forward!"
        if len(lmList) != 0:
            left_knee = detector.findAngle(img, 23, 25, 27)
            right_knee = detector.findAngle(img, 24, 26, 28)
            torso_angle = detector.findAngle(img, 11, 23, 25)
            
            if left_knee > 140 and right_knee > 140:
                form = 1
            
            if form == 1:
                if left_knee >= 160 and right_knee >= 160 and direction == 0:
                    direction = 1
                elif left_knee <= 105 and right_knee <= 105 and direction == 1:
                    count += 1
                    direction = 0
                    print(f"Set {sets}/{target_sets}, Reps {count}/{target_reps}")
                    
                    if count >= target_reps:
                        if sets < target_sets:
                            sets += 1
                            count = 0
                            print(f"Set {sets}/{target_sets} completed")
                        if sets >= target_sets and not final_message_shown:
                            final_message_shown = True
                            print("Target Achieved!!")
            
            posture_accuracy = max(0, min(100, 100 - abs(120 - torso_angle)))
            
            if posture_accuracy > 85:
                feedback = "Perfect Form!"
            elif 60 <= posture_accuracy <= 85:
                feedback = "Good, but adjust slightly."
            else:
                feedback = "Fix Your Posture!"
        
        frame_width = img.shape[1]
        info_panel = np.zeros((150, frame_width, 3), dtype=np.uint8)
        
        cv2.putText(info_panel, f"Sets: {sets}/{target_sets}", (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Reps: {count}/{target_reps}", (50, 90), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Feedback: {feedback}", (50, 130), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        img[0:150, :] = info_panel
        
        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()