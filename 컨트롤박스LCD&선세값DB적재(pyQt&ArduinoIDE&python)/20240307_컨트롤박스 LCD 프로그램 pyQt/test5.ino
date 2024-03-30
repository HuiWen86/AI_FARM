
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
  //if (light_intensity < 500) {
  //  digitalWrite(LED_PIN2, HIGH);
  //} else {
  //  digitalWrite(LED_PIN2, LOW);
  //}

  // LED 상태를 시리얼 포트를 통해 보내기
  Serial.print("STATUS,");
  Serial.print(LED_PIN1);
  Serial.println(ledState1 ? ",ON" : ",OFF");

  Serial.print("STATUS,");
  Serial.print(LED_PIN2);
  Serial.println(ledState2 ? ",ON" : ",OFF");

  Serial.print("STATUS,");
  Serial.print(LED_PIN3);
  Serial.println(ledState3 ? ",ON" : ",OFF");

  // 시리얼 입력을 처리
  if (Serial.available() > 0) {
    String receivedData = Serial.readStringUntil('\n');
    if (receivedData.startsWith("ON")) {
      int ledPin = receivedData.substring(receivedData.indexOf(',') + 1).toInt();
      if (ledPin == LED_PIN1)
        ledState1 = true;
      else if (ledPin == LED_PIN2)
        ledState2 = true;
      else if (ledPin == LED_PIN3)
        ledState3 = true;
      digitalWrite(ledPin, HIGH);
    }
    else if (receivedData.startsWith("OFF")) {
      int ledPin = receivedData.substring(receivedData.indexOf(',') + 1).toInt();
      if (ledPin == LED_PIN1)
        ledState1 = false;
      else if (ledPin == LED_PIN2)
        ledState2 = false;
      else if (ledPin == LED_PIN3)
        ledState3 = false;
      digitalWrite(ledPin, LOW);
    }
  }

  // LCD에 값을 출력
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("S: ");
  lcd.print(soil_moisture);
  lcd.print("% T: ");
  lcd.print(temperature);
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.print("H: ");
  lcd.print(humidity);
  lcd.print("% L:");
  lcd.print(light_intensity);
  lcd.print("C");

  delay(2000); // 2초 간격으로 값을 출력
}
