/*
 * soil_moisture.h
 *
 * Created: 2024-04-12 pm 1:25:28
 *  Author: hyewon
 */ 


#ifndef SOIL_MOISTURE_H_
#define SOIL_MOISTURE_H_

#include <avr/io.h>
#define PC0 0

uint16_t read_soil_moisture(void);

#endif /* SOIL_MOISTURE_H_ */