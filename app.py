from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
import threading
import time

app = Flask(__name__)

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global variables for video capture and pose detection
cap = None
pose = None
counter = 0
stage = None
lock = threading.Lock()

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle
    return angle

def init_camera():
    global cap, pose
    if cap is None:
        cap = cv2.VideoCapture(0)
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def generate_frames():
    global counter, stage
    
    init_camera()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make detection
        results = pose.process(image)
        
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, 
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # Calculate angle
            angle = calculate_angle(hip, knee, ankle)
            
            # Visualize angle
            cv2.putText(image, str(int(angle)), 
                        tuple(np.multiply(knee, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                        )
            
            # Squat logic
            with lock:
                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    print(f"Squat Count: {counter}")
                
        except:
            pass
        
        # Render squat count
        with lock:
            current_count = counter
        
        # Get frame dimensions
        frame_width = image.shape[1]
        frame_height = image.shape[0]
        
        # Make counter box full width of the frame
        box_height = 73
        cv2.rectangle(image, (0,0), (frame_width, box_height), (245,117,16), -1)
        cv2.putText(image, 'SQUATS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(current_count), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        
        # Yield frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/counter')
def get_counter():
    with lock:
        return jsonify({'counter': counter})

@app.route('/reset', methods=['POST'])
def reset_counter():
    global counter, stage
    with lock:
        counter = 0
        stage = None
    return jsonify({'success': True, 'counter': counter})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host=host, port=port, debug=debug, threaded=True)
