
import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

# Global variables to track count & direction
count = 0
direction = 0
form = 0  # Ensures correct posture before counting

def right_curl():
    global count, direction, form  # Maintain values across frames
    
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    
    feedback = "LOWER YOUR ARM"

    with detector.pose:
        while True:
            ret, img = cap.read()  # Read frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) != 0:
                elbow = detector.findAngle(img, 12, 14, 16)  # Right elbow
                shoulder = detector.findAngle(img, 14, 12, 24)  # Right shoulder
                
                # Debugging print
                print(f'Elbow: {elbow}, Shoulder: {shoulder}, Count: {count}')

                # Ensure proper posture before counting
                if shoulder < 45:
                    form = 1

                # Convert elbow angle to percentage (motion progress)
                per = np.interp(elbow, (50, 160), (100, 0))
                bar = np.interp(elbow, (50, 160), (50, 380))

                # Curl Motion Detection
                if form == 1:
                    if elbow > 160:  # Arm fully extended (UP position)
                        feedback = "UP"
                        if direction == 0:  # Only count once when reaching UP
                            count += 1
                            direction = 1  # Change direction to DOWN
                    
                    elif elbow < 50 and direction==1:  # Arm fully bent (DOWN position)
                        feedback = "DOWN"
                        count+=1
                        direction = 0  # Reset direction for next curl

                    else:
                        feedback = "LOWER YOUR ARM"

                # Draw progress bar
                # cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Display counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                # Display feedback
                cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Convert frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', img)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
