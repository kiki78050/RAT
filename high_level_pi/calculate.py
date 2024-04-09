import math
from values import *



#ohne Funktion 
   
def control_radar (radar):

    if int(radar) > 10:
        pass

    else:
        v_to_XMC = v_slow

        if int(radar) <= 5:
             v_to_XMC = v_stop

    return v_to_XMC


def values_for_XMC(lenkwinkel): #für Umrechnung bitte auch die angehängte Exeltabelle angucken

    normalisierter_lenkwinkel = lenkwinkel + 24 #Offset von 24, um negative Winkel zu vermeiden
    lw_betrag = int(normalisierter_lenkwinkel/50 * 240) +12 #umrechnung in einen Char-Wert, siehe Exeltabelle

    #Bestimmung der Geschwindigkeit, abhängig vom Betrag des Lenkwinkels 

    if lw_betrag > 103 and lw_betrag < 152:
        v_to_XMC = v_fast

    elif (lw_betrag >= 55 and lw_betrag <= 103) or (lw_betrag >= 152 and lw_betrag <= 200) :
        v_to_XMC = v_mid

    elif lw_betrag < 55 or lw_betrag > 200:
         v_to_XMC = v_slow


#Vorkehrung, dass der Wert nicht kleiner als 12 oder größer als 255 wird, damit kann der XMC nichts anfangen
    if lw_betrag < 12:
        lw_betrag =12
    elif lw_betrag >252:
        lw_betrag = 252
        
 

    lw_to_XMC = lw_betrag

#Zum testen 
    #print("lw_betrag = ", lw_to_XMC)
    #print("lw_geschwindigkeit = ", v_to_XMC)
    return lw_to_XMC, v_to_XMC





  
