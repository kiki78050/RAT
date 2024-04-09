/*
 * infrarot.c
 *
 *  Created on: Dec 4, 2023
 *      Author: danie
 */

#include "DAVE.h"
#include "infrarot.h"
#include <stdio.h>
#include "global.h"
#define PERIODIC_READ 10000U

uint8_t IR_ADC[100];
uint8_t Luecke[100];
uint32_t Timer_IR;

uint32_t previous_ADC = 0;

float elapsed_time;
float time_in_s;

int check_start = 0;
int turn = 0;

extern float park_luecke_cm = 0;
extern int park_luecke_genug = 0;
extern float speed_in_cms, strecke_cm;

int min_parkluecke_laenge_cm = 70;

float parkluecke = 0;

XMC_VADC_RESULT_SIZE_t IR_ADC_Wert;

void IR_ADC_Wert_1ms (void)
{
	IR_ADC_Wert = ADC_MEASUREMENT_GetResult(&ADC_MEASUREMENT_Channel_A);


	if (previous_ADC >= 1000 && IR_ADC_Wert <= 1000)
		  {
			  check_start++;
			  DIGITAL_IO_ToggleOutput(&LED_TEST);
			  parkluecke = strecke_cm;
		  }
		  if (previous_ADC <= 1000 && IR_ADC_Wert >= 1000 && check_start == 1)
		  {
			  check_start = 0;



			  if (turn % 2 == 0)
			  {

				  parkluecke = strecke_cm - parkluecke;
				  if(parkluecke >= min_parkluecke_laenge_cm){
					  park_luecke_genug = 1;
				  }

//				  sprintf(Luecke, "\f Abstand: %.2fcm | Strecke : %.2fcm\n\r",parkluecke,strecke_cm);
//				  UART_Transmit(&UART_PROTOKOLL, Luecke, sizeof(Luecke));


			  }

			  turn++;

			  if (turn >= 10) {
		       turn = 0;
			  }



		   }

		  previous_ADC=IR_ADC_Wert;
}

void Infrarot_Init(void)
{
	Timer_IR = SYSTIMER_CreateTimer(PERIODIC_READ,SYSTIMER_MODE_PERIODIC,(void*)IR_ADC_Wert_1ms,NULL);
	SYSTIMER_StartTimer(Timer_IR);
}
