/*
 * usart.h
 *
 * Created: 2024-04-12 pm 2:16:01
 *  Author: hyewon
 */ 


#ifndef USART_H_
#define USART_H_

#include <avr/io.h>

#define BAUDRATE 9600
#define UBRR_VALUE ((F_CPU / (BAUDRATE * 16UL)) - 1)

void USART_Init(unsigned int ubrr);
void USART_Transmit(unsigned char data);
void USART_Transmit_String(const char *str);

#endif /* USART_H_ */