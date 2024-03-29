#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#define led_pin1 13



int main(void)
{
	//DDRB 전체 선택
	DDRB = 0xFF;
	
	while (1)
	{
		PORTB = 0xFF; // PB0~PB5 어디에 연결해도 LED 출력됨. 
		_delay_ms(1000); // 1초간 대기 --> 여기서 실제로 1초인지 확인해야함. 
						//딜레이 시간을 바꿔가며 실제 시간과 맞는지 확인, 안맞을 경우 퓨즈 확인
		PORTB = 0x00; // PB0~PB5 모두 끔
		_delay_ms(500); // 1초간 대기
	}
	
	return 0;
}


