import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
from gtts import gTTS
import pyglet  # Alternative to playsound
import threading
import time

# Global variables to track count & direction
total_count = 0
direction = 0
form = 0
feedback = "LOWER YOUR WAIST"

# Function to play audio feedback
def play_audio(text):
    tts = gTTS(text=text, lang='en')
    filename = "congrats.mp3"
    tts.save(filename)

    def play():
        music = pyglet.media.load(filename, streaming=False)
        music.play()
        pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
        pyglet.app.run()

    threading.Thread(target=play, daemon=True).start()

def pushup(target_reps, target_sets):
    global total_count, direction, form, feedback

    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    set_count = 0

    start_time = time.time()  # Track start time to limit exercise duration to 30 minutes

    with detector.pose:
        while set_count < target_sets:
            count = 0
            while count < target_reps:
                ret, img = cap.read()
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)

                if len(lmList) != 0:
                    elbow = detector.findAngle(img, 11, 13, 15)  # Right elbow
                    shoulder = detector.findAngle(img, 13, 11, 23)  # Right shoulder
                    hip = detector.findAngle(img, 11, 23, 25)  # Hip

                    # Percentage of pushup progress
                    per = np.interp(elbow, (90, 160), (0, 100))
                    bar = np.interp(elbow, (90, 160), (380, 50))  # Progress bar position

                    # Check proper form before starting
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        form = 1

                    # Pushup detection
                    if form == 1:
                        if per == 0:
                            if elbow <= 90 and hip > 160:
                                feedback = "UP"
                                if direction == 0:
                                    count += 0.5
                                    total_count += 0.5
                                    direction = 1
                        if per == 100:
                            if elbow > 160 and shoulder > 40 and hip > 160:
                                feedback = "DOWN"
                                if direction == 1:
                                    count += 0.5
                                    total_count += 0.5
                                    direction = 0

                    # UI Display
                    info_panel = np.zeros((120, 1280, 3), dtype=np.uint8)
                    encouragement_text = "Keep pushing!" if count < target_reps else "Set Complete!"
                    # Feedback Message
                    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    # Combine Frames
                    info_panel_resized = cv2.resize(info_panel, (img.shape[1], info_panel.shape[0]))
                    final_frame = np.vstack((img, info_panel_resized))


                    # Convert to JPEG
                    ret, jpeg = cv2.imencode('.jpg', final_frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                # Check time limit (30 min)
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1800:
                    cv2.putText(info_panel, "Time's up! Exercise Complete.", (500, 50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    break

            # After completing a set
            set_count += 1
            if set_count < target_sets:
                play_audio(f"Set {set_count} complete! Take a break.")
                rest_time = 30  # Rest time in seconds
                for i in range(rest_time, 0, -1):
                    print(f"Rest for {i} seconds...", end='\r')
                    time.sleep(1)

        # Final completion message
        play_audio("Congratulations! You completed all sets.")
        print("Workout complete!")

    cap.release()
    cv2.destroyAllWindows()
