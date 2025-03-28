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
count = 0
direction = 0
form = 0  

def play_audio(text):
    """Convert text to speech and play it asynchronously."""
    tts = gTTS(text=text, lang='en')
    filename = "congrats.mp3"
    tts.save(filename)

    def play():
        music = pyglet.media.load(filename, streaming=False)
        music.play()
        pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
        pyglet.app.run()

    threading.Thread(target=play, daemon=True).start()

def squat_tracker():
    global count, direction, form

    target_count = int(input("Enter the number of squats you want to do: "))

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = pm.poseDetector()
    start_time = time.time()

    with detector.pose:
        while True:
            ret, img = cap.read()
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) != 0:
                hip = detector.findAngle(img, 24, 26, 28)   # Right Hip, Right Knee, Right Ankle
                knee = detector.findAngle(img, 26, 28, 30)  # Right Knee, Right Ankle, Right Foot

                if hip > 160:  
                    form = 1  # Ensure initial standing position

                per = np.interp(knee, (50, 160), (100, 0))  # Convert knee angle to percentage
                bar = np.interp(knee, (50, 160), (50, 380))  

                feedback = "Good"  
                if form == 1:
                    if knee > 160:  # Standing
                        feedback = "Stand Up"
                        if direction == 0:
                            direction = 1  
                    
                    elif knee < 70 and direction == 1:  # Squatting
                        feedback = "Go Up!"
                        count += 1  
                        direction = 0  

                    else:
                        feedback = "Lower More!"

                info_panel = np.zeros((120, 1280, 3), dtype=np.uint8)

                # Encouragement text
                if count >= 3 and count <= 8:
                    encouragement_text = "Great! Keep pushing!"
                    button_color = (255, 0, 0)  
                elif count > 8:
                    encouragement_text = "You are unstoppable!"
                    button_color = (0, 0, 255)  
                else:
                    encouragement_text = " "
                    button_color = (0, 255, 0)  

                # Display count
                cv2.rectangle(info_panel, (50, 20), (150, 100), button_color, cv2.FILLED)
                cv2.putText(info_panel, str(int(count)), (80, 80), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                cv2.putText(info_panel, encouragement_text, (300, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                if count >= target_count:
                    cv2.putText(info_panel, "Target Achieved!", (500, 50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    play_audio("Congratulations! You reached your goal.")
                    count = 0  

                info_panel = cv2.resize(info_panel, (img.shape[1], info_panel.shape[0]))
                final_frame = np.vstack((img, info_panel))

                # Convert frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', final_frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                # Stop after 30 minutes
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1800:
                    cv2.putText(info_panel, "Time's up! Exercise Complete.", (500, 50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    break  

    cap.release()
    cv2.destroyAllWindows()
