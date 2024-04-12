/*
 * autolmp.h
 *
 * Created: 2024-04-12 pm 7:38:31
 *  Author: hyewon
 */ 


#ifndef AUTOLMP_H_
#define AUTOLMP_H_
#include <avr/io.h>

#include "motor.h"
#include "pump.h"
#include "light_sensor.h"
#include "dht.h"
#include "soil_moisture.h"

void perform_hourly_automation(uint16_t light_sensor_value, uint8_t humidity, uint8_t temperature, uint16_t soil_moisture);

#endif /* AUTOLMP_H_ */