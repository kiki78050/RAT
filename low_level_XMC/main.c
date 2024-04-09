#include "DAVE.h"
#include "ultraschall.h"
#include "infrarot.h"
#include "global.h"
#define ONESEC 1000000U										//Watchdog Timer
#define TENMILSEC 10000U									//Regelung jede 10ms
#define HALFSEC 500000U



uint32_t Timer_WD, Timer_Regelung, Timer_BUTTON;			//Timers

uint8_t string[100] = "test";

int zaehlimpulse = 0;										//Zaehlimpulse Lichtschranke


#define impulse_einer_umdrehung 60							//Eine Umdrehung = 60 Impulse
float speed_in_cms = 0;										//V(ist) in cm/s
#define u_rad_cm 20.42										//Radumdrehung
const float faktor = u_rad_cm/impulse_einer_umdrehung;		//Fester Faktor für die Umrechnung der Geschwindigkeit

uint8_t recieved[4]= {0,0,0,0}; 							//Recieved UART ARRAY [startbit, geschwindigkeit, lenkwinkel, checksumme]

uint8_t startbit = 0;										//Startbit 0x01 (Pi auf Xmc)
uint8_t fahr_geschwindigkeit_char = 0;						//Selektierte Geschwindigkeit 127=Leerlauf; 0 = Rückwärts; 255 = Vorwärts
uint8_t lenk_winkel;									//Selektierter Lenkwinkel 127=Geradeaus; 0=Rechts; 255=Links
uint8_t checksumme = 0;										//Checksumme Geschwindigkeit ^ Lenkwinkel (XOR)

float soll_fahr_geschwindigkeit = 0;						//V(soll) in cm/s

float strecke_cm = 0;										//Zurückgelegte Strecke

float abweichung = 0;										//V(soll) - v(ist)
float speed_nach_regler= 0;									//V(geregelt)

int pwm_lenkung_leerlauf = 870;								//Leerlauf PWM (Lenkung)
int pwm_motor_leerlauf = 870;								//Leerlauf PWM (Motor)
int pwm;													//PWM (nach dem Regler)

int reglerOutput = 0;										//Regler Ausgang
int Kp = 0.5;												//Regler P faktor

int check=0;												//Variable für den Testknopf


uint8_t fahr_infos[1] = {0};						//Fahrinfos für den Raspi




void watch_dog(void){
	//Falls nach 1s kein Inputbefehl gibt, wird alles in Leerlauf gesetzt
	PWM_SetDutyCycle(&PWM_LENKUNG, pwm_lenkung_leerlauf);
	soll_fahr_geschwindigkeit = 0;
	SYSTIMER_StopTimer(Timer_WD);
}

int regelung(){
	//DIGITAL_IO_ToggleOutput(&LED_TEST);
	abweichung = soll_fahr_geschwindigkeit - speed_in_cms;		// e
	speed_nach_regler = abweichung * 0.5;  						// e * Kp (geregelte Geschwindigkeit)
	pwm = (speed_nach_regler*0.24)+895.4;						// pwm wird neu gesetzt
	PWM_SetDutyCycle(&PWM_MOTOR, pwm);
}

void set_speed(int speed_char){
	//die Umrechung von speed_char in cm/s
	if(speed_char<155){
		soll_fahr_geschwindigkeit = 0;							//Schwellwert
	}else{
		soll_fahr_geschwindigkeit = (6.92*speed_char)-982;		//Rechnung fuer die Soll Geschwindigkeit
	}

}

void pwm_set_lenkung(int winkel){

	int pwm = (winkel*1.3)+700;									//Pwm der Lenkung gesetzt
	PWM_SetDutyCycle(&PWM_LENKUNG, pwm);

}

void impulse_lichtschranke(void){
	zaehlimpulse++;												//Impulse hochzaehlen

}


void Geschwindigkeit(void){
	speed_in_cms = (float)zaehlimpulse*faktor*2; 				//passiert jede 500ms
																//Multiplikation mit 2 ist gleich Division durch 0.5s
																//Zaehlimpulse* Faktor ist gleich die zuruckgelegte Strecke in der Zeit
	strecke_cm = strecke_cm + (speed_in_cms*0.5);				//Zurückgelegte Strecke
	zaehlimpulse = 0;

}


int main(void)
{
  DAVE_STATUS_t status;
  status = DAVE_Init();           /* Initialization of DAVE APPs  */
  Ultraschall_Init();
  Infrarot_Init();
  if (status != DAVE_STATUS_SUCCESS)
  {
    XMC_DEBUG("DAVE APPs initialization failed\n");
    while(1U)
    {


    }
  }

  Timer_WD = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)watch_dog,NULL);			//Watchdog timer
  Timer_Regelung = (uint32_t)SYSTIMER_CreateTimer(TENMILSEC,SYSTIMER_MODE_PERIODIC,(void*)regelung,NULL);	//Regelung timer
  SYSTIMER_StartTimer(Timer_Regelung);

  //DIGITAL_IO_ToggleOutput(&LED_TEST);


  while(1U)
  {

	  if(UART_Receive(&UART_PROTOKOLL,&recieved, 4) == UART_STATUS_SUCCESS)
	         {

		  	  	  startbit = recieved[0];							//0. Byte enthält den Startbit
		  	  	  if(startbit == 0x01){
		  	  		fahr_geschwindigkeit_char = recieved[1]; 		//1.Byte beinhaltet Fahrgeschwindigkeit
		  	  		lenk_winkel = recieved[2];						//2.Byte beinhaltet Lenkwinkel
		  	  		checksumme = recieved[3];						//Checksumme (1. XOR 2.)
		  	  		if(checksumme == (fahr_geschwindigkeit_char ^ lenk_winkel)){
		  	  			//Aktoren gesetzt
		  	  			if(distance>=20){							//Falls kein Hindernis sich 20m vor dem Auto befindet:
		  	  				set_speed(fahr_geschwindigkeit_char);	//Soll geschwindigkeit gesetzt
		  	  				pwm_set_lenkung(lenk_winkel);			//PWM Dutycycle für den Lenkwinkel wird gesetzt
		  	  			}else{
		  	  				set_speed(pwm_motor_leerlauf);			//Falls es nicht stimmt dann sollte das Auto stehenbleiben
		  	  				pwm_set_lenkung(lenk_winkel);
		  	  			}

		  	  			SYSTIMER_RestartTimer(Timer_WD,ONESEC);		//watchdog timer neugestartet

		  	  		}else{
		  	  				  	  			recieved[0] = 0;		//Falls die Übertragung fehlerhaft ist, wird die Nachricht gelöscht
		  	  				  	  			recieved[1] = 0;		//und der Wachhund greift an
		  	  				  	  			recieved[2] = 0;
		  	  				  	  			recieved[3] = 0;
		  	  		}
		  	  	  }

	         }

  }
}
