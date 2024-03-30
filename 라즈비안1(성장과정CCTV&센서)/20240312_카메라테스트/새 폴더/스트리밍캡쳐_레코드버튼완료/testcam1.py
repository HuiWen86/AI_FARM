from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def generate_frames():
    # 카메라 열기
    camera = cv2.VideoCapture(0)

    while True:
        # 프레임 읽기
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
    return render_template('testcam1.html')

@app.route('/video_feed')
def video_feed():
    # 프레임을 스트리밍하여 응답 생성
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
