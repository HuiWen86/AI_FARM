/*
 * led.h
 *
 * Created: 2024-04-12 pm 12:24:08
 *  Author: hyewon
 */ 


#ifndef LED_H_
#define LED_H_
#include <avr/io.h>

#define LIGHT_PIN PB3

void light_init(void);
void light_on(void);
void light_off(void);

#endif /* LED_H_ */