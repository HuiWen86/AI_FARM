import os
import base64
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 이미지가 저장될 폴더 설정
CAPTURED_IMAGES_FOLDER = os.path.join(app.static_folder, 'images')
if not os.path.exists(CAPTURED_IMAGES_FOLDER):
    os.makedirs(CAPTURED_IMAGES_FOLDER)

@app.route('/')
def index():
    return render_template('camtest.html')

@app.route('/get_images', methods=['GET'])
def get_images():
    images = []
    # 이미지 폴더에서 모든 이미지 파일을 가져와서 내림차순으로 정렬
    for filename in sorted(os.listdir(CAPTURED_IMAGES_FOLDER), reverse=True):
        if filename.endswith('.jpg'):
            image_path = os.path.join('/static/images', filename)
            images.append({'name': filename, 'path': image_path})
    return jsonify(images)

@app.route('/capture', methods=['POST'])
def capture():
    try:
        image_data = request.form['image']
        # 이미지 파일로 저장
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(CAPTURED_IMAGES_FOLDER, now + '.jpg')
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(image_data.split(',')[1]))
        # 이미지 파일의 경로를 클라이언트로 전송
        return jsonify({'image_path': '/static/images/' + now + '.jpg'})
    except Exception as e:
        error_message = str(e)
        print("Error while capturing image:", error_message)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
