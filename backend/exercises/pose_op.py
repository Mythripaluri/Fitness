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
reps = 0
sets = 0
direction = 0
form = 0  # Ensures correct posture before counting
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

def op(target_reps, target_sets):
    global reps, sets, direction, form, last_audio_message, message_timer, final_message_shown
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        feedback = "Raise Your Arms!"
        if len(lmList) != 0:
            left_shoulder = detector.findAngle(img, 11, 13, 15)
            right_shoulder = detector.findAngle(img, 12, 14, 16)

            if left_shoulder > 150 and right_shoulder > 150:
                form = 1

            if form == 1:
                if left_shoulder >= 175 and right_shoulder >= 175:
                    feedback = "UP"
                    if direction == 0:
                        direction = 1
                elif left_shoulder <= 90 and right_shoulder <= 90 and direction == 1:
                    feedback = "DOWN"
                    reps += 1
                    direction = 0

                    if reps >= target_reps:
                        if sets < target_sets:
                            sets += 1
                            reps = 0
                            play_audio("You have completed a set!")

                        if sets >= target_sets and not final_message_shown:
                            final_message_shown = True
                            play_audio("Target Achieved!!")

            posture_accuracy = max(0, min(100, 100 - abs(135 - (left_shoulder + right_shoulder) // 2)))

            if posture_accuracy > 85:
                feedback = "Perfect Form!"
            elif 50 <= posture_accuracy <= 85:
                feedback = "Good, but adjust slightly."
            else:
                feedback = "Fix Your Posture!"

        frame_width = img.shape[1]
        info_panel = np.zeros((150, frame_width, 3), dtype=np.uint8)

        cv2.putText(info_panel, f"Sets: {sets}/{target_sets}", (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Reps: {reps}", (50, 90), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Feedback: {feedback}", (50, 130), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        img[0:150, :] = info_panel

        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()