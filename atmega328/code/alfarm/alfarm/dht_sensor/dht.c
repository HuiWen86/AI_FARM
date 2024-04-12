/*
 * dht.c
 *
 * Created: 2024-04-12 pm 1:43:24
 *  Author: 2
 */ 

#include <util/delay.h>
#include "dht.h"


void dht_send_start_signal(void) {
	DDRD |= (1 << PD3); // Change to output mode
	PORTD &= ~(1 << PD3); // Set to LOW
	_delay_ms(20); // Minimum 18ms wait
}

void dht_read_response(void) {
	DDRD &= ~(1 << PD3); // Change to input mode
	_delay_us(40);

	// Check response from sensor
	while (PIND & (1 << PD3)); // Wait while LOW
	while (!(PIND & (1 << PD3))); // Wait for as long as HIGH
	while (PIND & (1 << PD3)); // Wait while LOW
}

uint8_t dht_read_byte(void) {
	uint8_t data = 0;

	for (int i = 0; i < 8; i++) {
		while (!(PIND & (1 << PD3))); // Wait while held HIGH
		_delay_us(30); // Wait 30us and check if it remains HIGH
		if (PIND & (1 << PD3)) // If held HIGH, set bit to 1
		data |= (1 << (7 - i));
		while (PIND & (1 << PD3)); // Wait while LOW
	}

	return data;
}

void dht_read_data(uint8_t *humidity, uint8_t *temperature) {
	uint8_t data[5];

	// Sends a start signal
	dht_send_start_signal();

	// Check the response
	dht_read_response();

	// Receives data
	for (int i = 0; i < 5; i++) {
		data[i] = dht_read_byte();
	}

	// Validate
	if (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)) {
		*humidity = data[0];
		*temperature = data[2];
	}
}