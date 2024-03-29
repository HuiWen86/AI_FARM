/*
 * GccApplication_print_hello.cpp
 *
 * Created: 2024-03-28 오후 2:13:54
 * Author : 2
 */ 

#include <avr/io.h>
#include <util/delay.h>

#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUD_RATE * 16UL))) - 1)

// LED를 제어하기 위한 매크로 및 함수 정의
#define LED_PORT PORTB
#define LED_DDR DDRB
#define LED_PIN 0

void init_LED() {
	// LED 핀을 출력으로 설정
	LED_DDR |= (1 << LED_PIN);
}

void toggle_LED() {
	// LED 핀의 상태를 토글
	LED_PORT ^= (1 << LED_PIN);
}

// UART 통신을 위한 함수 정의
void init_UART() {
	// 보오레이트 레지스터 설정
	UBRR0H = (unsigned char)(BAUD_PRESCALLER >> 8);
	UBRR0L = (unsigned char)BAUD_PRESCALLER;
	// 송수신 활성화
	UCSR0B = (1 << RXEN0) | (1 << TXEN0);
	// 데이터 비트: 8비트, 패리티 비트: 없음, 정지 비트: 1비트
	UCSR0C = (3 << UCSZ00);
}

void transmit_message(const char *message) {
	// 문자열 전송
	while (*message) {
		// 전송이 완료될 때까지 대기
		while (!(UCSR0A & (1 << UDRE0)));
		// 데이터 전송
		UDR0 = *message++;
	}
}

int main(void) {
	// LED 및 UART 초기화
	init_LED();
	init_UART();

	// 무한 루프
	while (1) {
		// LED 깜빡이기
		toggle_LED();
		_delay_ms(1000);

		// UART를 통해 메시지 전송
		transmit_message("hi hello fine thank you!\r\n");
		_delay_ms(1000);
	}

	return 0;
}
