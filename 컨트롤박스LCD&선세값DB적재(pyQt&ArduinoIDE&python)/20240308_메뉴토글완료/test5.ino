#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define BUZZER_PIN 7       // 피에조 부저 핀
#define DHTPIN 2            // DHT11 센서 핀
#define DHTTYPE DHT11       // DHT 센서 타입
#define SOIL_MOISTURE_PIN A0 // 토양 수분 센서 핀
#define LIGHT_SENSOR_PIN A1 // 조도 센서 핀
#define LED_PIN1 13         // LED 핀
#define LED_PIN2 12
#define LED_PIN3 11
#define FAN_RELAY 4

bool ledState1 = false;
bool ledState2 = false;
bool ledState3 = false;
bool autoMode = true;

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD 주소와 행/열 설정

void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN1, OUTPUT); // LED 핀을 출력으로 설정
  pinMode(LED_PIN2, OUTPUT);
  pinMode(LED_PIN3, OUTPUT);

  pinMode(BUZZER_PIN, OUTPUT); // 피에조 부저 핀을 출력으로 설정
  pinMode(FAN_RELAY, OUTPUT);

  dht.begin();

  // LCD 초기화
  lcd.init();
  lcd.backlight(); // 백라이트 활성화

  // 자동모드 시작
  Serial.println("A");
}

void loop() {
  // 온습도 센서 값 읽기
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // 토양 수분 센서 값 읽기
  int soil_moisture = analogRead(SOIL_MOISTURE_PIN);

  // 조도 센서 값 읽기
  int light_intensity = analogRead(LIGHT_SENSOR_PIN);

  // 시리얼로 값을 출력
  Serial.print("Soil Moisture: ");
  Serial.print(soil_moisture);
  Serial.print("  Humidity: ");
  Serial.print(humidity);
  Serial.print("%  Temperature: ");
  Serial.print(temperature);
  Serial.print("°C  Light Intensity: ");
  Serial.println(light_intensity);

  // 조도가 500보다 낮은 경우 LED2 켜기
  if (autoMode && light_intensity < 500) {
    digitalWrite(LED_PIN2, HIGH);
  } else {
    digitalWrite(LED_PIN2, LOW);
  }

  delay(2000); // 2초 간격으로 값을 출력
}

void serialEvent() {
  if (Serial.available()) {
    char receivedChar = Serial.read();
    if (receivedChar == 'A') {
      autoMode = true;
    } else if (receivedChar == 'M') {
      autoMode = false;
    }
  }
}
