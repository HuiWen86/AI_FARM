from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# 이미지 저장 디렉토리 설정
SAVE_DIR = 'captured_images'

# 이미지 저장 디렉토리가 없는 경우 생성
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 캡처 버튼 클릭 시 이미지 저장하는 함수
def save_image(frame):
    if frame is None:
        return False, 'Empty frame'
    
    # 현재 시간을 기준으로 이미지 파일 이름 생성
    now = datetime.now()
    image_name = now.strftime('%Y%m%d%H%M%S') + '.jpg'

    # 이미지 파일 경로 생성
    image_path = os.path.join(SAVE_DIR, image_name)

    # 이미지 저장
    success = cv2.imwrite(image_path, frame)
    return success, image_path

# 카메라 스트리밍을 위한 함수
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 프레임을 JPEG 형식으로 인코딩하여 바이트로 변환
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # 스트리밍
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # 카메라 닫기
    camera.release()

@app.route('/')
def index():
    # HTML 템플릿 렌더링
    return render_template('camtest.html')

@app.route('/video_feed')
def video_feed():
    # 프레임을 스트리밍하여 응답 생성
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 캡처 버튼 클릭 시 캡처하는 엔드포인트
@app.route('/capture_image', methods=['POST'])
def capture_image():
    # 카메라 열기
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    success, image_path = save_image(frame)
    # 카메라 닫기
    camera.release()
    if success:
        return jsonify({'success': True, 'image_path': image_path})
    else:
        return jsonify({'success': False, 'error': 'Failed to capture image'})

if __name__ == '__main__':
    app.run(debug=True)
