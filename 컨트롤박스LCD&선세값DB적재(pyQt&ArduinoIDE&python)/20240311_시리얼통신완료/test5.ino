#include <Wire.h>
#include <DHT.h>

#define DHTPIN 2            // DHT11 센서 핀
#define DHTTYPE DHT11       // DHT 센서 타입
#define SOIL_MOISTURE_PIN A0 // 토양 수분 센서 핀
#define LIGHT_SENSOR_PIN A1 // 조도 센서 핀
#define LED_PIN1 13         // LED 핀
#define LED_PIN2 12
#define LED_PIN3 11

DHT dht(DHTPIN, DHTTYPE);

void setup() 
{ 
  Serial.begin(115200);

  pinMode(LED_PIN1, OUTPUT); 
  pinMode(LED_PIN2, OUTPUT);
  pinMode(LED_PIN3, OUTPUT);

  dht.begin();  
}

void loop() {
  
  // 온습도 센서 값 읽기
  //float humidity = dht.readHumidity();
  //float temperature = dht.readTemperature();

  // 토양 수분 센서 값 읽기
  //int soil_moisture = analogRead(SOIL_MOISTURE_PIN);

  // 조도 센서 값 읽기
  //int light_intensity = analogRead(LIGHT_SENSOR_PIN);

  // 시리얼 통신으로 모드 변경 확인
  if (Serial.available()) {
    char receivedChar = Serial.read();
    Serial.println(receivedChar);
    if (receivedChar == 'A') {
      Serial.println("A");
      // 자동 모드에서 LED 제어 코드 추가
      // ...
    } else if (receivedChar == 'M') {
      Serial.println("M");
      // 수동 모드에서 LED 제어 코드 추가
      // ...
    } else if (receivedChar == 'B') {
      char buttonChar = Serial.read(); // 버튼 이름을 읽음
      char statusChar = Serial.read(); // 버튼 상태를 읽음

      // 버튼 상태에 따라 LED 제어
      int buttonPin = -1;
    if (buttonChar == '1') {
        buttonPin = LED_PIN1;
      } else if (buttonChar == '2') {
        buttonPin = LED_PIN2;
      } else if (buttonChar == '3') {
        buttonPin = LED_PIN3;
      }

      if (statusChar == 'N') {
        digitalWrite(buttonPin, HIGH); // LED ON
      } else if (statusChar == 'F') {
        digitalWrite(buttonPin, LOW); // LED OFF
      }
    }
  }

  //delay(2000); // 2초 간격으로 값을 출력
}
