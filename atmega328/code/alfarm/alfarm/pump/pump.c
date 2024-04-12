/*
 * pump.c
 * This is a water pump function.
 * Created: 2024-04-12 오후 12:10:08
 *  Author: 2
 */ 

#include "pump.h"

void pump_init() {
	PUMP_DDRB |= (1 << PUMP_PINB); // Set PUMP_PINB as output
	PUMP_DDRD |= (1 << PUMP_PIND); // Set PUMP_PIND as output
}

void pump_on() {
	PUMP_PORTB |= (1 << PUMP_PINB); // Set PUMP_PINB high
	PUMP_PORTD |= (1 << PUMP_PIND); // Set PUMP_PIND high
}

void pump_off() {
	PUMP_PORTB &= ~(1 << PUMP_PINB); // Set PUMP_PINB low
	PUMP_PORTD &= ~(1 << PUMP_PIND); // Set PUMP_PIND low
}