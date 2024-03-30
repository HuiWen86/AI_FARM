from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import os
from datetime import datetime, timedelta
import mysql.connector
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)
images_folder = "static/images"

# MySQL 연결 설정
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="flask_login_demo"
)

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

def find_latest_images(start_date, end_date):
    latest_images = {}
    current_date = start_date
    while current_date <= end_date:
        # Format the current date
        current_date_str = current_date.strftime("%Y%m%d")
        # Find images for the current date
        images_for_date = [filename for filename in os.listdir(images_folder) if filename.startswith(current_date_str)]
        if images_for_date:
            # Sort images by creation time and get the latest one
            latest_image = max(images_for_date, key=lambda x: os.path.getctime(os.path.join(images_folder, x)))
            latest_images[current_date_str] = os.path.join(images_folder, latest_image)
        # Move to the next date
        current_date += timedelta(days=1)
    return latest_images

@app.route('/')
def index():
    latest_image_path = None
    if len(os.listdir(images_folder)) > 0:
        latest_image_path = max([os.path.join(images_folder, f) for f in os.listdir(images_folder)], key=os.path.getctime)
    return render_template('camtest1.html', latest_image=latest_image_path)

@app.route('/stream')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    capture_image()
    return redirect(url_for('index'))

@app.route('/search')
def search_images():
    try:
        start_date = datetime.strptime(request.args.get('startDate'), "%Y-%m-%d")
        end_date = datetime.strptime(request.args.get('endDate'), "%Y-%m-%d")
        # Find the latest image for each date in the selected range
        latest_images = find_latest_images(start_date, end_date)
        # Render the images as HTML with fixed size 400x300
        images_html = ''
        for date, image_path in latest_images.items():
            image = cv2.imread(image_path)
            green_pixels = np.sum((image[:,:,1] > 100) & (image[:,:,0] < 100) & (image[:,:,2] < 100))
            total_pixels = image.shape[0] * image.shape[1]
            green_percentage = (green_pixels / total_pixels) * 100
            images_html += f'<div><img src="{image_path}" width="400" height="300" alt="Latest Image">' \
                           f'<p>Green Pixels: {green_percentage:.2f}%</p></div>'
        return images_html
    except Exception as e:
        error_message = str(e)
        print("Error while searching images:", error_message)
        return jsonify({'error': error_message}), 500

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

@app.route('/chart')
def chart():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('chart.html', date=today)

@app.route('/chart2')
def chart2():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('chart2.html', date=today)

@app.route('/chart3')
def chart3():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('chart3.html', date=today)

@app.route('/chart4')
def chart4():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('chart4.html', date=today)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
