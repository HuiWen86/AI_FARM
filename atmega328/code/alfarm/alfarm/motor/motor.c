/*
 * CFile1.c
 *
 * Created: 2024-04-12 오전 11:12:45
 *  Author: hyewon
 */ 

#include "motor.h"


void motor_init(void) {
	MOTOR_DDR |= (1 << MOTOR_PIN1) | (1 << MOTOR_PIN2);
}

void motor_on(void) {
	MOTOR_PORT |= (1 << MOTOR_PIN1);  // PB0 HIGH
	MOTOR_PORT &= ~(1 << MOTOR_PIN2); // PB1 LOW,
}

void motor_off(void) {
	MOTOR_PORT &= ~(1 << MOTOR_PIN1);  // PB0 LOW
	MOTOR_PORT &= ~(1 << MOTOR_PIN2);  // PB1 LOW
}
