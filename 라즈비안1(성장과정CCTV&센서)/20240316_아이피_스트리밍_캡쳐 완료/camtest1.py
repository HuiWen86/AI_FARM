from flask import Flask, render_template, Response, request
import cv2
import os
from datetime import datetime

app = Flask(__name__)
camera = cv2.VideoCapture(0)
images_folder = "static/images"

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Resize frame to 400x300
            frame = cv2.resize(frame, (400, 300))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_image():
    success, frame = camera.read()
    if success:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        filename = os.path.join(images_folder, f"{timestamp}.jpg")
        cv2.imwrite(filename, frame)

@app.route('/')
def index():
    return render_template('camtest1.html')

@app.route('/stream')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    capture_image()
    latest_image_path = max([os.path.join(images_folder, f) for f in os.listdir(images_folder)], key=os.path.getctime)
    return render_template('camtest1.html', latest_image=latest_image_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
