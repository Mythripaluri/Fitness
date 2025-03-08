import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

# Global variables to track count & direction
count = 0
direction = 0
form = 0  # Ensures correct posture before counting

def left_curl():
    global count, direction, form  # Maintain values across frames
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)  # Increase width (e.g., 1920 pixels)
    cap.set(4, 1080)
    detector = pm.poseDetector()
    
    feedback = "LOWER YOUR ARM"

    with detector.pose:
        while True:
            ret, img = cap.read()  # Read frame
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) != 0:
                elbow = detector.findAngle(img, 11, 13, 15)  # Left elbow
                shoulder = detector.findAngle(img, 13, 11, 23)  # Left shoulder
                
                # Debugging print
                print(f'Elbow: {elbow}, Shoulder: {shoulder}, Count: {count}')

                # Ensure proper posture before counting
                if shoulder < 45:
                    form = 1

                # Convert elbow angle to percentage (motion progress)
                per = np.interp(elbow, (50, 160), (100, 0))
                bar = np.interp(elbow, (50, 160), (50, 380))

                if form == 1:
                    if elbow > 160:  # Arm fully extended (UP position)
                        feedback = "UP"
                        if direction == 0:  # Only count once when reaching UP
                            direction = 1  # Change direction to DOWN
                    
                    elif elbow < 50 and direction == 1:  # Only count when transitioning DOWN
                        feedback = "DOWN"
                        count += 1  # Increment the count
                        direction = 0  # Reset direction for next curl

                    else:
                        feedback = "LOWER YOUR ARM"






                #Calculate Posture Accuracy

                ideal_elbow_angle = 90  # Midpoint of motion
                ideal_shoulder_angle = 30  # Preferred shoulder position

                # Calculate error from the ideal posture
                elbow_error = abs(ideal_elbow_angle - elbow)
                shoulder_error = abs(ideal_shoulder_angle - shoulder)

                # Normalize errors to percentages (Lower error = Higher accuracy)
                elbow_accuracy = max(0, 100 - (elbow_error / ideal_elbow_angle * 100))
                shoulder_accuracy = max(0, 100 - (shoulder_error / ideal_shoulder_angle * 100))

                # Average accuracy score
                posture_accuracy = (elbow_accuracy + shoulder_accuracy) / 2


                

                # Draw progress bar
                # cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Display counter
                #cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (0, 350), (150, 500), (0, 255, 0), cv2.FILLED)

                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                #Display posture accuracy
                cv2.putText(img, f'Posture: {int(posture_accuracy)}%', (500, 80), 
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

                #Provide Feedback Based on Accuracy
                if posture_accuracy > 85:
                    feedback = ""
                elif 60 <= posture_accuracy <= 85:
                    feedback = ""
                else:
                    feedback = ""



                # Display feedback
                cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Convert frame to JPEG
                img = cv2.resize(img, (1400, 720))
                ret, jpeg = cv2.imencode('.jpg', img)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
