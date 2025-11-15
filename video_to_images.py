# video_to_images.py
import cv2, os

vid = cv2.VideoCapture('squat_video.mp4')
os.makedirs('dataset/squat_frames', exist_ok=True)
count = 0

while True:
    ret, frame = vid.read()
    if not ret:
        break
    cv2.imwrite(f'dataset/squat_frames/frame_{count}.jpg', frame)
    count += 1

vid.release()
print(f"Extracted {count} frames.")
