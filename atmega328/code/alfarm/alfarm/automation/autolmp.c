/*
 * autolmp.c
 *
 * Created: 2024-04-12 pm 7:38:42
 *  Author: hyewon
 */ 


#include "autolmp.h"

void perform_hourly_automation(uint16_t light_sensor_value, uint8_t humidity, uint8_t temperature, uint16_t soil_moisture) {
	if (light_sensor_value > 70 && humidity > 75 && temperature > 27 && soil_moisture > 85) {
		light_off();
		motor_on();
		pump_off();
		} else if (light_sensor_value > 70 && humidity > 75 && temperature > 27 && soil_moisture < 75) {
		light_off();
		motor_on();
		pump_on();
		} else if (light_sensor_value > 70 && humidity > 75 && temperature < 18 && soil_moisture > 85) {
		light_on();
		motor_off();
		pump_off();
		} else if (light_sensor_value > 70 && humidity > 75 && temperature < 18 && soil_moisture < 75) {
		light_on();
		motor_on();
		pump_on();
		} else if (light_sensor_value > 70 && humidity < 65 && temperature > 27 && soil_moisture > 85) {
		light_off();
		motor_on();
		pump_off();
		} else if (light_sensor_value > 70 && humidity < 65 && temperature > 27 && soil_moisture < 75) {
		light_off();
		motor_on();
		pump_on();
		} else if (light_sensor_value > 70 && humidity < 65 && temperature < 18 && soil_moisture > 85) {
		light_off();
		motor_on();
		pump_off();
		} else if (light_sensor_value > 70 && humidity < 65 && temperature < 18 && soil_moisture < 75) {
		light_off();
		motor_off();
		pump_on();
		} else if (light_sensor_value < 30 && humidity > 75 && temperature > 27 && soil_moisture > 85) {
		light_on();
		motor_on();
		pump_off();
		} else if (light_sensor_value < 30 && humidity > 75 && temperature > 27 && soil_moisture < 75) {
		light_on();
		motor_on();
		pump_on();
		} else if (light_sensor_value < 30 && humidity > 75 && temperature < 18 && soil_moisture > 85) {
		light_on();
		motor_on();
		pump_off();
		} else if (light_sensor_value < 30 && humidity > 75 && temperature < 18 && soil_moisture < 75) {
		light_on();
		motor_off();
		pump_on();
		} else if (light_sensor_value < 30 && humidity < 65 && temperature > 27 && soil_moisture > 85) {
		light_on();
		motor_on();
		pump_off();
		} else if (light_sensor_value < 30 && humidity < 65 && temperature > 27 && soil_moisture < 75) {
		light_on();
		motor_off();
		pump_on();
		} else if (light_sensor_value < 30 && humidity < 65 && temperature < 18 && soil_moisture > 85) {
		light_on();
		motor_off();
		pump_off();
		} else if (light_sensor_value < 30 && humidity < 65 && temperature < 18 && soil_moisture < 75) {
		light_on();
		motor_off();
		pump_on();
	}
}

