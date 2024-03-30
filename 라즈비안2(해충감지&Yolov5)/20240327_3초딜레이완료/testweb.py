from flask import Flask, render_template, Response
from imutils.video import VideoStream
import cv2
import torch
import yaml
from flask_socketio import SocketIO
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# YOLOv5 model and class names loading
model = None
class_names = []

# Directory to store images
CAPTURE_DIR = "static/images/detect"
if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)

# Flag to control object detection thread
detection_active = False

# Adjust camera streaming speed (in frames per second)
STREAMING_SPEED = 10  # Increased streaming speed to 10 frames per second

def load_model():
    global model, class_names
    model_path = "/home/jang/opencv-venv/yolov5/worms1/best.pt"
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    data_path = "/home/jang/opencv-venv/yolov5/worms1/data.yaml"
    with open(data_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    class_names = data['names']

def detect_objects_thread(vs):
    global detection_active
    while detection_active:
        frame = vs.read()
        if frame is None:
            print("Error: Failed to read frame from camera.")
            break

        img = frame[:, :, ::-1]
        results = model(img)

        frame_objects = []
        last_detection = None
        for detection in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = detection.tolist()
            class_name = class_names[int(cls)]
            percent = int(conf * 100)
            label = f'{class_name} {percent}%'

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Draw green box
            cv2.putText(frame, f'{percent}%', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Display confidence

            frame_objects.append({'class_name': class_name, 'confidence': percent})
            last_detection = {'class_name': class_name, 'confidence': percent}

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        if frame_objects:
            capture_time = datetime.now().strftime("%Y%m%d%H%M%S")
            image_name = f"{capture_time}.jpg"
            image_path = os.path.join(CAPTURE_DIR, image_name)
            cv2.imwrite(image_path, frame)
            for obj in frame_objects:
                message = f"[{capture_time}] {obj['class_name']} 확률: {obj['confidence']}%"
                socketio.emit('object_detection_log', {'message': message, 'image_path': f"/{image_path}"})

        if last_detection:
            capture_time = datetime.now().strftime("%Y%m%d%H%M%S")
            message = f"[{capture_time}] {last_detection['class_name']} 확률: {last_detection['confidence']}%"
            socketio.emit('last_object_detection', {'message': message, 'image_path': f"/{image_path}"})

@app.route('/')
def index():
    return render_template('testweb.html')

@app.route('/video_feed')
def video_feed():
    global detection_active
    detection_active = True
    vs = VideoStream(src=0).start()
    return Response(detect_objects_thread(vs), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    load_model()
    threading.Thread(target=detect_objects_thread).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)