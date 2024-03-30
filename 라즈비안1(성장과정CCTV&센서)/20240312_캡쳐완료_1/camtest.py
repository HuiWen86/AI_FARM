from flask import Flask, render_template, request, jsonify
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('camtest.html')

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.form['image']
    # 이미지 데이터를 클라이언트로 반환
    return jsonify({'data_url': image_data})

if __name__ == '__main__':
    app.run(debug=True)
