/*
 * infrarot.h
 *
 *  Created on: Dec 4, 2023
 *      Author: danie
 */

#ifndef INFRAROT_H_
#define INFRAROT_H_

void Infrarot_Init(void);
void IR_ADC_Wert_1ms (void);

extern float speed_in_cms, strecke_m, park_luecke_cm;
extern int park_luecke_genug;

#endif /* INFRAROT_H_ */
