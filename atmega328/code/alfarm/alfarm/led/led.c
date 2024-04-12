/*
 * led.c
 *
 * Created: 2024-04-12 pm 12:24:20
 *  Author: hyewon
 */ 
#include "led.h"



void light_init() {
	DDRB |= (1 << LIGHT_PIN); // Set LIGHT_PIN as output
}

void light_on() {
	PORTB |= (1 << LIGHT_PIN); // Turn on LED connected to LIGHT_PIN
}

void light_off() {
	PORTB &= ~(1 << LIGHT_PIN); // Turn off LED connected to LIGHT_PIN
}