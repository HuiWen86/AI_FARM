/*
 * usart.c
 * //Serial communication settings
 * Created: 2024-04-12 pm 2:16:22
 *  Author: hyewon
 */ 

#include <avr/io.h>



void USART_Init(unsigned int ubrr){
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;
	UCSR0B = (1 << TXEN0) | (1 << RXEN0); // Enable sending and receiving
	UCSR0C = (3 << UCSZ00); // Data bits: 8 bits
}

void USART_Transmit(unsigned char data) {
	while (!(UCSR0A & (1 << UDRE0))); // Waiting for transmission
	UDR0 = data; // data transfer
}

void USART_Transmit_String(const char *str) {
	while (*str) {
		USART_Transmit(*str++);
	}
}