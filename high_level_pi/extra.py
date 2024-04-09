import serial
from time import sleep
from calculate import values_for_XMC
#ich erwarte als Start Byte 0x00
#ich sende als Start Byte 0x01

get_geschwindigkeit = 0
get_ultraschllsensor = 0
get_infrarot = 0
senden = True
receive_buffer = bytearray()

#Um zu Testen
give_geschwindigkeit = 12
give_lenkwinkel = 122
            

send_buffer = bytearray()
start_send = 0x01



ser = serial.Serial ("/dev/ttyS0", 115200)
ser.flush()

while True:
    
    while senden == False:
        
        receive_buffer = ser.read()
        
        sleep(1)
        
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
            
         
         
        senden = True

    while senden == True:
        lenkwinkel = 25
    
        steering_in_char, v_in_char = values_for_XMC(lenkwinkel)
        send_buffer.append(start_send)
        send_buffer.append(v_in_char)
        send_buffer.append(steering_in_char)
        
        check_sum_create = (send_buffer[1] ^ send_buffer[2])
        
        send_buffer.append(check_sum_create)
        
        ser.write(send_buffer)
        sleep(0.02)
        
        
        
        print('done')
        print(send_buffer)
        
        send_buffer.clear() 
        
        senden = False
                    
ser.close()
