#define F_CPU 16000000L

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>

#include "motor.h" //Load fan motor control header file
#include "pump.h" //Load water pump control header file
#include "led.h" //Load led control header file
#include "light_sensor.h" //Load cds sensor header file
#include "soil_moisture.h"//Load soil sensor header file
#include "dht.h" //Load dht sensor header file
#include "usart.h" //Load usart header file
#include "autolmp.h" //Load automatin_fan_water pump_led header file

int main(void) {
	USART_Init(UBRR_VALUE); // Serial communication initialization
	motor_init();
	pump_init();
	light_init();
	
	while (1) {

		if (UCSR0A & (1 << RXC0)) { // If data is received
			char receivedData = UDR0;
			USART_Transmit(receivedData);
			switch (receivedData) {
				case '1':
				motor_on();
				break;
				case '2':
				motor_off();
				break;
				case '3':
				pump_on();
				break;
				case '4':
				pump_off();
				break;
				case '5':
				light_on();
				break;
				case '6':
				light_off();
				break;
				default:
				// Invalid command, do nothing
				break;
			}
		}
		
		// read dht(hum, temp) 
		uint8_t humidity, temperature;
		dht_read_data(&humidity, &temperature);

		// read soil sensor
		uint16_t soil_moisture = read_soil_moisture();

		// read cds
		uint16_t light_sensor_value = read_light_sensor();

		// print sensor data : temperature, humidity, soil_moisture, light_sensor
		char output[50];
		sprintf(output, "T:%d H:%d S:%d L:%d\n", temperature, humidity, soil_moisture, light_sensor_value);
		USART_Transmit_String(output);

		_delay_ms(1000); // 1 second delay
		
		perform_hourly_automation(light_sensor_value,humidity,temperature,soil_moisture);

	}
	
	
	return 0;
}
