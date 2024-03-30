import os
import base64
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import mysql.connector

app = Flask(__name__)

# MySQL 연결 설정
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="flask_login_demo"
)

# 이미지가 저장될 폴더 설정
CAPTURED_IMAGES_FOLDER = os.path.join(app.static_folder, 'images')
if not os.path.exists(CAPTURED_IMAGES_FOLDER):
    os.makedirs(CAPTURED_IMAGES_FOLDER)

# 마지막으로 캡처된 이미지의 경로를 저장하는 변수
last_captured_image_path = None

@app.route('/')
def index():
    # 어제 날짜와 오늘 날짜 계산
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('camtest1.html', yesterday=yesterday, today=today)

@app.route('/get_images', methods=['GET'])
def get_images():
    images = []
    # 이미지 폴더에서 모든 이미지 파일을 가져와서 내림차순으로 정렬
    for filename in sorted(os.listdir(CAPTURED_IMAGES_FOLDER), reverse=True):
        if filename.endswith('.jpg'):
            image_path = os.path.join('/static/images', filename)
            images.append({'name': filename, 'path': image_path})
    return jsonify(images)

@app.route('/get_soil_moisture_data', methods=['GET'])
def get_soil_moisture_data():
    try:
        selected_date = request.args.get('date')
        cursor = mydb.cursor()
        cursor.execute("SELECT MAX(Soil_moisture) AS Soil_moisture, TIMESTAMP FROM Soil_moisture_data WHERE DATE(Timestamp) = %s GROUP BY HOUR(Timestamp)", (selected_date,))
        results = cursor.fetchall()
        soil_moisture_values = [result[0] for result in results]
        timestamps = [result[1].strftime("%Y-%m-%d %H:%M:%S") for result in results]
        return jsonify({'soil_moisture_values': soil_moisture_values, 'timestamps': timestamps})
    except Exception as e:
        error_message = str(e)
        print("Error while fetching soil moisture data:", error_message)
        return jsonify({'error': error_message}), 500

@app.route('/get_air_humidity_data', methods=['GET'])
def get_air_humidity_data():
    try:
        selected_date = request.args.get('date')
        cursor = mydb.cursor()
        cursor.execute("SELECT Humidity, MAX(Timestamp) FROM Dht11_data WHERE DATE(Timestamp) = %s GROUP BY HOUR(Timestamp)", (selected_date,))
        results = cursor.fetchall()
        humidity_values = []
        timestamps = []
        if results:
            humidity_values = [result[0] for result in results]
            timestamps = [result[1].strftime("%Y-%m-%d %H:%M:%S") for result in results]
        return jsonify({'humidity_values': humidity_values, 'timestamps': timestamps})
    except Exception as e:
        error_message = str(e)
        print("Error while fetching air humidity data:", error_message)
        return jsonify({'error': error_message}), 500

@app.route('/get_air_temperature_data', methods=['GET'])
def get_air_temperature_data():
    try:
        selected_date = request.args.get('date')
        cursor = mydb.cursor()
        cursor.execute("SELECT Temperature, MAX(Timestamp) FROM Dht11_data WHERE DATE(Timestamp) = %s GROUP BY HOUR(Timestamp)", (selected_date,))
        results = cursor.fetchall()
        temperature_values = [result[0] for result in results]
        timestamps = [result[1].strftime("%Y-%m-%d %H:%M:%S") for result in results]
        return jsonify({'temperature_values': temperature_values, 'timestamps': timestamps})
    except Exception as e:
        error_message = str(e)
        print("Error while fetching air temperature data:", error_message)
        return jsonify({'error': error_message}), 500

@app.route('/get_light_intensity_data', methods=['GET'])
def get_light_intensity_data():
    try:
        selected_date = request.args.get('date')
        cursor = mydb.cursor()
        cursor.execute("SELECT Intensity, MAX(Recorded_at) FROM Light_intensity_data WHERE DATE(Recorded_at) = %s GROUP BY HOUR(Recorded_at)", (selected_date,))
        results = cursor.fetchall()
        intensity_values = [result[0] for result in results]
        timestamps = [result[1].strftime("%Y-%m-%d %H:%M:%S") for result in results]
        return jsonify({'intensity_values': intensity_values, 'timestamps': timestamps})
    except Exception as e:
        error_message = str(e)
        print("Error while fetching light intensity data:", error_message)
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

        # 이미지를 파일명을 기준으로 정렬
        images.sort(key=lambda x: x['name'])

        # 각 날짜별로 마지막 이미지만 가져오기
        last_images = {}
        for image in images:
            file_date = image['name'].split('.')[0][:8]
            last_images[file_date] = image

        # 마지막 이미지만 반환
        last_images = list(last_images.values())

        return jsonify({'images': last_images, 'image_folder': CAPTURED_IMAGES_FOLDER})
    except Exception as e:
        error_message = str(e)
        print("Error while searching images:", error_message)
        return jsonify({'error': error_message}), 500

@app.route('/chart')
def show_chart_page():
    return render_template('chart.html')

@app.route('/chart2')
def show_chart():
    return render_template('chart2.html')

@app.route('/chart3')
def show_chart3():
    return render_template('chart3.html')

@app.route('/chart4')
def show_chart4():
    return render_template('chart4.html')

@app.route('/analyze_images', methods=['POST'])
def analyze_images():
    try:
        image_paths = request.json['image_paths']

        black_ratios = []
        for image_path in image_paths:
            # 이미지 불러오기
            image = cv2.imread(os.path.join(app.static_folder, image_path.strip('/')))
            # 그레이스케일 변환
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 이진화
            _, binary_image = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY)
            # 검정색 픽셀 수 계산
            black_pixels = np.sum(binary_image == 0)
            # 전체 픽셀 수 계산
            total_pixels = binary_image.size
            # 검정색 픽셀 비율 계산
            black_ratio = black_pixels / total_pixels * 100
            black_ratios.append(black_ratio)

        return jsonify({'black_ratios': black_ratios})
    except Exception as e:
        error_message = str(e)
        print("Error while analyzing images:", error_message)
        return jsonify({'error': error_message}), 500

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
