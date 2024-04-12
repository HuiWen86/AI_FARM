/*
 * light_sensor.c
 *
 * Created: 2024-04-12 pm 12:49:08
 *  Author: hyewon
 */ 

#include "light_sensor.h"

uint16_t read_light_sensor(void) {
	ADMUX = (1 << REFS0); // Select AVCC as reference voltage, select ADC1 channel
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Enable ADC and set prescaler to 128

	// Start ADC conversion
	ADMUX |= (1 << MUX0); // ADC1 channel selection
	ADCSRA |= (1 << ADSC);

	// Wait for conversion to complete
	while (ADCSRA & (1 << ADSC));

	return ADC;
}
