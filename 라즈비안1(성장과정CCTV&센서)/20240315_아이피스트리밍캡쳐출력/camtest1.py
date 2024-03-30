from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from time import sleep
import cv2
import os
from datetime import datetime

app = Flask(__name__)
capture = cv2.VideoCapture(0)  # 웹캠으로부터 비디오 캡처 객체 생성
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 캡처된 비디오의 폭 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 캡처된 비디오의 높이 설정

def generate_frames():
    while True:
        sleep(0.1)  # 프레임 생성 간격을 잠시 지연시킵니다.
        ref, frame = capture.read()  # 비디오 프레임을 읽어옵니다.
        if not ref:  # 비디오 프레임을 제대로 읽어오지 못했다면 반복문을 종료합니다.
            break
        else:
            ref, buffer = cv2.imencode('.jpg', frame)  # JPEG 형식으로 이미지를 인코딩합니다.
            frame = buffer.tobytes()  # 인코딩된 이미지를 바이트 스트림으로 변환합니다.
            # multipart/x-mixed-replace 포맷으로 비디오 프레임을 클라이언트에게 반환합니다.
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_latest_image():
    image_folder = os.path.join('static', 'images')
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    if image_files:
        latest_image = max(image_files)
        return os.path.join('static', 'images', latest_image)
    else:
        return None

@app.route('/')
def index():
    return render_template('camtest1.html', image_path=get_latest_image())

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture_image():
    success, frame = capture.read()
    if success:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        image_path = os.path.join('static', 'images', f"{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        return jsonify({'status': 'success', 'image_path': image_path}), 200
    else:
        return jsonify({'status': 'failed'}), 500

@app.route('/latest_image')
def latest_image():
    latest_image_path = get_latest_image()
    if latest_image_path:
        return send_from_directory('static', latest_image_path)
    else:
        return "No image available."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
