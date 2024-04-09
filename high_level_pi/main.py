
from lines import get_lines    
from calculate import values_for_XMC
from communication import send_UART, get_UART





if __name__ == "__main__":

   
   while True:
    lenkwinkel = get_lines() #Lenkwinkel wird über get_lines Funktion in der lines.py File berechnet 

    steering_in_char, v_in_char = values_for_XMC(lenkwinkel) #Umrechnung der Werte über die calculation.py File
 

    send_UART(steering_in_char, v_in_char)      # (lenkwinkel, Geschwindigkeit)
    
 
    
    
    #get_UART()
    


    



   


  
