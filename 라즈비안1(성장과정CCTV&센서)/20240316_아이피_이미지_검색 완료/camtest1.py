from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
from datetime import datetime, timedelta

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
    start_date = datetime.strptime(request.args.get('startDate'), "%Y-%m-%d")
    end_date = datetime.strptime(request.args.get('endDate'), "%Y-%m-%d")

    # Find the latest image for each date in the selected range
    latest_images = find_latest_images(start_date, end_date)

    # Render the images as HTML with fixed size 400x300
    images_html = ''.join([f'<img src="{image}" width="400" height="300" alt="Latest Image">' for image in latest_images.values()])
    return images_html

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
