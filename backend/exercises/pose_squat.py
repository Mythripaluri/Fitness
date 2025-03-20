# import cv2
# import mediapipe as mp
# import numpy as np
# import PoseModule as pm

# def squat():
#     cap = cv2.VideoCapture(0)
#     detector = pm.poseDetector()
#     count = 0
#     direction = 0
#     form = 0
#     feedback = "STRAIGHTEN YOUR BACK"

#     with detector.pose:
#         while True:
                
#             ret, img = cap.read() #640 x 480


#             img = detector.findPose(img, False)
#             lmList = detector.findPosition(img, False)
#             # print(lmList)
#             if len(lmList) != 0:
#                 shoulder = detector.findAngle(img, 7, 11, 23)
#                 knee = detector.findAngle(img, 23, 25, 27)
                
#                 #Percentage of success of pushup
#                 per = np.interp(knee, (90, 160), (0, 100))
                
#                 #Bar to show Pushup progress
#                 bar = np.interp(knee, (90, 160), (380, 50))

#                 #Check to ensure right form before starting the program
#                 if shoulder > 160:
#                     form = 1
            
#                 #Check for full range of motion for the pushup
#                 if form == 1:
#                     if per == 0:
#                         if knee <= 90 and shoulder > 160:
#                             feedback = "UP"
#                             if direction == 0:
#                                 count += 0.5
#                                 direction = 1
#                         else:
#                             feedback = "STRAIGHTEN YOUR BACK"
                            
#                     if per == 100:
#                         if shoulder > 160 and knee > 160:
#                             feedback = "DOWN"
#                             if direction == 1:
#                                 count += 0.5
#                                 direction = 0
#                         else:
#                             feedback = "STRAIGHTEN YOUR BACK"
#                                 # form = 0

#                 print(count)
                
#                 #Draw Bar
#                 if form == 1:
#                     cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
#                     cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
#                     cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2,
#                                 (255, 255, 0), 2)


#                 #Pushup counter
#                 cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
#                 cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
#                             (255, 0, 0), 5)
                
#                 #Feedback 
                
#                 cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
#                             (255, 255, 0), 2)

                
#             # Convert the frame to JPEG format
#                 ret, jpeg = cv2.imencode('.jpg', img)

#                 # Yield the frame as a bytes-like object
#                 yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')





import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
from gtts import gTTS
import pyglet  # Alternative to playsound
import threading
import time

# Global variables to track count & direction
count = 0
direction = 0
form = 0
feedback = "STRAIGHTEN YOUR BACK"

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

def squat(target_reps, target_sets):
    global count, direction, form, feedback

    # Get user input for target count
    
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    start_time = time.time()  # Track the start time to limit exercise duration to 30 minutes

    with detector.pose:
        while True:
            ret, img = cap.read()  # Read frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) != 0:
                shoulder = detector.findAngle(img, 7, 11, 23)
                knee = detector.findAngle(img, 23, 25, 27)
                
                # Percentage of success of squat
                per = np.interp(knee, (90, 160), (0, 100))
                bar = np.interp(knee, (90, 160), (380, 50))  # Bar for progress

                # Check for proper form before starting
                if shoulder > 160:
                    form = 1

                # Squat motion detection
                if form == 1:
                    if per == 0:
                        if knee <= 90 and shoulder > 160:
                            feedback = "UP"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                    if per == 100:
                        if shoulder > 160 and knee > 160:
                            feedback = "DOWN"
                            if direction == 1:
                                count += 0.5
                                direction = 0

                # Provide feedback based on squat progress
                info_panel = np.zeros((120, 1280, 3), dtype=np.uint8)

                if count >= 3 and count <= 8:
                    encouragement_text = "Good! Keep it up!"
                    button_color = (255, 0, 0)  # Red for motivation
                elif count > 8:
                    encouragement_text = "You are amazing!!"
                    button_color = (0, 0, 255)  # Blue for encouragement
                else:
                    encouragement_text = " "
                    button_color = (0, 255, 0)  # Green for starting point

                cv2.rectangle(info_panel, (50, 20), (150, 100), button_color, cv2.FILLED)
                cv2.putText(info_panel, str(int(count)), (80, 80), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                cv2.putText(info_panel, encouragement_text, (300, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Check if target count is achieved
                if count >= target_count:
                    cv2.putText(info_panel, "Target Achieved!", (500, 50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)

                    play_audio("Congratulations! You reached your goal.")  # Play TTS audio
                    count = 0  # Reset count for next goal

                # Add progress bar and squat count to the image
                cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Squat counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                # Feedback message
                cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Display the final frame with feedback
                final_frame = np.vstack((img, info_panel))

                # Convert frame to JPEG format
                ret, jpeg = cv2.imencode('.jpg', final_frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                # Stop exercising after 30 minutes
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1800:  # 30 minutes
                    cv2.putText(info_panel, "Time's up! Exercise Complete.", (500, 50), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    break  # Exit the loop after 30 minutes

    cap.release()
    cv2.destroyAllWindows()
