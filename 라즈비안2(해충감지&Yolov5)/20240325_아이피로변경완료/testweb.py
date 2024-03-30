from flask import Flask, render_template, Response
import cv2
import torch
import yaml
from flask_socketio import SocketIO, emit
import os
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # 모든 origin 허용

# 객체 감지 정보를 저장할 리스트
detected_objects = []

# 이미지를 저장할 디렉토리
CAPTURE_DIR = "/home/jang/flask_app/static/images/detect"
if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)

@app.route('/')
def index():
    return render_template('testweb.html')

def detect_objects():
    model_path = "/home/jang/opencv-venv/yolov5/worms1/best.pt"
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    data_path = "/home/jang/opencv-venv/yolov5/worms1/data.yaml"
    with open(data_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    class_names = data['names']

    cap = cv2.VideoCapture(0)
    detection_started = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img = frame[:, :, ::-1]

        results = model(img)

        if not detection_started:
            print("감지를 시작합니다.")
            detection_started = True
            socketio.emit('object_detection_started')  # 감지 시작 이벤트 전송

        # 현재 프레임에서 감지된 객체 정보를 리스트에 추가
        frame_objects = []
        for detection in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = detection.tolist()
            class_name = class_names[int(cls)]
            percent = int(conf * 100)
            label = f'{class_name} {percent}%'

            # 초록색 박스 그리기
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # 객체 감지 정보를 저장
            object_info = {
                'class_name': class_name,
                'confidence': percent,
                'x1': int(x1),
                'y1': int(y1),
                'x2': int(x2),
                'y2': int(y2)
            }
            frame_objects.append(object_info)

            # 초록색 박스 위에 확률 표시
            cv2.putText(frame, f'{percent}%', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 객체가 감지되었을 때만 화면 캡쳐 및 저장
        if frame_objects:
            capture_time = datetime.now().strftime("%Y%m%d%H%M%S")
            image_name = f"{capture_time}.jpg"
            image_path = os.path.join(CAPTURE_DIR, image_name)
            cv2.imwrite(image_path, frame)
            socketio.emit('object_detection_log', {'message': f'{capture_time} 확률: 100% 캡쳐된 이미지: {image_path}'})

        # 현재 프레임에서 감지된 객체 정보를 전역 변수에 저장
        global detected_objects
        detected_objects = frame_objects

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)  # 원하는 IP 주소와 포트로 설정