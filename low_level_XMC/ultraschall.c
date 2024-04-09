/*
 * ultraschall.c
 *
 *  Created on: Dec 4, 2023
 *      Author: danie
 */

#include "DAVE.h"                 //Declarations from DAVE Code Generation (includes SFR declaration)
#include "ultraschall.h"
#include <stdio.h>

#define Durchlauf 60000U

uint8_t Abstand [12];
uint32_t Timer_60ms;
uint32_t Capture_t;

float captured_time_us;
float distance;

void Get_Captured_Time_60ms(void)
{
	PWM_Start(&PWM_ULTRA);
	CAPTURE_GetCapturedTimeInNanoSec(&CAPTURE_ULTRA, &Capture_t);
	captured_time_us = ((float)Capture_t)/1000;
	distance = captured_time_us /58;
	//sprintf((char*)Abstand,"%.2fcm\n\r", distance);
	//UART_Transmit(&UART_PROTOKOLL, Abstand, sizeof(Abstand));
}

void Ultraschall_Init(void)
{
	Timer_60ms = SYSTIMER_CreateTimer(Durchlauf,SYSTIMER_MODE_PERIODIC,(void*)Get_Captured_Time_60ms,NULL);
	SYSTIMER_StartTimer(Timer_60ms);
}
