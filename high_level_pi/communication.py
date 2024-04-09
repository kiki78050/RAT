import serial 
from time import sleep
from values import *


#ich erwarte als Start Byte 0x00
#ich sende als Start Byte 0x01


def send_UART(value_1, value_2): #Als Value_1 und Value_2 werden Geschwindigkeit und Lenkwinkel übergeben

    send_buffer.append(start_send) #Start_byte welchen der XMC erwartet wird in Sende_buffer geschrieben 
    
    send_buffer.append(value_2) #Lenkwinkel wird in Sende_buffer geschrieben 
    send_buffer.append(value_1) #Geschwindigkeit wird in den Sende_buffer geschrieben 
    
    check_sum_create = send_buffer[1] ^ send_buffer[2] #Check_summe wird als ein XOR vergleich zwischen Lenkwinkel und Geschwindigkeit erstellt 

    send_buffer.append(check_sum_create)

    ser.write(send_buffer) #der Sende_buffer wird auf den Serial-Port geschrieben 
    
    send_buffer.clear() #Send_buffer wird geleert 
    
    ser.flush() #Serial-Port wird ebenfalls geleert 

    return

#Ohne Funktion
def get_UART():
    
    receive_buffer = ser.read()
    print("pass")    
    #sleep(1)
        
    data_left = ser.inWaiting()
        
    receive_buffer += ser.read(data_left)
        
    print(receive_buffer)
        
    if receive_buffer is not None: 
            
        check_sum_test = (receive_buffer[1] ^ receive_buffer[2] ^ receive_buffer[3])
            
        start_byte = receive_buffer[0] 
            
        if start_byte == 0x00:
            
            if receive_buffer[4] == check_sum_test:
                    
                get_geschwindigkeit = receive_buffer[1]
                get_ultraschllsensor = receive_buffer[2]
                get_infrarot = receive_buffer[3]
                    
                print(get_geschwindigkeit)
                print(get_ultraschllsensor)
                print(get_infrarot)
                    
            else: 
                ser.flush()
        else:
            ser.flush()
        
    print(f"get_v von xmc: {get_geschwindigkeit}")
    print(f"get_infrarot von XMC: {get_infrarot}")
    print(f"check_sum_test von XMC: {check_sum_test}")

    return 
