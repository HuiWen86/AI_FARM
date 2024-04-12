/*
 * soil_moisture.c
 *
 * Created: 2024-04-12 pm 1:25:41
 *  Author: hyewon
 */ 

#include "soil_moisture.h"

uint16_t read_soil_moisture(void) {
	ADMUX = (1 << REFS0); // Select AVCC as reference voltage, select ADC0 channel
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Enable ADC and set prescaler to 128

	// Start ADC conversion
	ADMUX &= ~((1 << MUX0) | (1 << MUX1)); // ADC0 channel selection
	ADCSRA |= (1 << ADSC);

	// Wait for conversion to complete
	while (ADCSRA & (1 << ADSC));

	return ADC;
}
