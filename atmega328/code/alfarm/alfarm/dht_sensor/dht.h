/*
 * dht.h
 *
 * Created: 2024-04-12 pm 1:43:13
 *  Author: 2
 */ 

#ifndef DHT_H_
#define DHT_H_

#include <avr/io.h>
#define PD3 3



void dht_send_start_signal(void);
void dht_read_response(void);
uint8_t dht_read_byte(void);
void dht_read_data(uint8_t *humidity, uint8_t *temperature);

#endif /* DHT_H_ */