/*
 * motor.h
 *
 * Created: 2024-04-12 오전 10:55:29
 *  Author: hyewon
 */ 

#ifndef MOTOR_H_
#define MOTOR_H_

#include <avr/io.h>

#define MOTOR_DDR DDRB
#define MOTOR_PORT PORTB
#define MOTOR_PIN1 PB1
#define MOTOR_PIN2 PB0

void motor_init(void);
void motor_on(void);
void motor_off(void);

#endif /* MOTOR_H_ */
