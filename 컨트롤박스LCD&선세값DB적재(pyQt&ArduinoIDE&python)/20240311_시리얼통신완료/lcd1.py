import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from serial import Serial

# 시리얼 통신을 위한 포트와 속도 설정
serial_port = '/dev/ttyACM0'  # 아두이노가 연결된 포트에 따라 변경
baud_rate = 115200

# LED 핀 번호 정의
LED_PINS = {
    "pushButton_1": 13,
    "pushButton_2": 12,
    "pushButton_3": 11
}

# LED 상태를 저장하는 딕셔너리
LED_status = {pin: False for _, pin in LED_PINS.items()}

def get_sensor_values():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="flask_login_demo"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT Temperature, Humidity FROM Dht11_data ORDER BY Timestamp DESC LIMIT 1")
    temperature_humidity = cursor.fetchone()

    cursor.execute("SELECT Soil_moisture FROM Soil_moisture_data ORDER BY Timestamp DESC LIMIT 1")
    soil_moisture = cursor.fetchone()

    cursor.execute("SELECT Intensity FROM Light_intensity_data ORDER BY Recorded_at DESC LIMIT 1")
    intensity = cursor.fetchone()

    cursor.close()
    connection.close()

    return temperature_humidity, soil_moisture, intensity

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("lcd1.ui", self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(2000)

        # 시리얼 포트 초기화
        self.serial = Serial(serial_port, baud_rate)

        # 버튼 초기 설정
        for button_name, pin in LED_PINS.items():
            button = getattr(self, button_name)
            button.clicked.connect(lambda _, p=pin: self.toggle_led(p))
            button.clicked.connect(lambda _, name=button_name: self.send_button_press(name))

        # 오토 모드 설정
        self.auto_mode = True

        # 메뉴얼 버튼 설정
        self.pushButton_4.clicked.connect(self.toggle_auto_mode)
        self.pushButton_5.clicked.connect(self.toggle_manual_mode)

        # 시작 시 오토 모드로 설정
        self.toggle_auto_mode()

        self.update_led_button_text()

    def toggle_auto_mode(self):
        self.auto_mode = True
        self.pushButton_4.setEnabled(False)  # 오토 버튼 비활성화
        self.pushButton_5.setEnabled(True)  # 매뉴얼 버튼 활성화
        for button_name in LED_PINS.keys():
            button = getattr(self, button_name)
            button.setEnabled(False)  # 푸쉬버튼 비활성화
        # 시리얼 모니터에 "A" 출력
        self.serial.write(b'A\n')
        self.serial.flush()  # 시리얼 버퍼를 비워서 즉시 전송되도록 함

    def toggle_manual_mode(self):
        self.auto_mode = False
        self.pushButton_5.setEnabled(False)  # 매뉴얼 버튼 비활성화
        self.pushButton_4.setEnabled(True)  # 오토 버튼 활성화
        for button_name in LED_PINS.keys():
            button = getattr(self, button_name)
            button.setEnabled(True)  # 푸쉬버튼 활성화
            # 모든 LED를 끄는 작업 추가
            self.toggle_led(LED_PINS[button_name], False)  # LED 끄기
        # 시리얼 모니터에 "M" 출력
        self.serial.write(b'M\n')
        self.serial.flush()  # 시리얼 버퍼를 비워서 즉시 전송되도록 함

    def update_data(self):
        temperature_humidity, soil_moisture, intensity = get_sensor_values()
        if temperature_humidity and soil_moisture and intensity:
            temperature, humidity = temperature_humidity
            self.update_display(temperature, humidity, soil_moisture[0], intensity[0])

            # 조도가 500보다 낮으면 LED_PIN2를 자동으로 켜기
            if self.auto_mode and intensity[0] < 500:
                self.toggle_led(LED_PINS["pushButton_2"])

    def update_display(self, temperature, humidity, soil_moisture, intensity):
        self.temp_label.setText("온도: {} ℃".format(temperature))
        self.humi_label.setText("습도: {} %".format(humidity))
        self.soil_label.setText("토양 수분: {}".format(soil_moisture))
        self.light_label.setText("조도: {}".format(intensity))

        # 온도에 따른 배경색 설정
        self.set_background_color(self.temp_label, temperature)

        # 습도에 따른 배경색 설정
        self.set_background_color(self.humi_label, humidity)

        # 토양 수분에 따른 배경색 설정
        self.set_background_color(self.soil_label, soil_moisture)

        # 조도에 따른 배경색 설정
        self.set_background_color(self.light_label, intensity)

    def set_background_color(self, label, value):
        if value > 30:
            color = QColor('red')
        elif value < 20:
            color = QColor('yellow')
        else:
            color = QColor('green')

        label.setAutoFillBackground(True)
        palette = label.palette()
        palette.setColor(label.backgroundRole(), color)
        label.setPalette(palette)

    def toggle_led(self, pin, on=True):
        global LED_status
        LED_status[pin] = not LED_status[pin]  # 현재 상태를 토글
        if LED_status[pin]:
            self.serial.write(b'ON,' + str(pin).encode() + b'\n')  # 아두이노에 ON 신호를 보냄
        else:
            self.serial.write(b'OFF,' + str(pin).encode() + b'\n')  # 아두이노에 OFF 신호를 보냄
            # 버튼이 OFF일 때 OFF를 시리얼 모니터에 출력
            print("OFF")
        self.update_led_button_text()

    def update_led_button_text(self):
        for button_name, pin in LED_PINS.items():
            button = getattr(self, button_name)
            if LED_status[pin]:
                button.setText("{} OFF".format(button_name))
            else:
                button.setText("{} ON".format(button_name))

    def send_button_press(self, button_name):
        if LED_status[LED_PINS[button_name]]:
            status = "ON"
        else:
            status = "OFF"
        # 버튼 이름과 상태를 아두이노로 전송
        self.serial.write("{}_{}\n".format(button_name, status).encode())
        self.serial.flush()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
