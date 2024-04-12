/*
 * pump.h
 * This is a water pump function.
 * Created: 2024-04-12 pm 12:09:55
 *  Author: hyewon
 */ 


#ifndef PUMP_H_
#define PUMP_H_

#include <avr/io.h>

#define PUMP_DDRB DDRB
#define PUMP_PINB PB2
#define PUMP_DDRD DDRD
#define PUMP_PIND PD6
#define PUMP_PORTB PORTB
#define PUMP_PORTD PORTD

void pump_init(void);
void pump_on(void);
void pump_off(void);

#endif /* PUMP_H_ */
