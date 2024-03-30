from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import cv2
import numpy as np
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1111',
    'database': 'flask_login_demo'
}

# Webcam streaming function
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Login Manager setup
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        user = User()
        user.id = user_data[0]
        return user
    else:
        return None

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            user = User()
            user.id = user_data[0]
            login_user(user)
            return redirect(url_for('welcome'))
        else:
            return "Invalid username or password"
    else:
        return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Welcome page with webcam streaming and sensor data
@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

# Video feed for webcam streaming
@app.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint to fetch sensor data
@app.route('/sensor_data')
@login_required
def sensor_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Retrieve DHT11 sensor data
    cursor.execute("SELECT * FROM Dht11_data ORDER BY id DESC")
    dht11_data = cursor.fetchall()

    # Retrieve soil moisture sensor data
    cursor.execute("SELECT * FROM Soil_moisture_data ORDER BY id DESC")
    soil_moisture_data = cursor.fetchall()

    # Retrieve light intensity sensor data
    cursor.execute("SELECT * FROM Light_intensity_data ORDER BY id DESC")
    light_intensity_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(dht11_data=dht11_data, soil_moisture_data=soil_moisture_data, light_intensity_data=light_intensity_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
