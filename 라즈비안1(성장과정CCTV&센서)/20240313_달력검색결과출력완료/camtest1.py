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
    return render_template('camtest1.html')

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

@app.route('/search_images', methods=['POST'])
def search_images():
    try:
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # 입력된 날짜를 YYYYMMDD 형식으로 변환
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")

        images = []
        for filename in os.listdir(CAPTURED_IMAGES_FOLDER):
            if filename.endswith('.jpg'):
                file_date = filename.split('.')[0]
                # 파일명의 날짜 부분만 추출하여 YYYYMMDD 형식으로 변환
                file_date = file_date[:8]
                if start_datetime <= file_date <= end_datetime:
                    image_path = os.path.join('/static/images', filename)
                    images.append({'name': filename, 'path': image_path})

        return jsonify({'images': images})
    except Exception as e:
        error_message = str(e)
        print("Error while searching images:", error_message)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
