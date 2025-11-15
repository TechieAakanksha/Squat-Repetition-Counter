import cv2
import mediapipe as mp
import numpy as np
import sqlite3
import time
from playsound import playsound
import pyttsx3

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # speech speed

# Database Setup
conn = sqlite3.connect('squat_progress.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    squats INTEGER
                )''')
conn.commit()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def save_progress(count):
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO progress (date, squats) VALUES (?, ?)", (date, count))
    conn.commit()

def speak(text):
    engine.say(text)
    engine.runAndWait()

cap = cv2.VideoCapture(0)
counter = 0
stage = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            angle = calculate_angle(hip, knee, ankle)
            
            cv2.putText(image, str(round(angle, 2)), 
                        tuple(np.multiply(knee, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Counting Logic
            if angle > 160:
                stage = "up"
            if angle < 90 and stage == "up":
                stage = "down"
                counter += 1
                print(f"Squat Count: {counter}")
                playsound('beep.mp3')  # Put a short beep file in the same folder
                speak(str(counter))
                save_progress(counter)
                
        except:
            pass
        
        # Counter Display
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        cv2.putText(image, 'SQUATS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(image, str(counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

        cv2.imshow('Pose Squat Counter', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
conn.close()
cv2.destroyAllWindows()

