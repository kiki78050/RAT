#------------------------------Geschwindigkeiten_und_Lenkwinkel-----------------------
v_stop = 127    ### Stop
v_crawl = 160  ### crawul: Parkplatz Suchen
v_slow = 193   ### Kurven: slow
v_mid = 200    ### Kurven: mid
v_fast = 205   ### Gerade: fast

v_in_char= 0
steering_in_char = 0
#--------------------------------------------------------------------------------------


#-------------------Für_Test_ohne_XMC--------------------------------------------------
get_geschwindigkeit = 0
get_ultraschallsensor = 0
#--------------------------------------------------------------------------------------

#-----------------------------Komunikation-------------------------------------------
send_buffer = bytearray()
receive_buffer = bytearray()


start_send = 0x01
start_get = 0x00

get_geschwindigkeit = 0
get_ultraschllsensor = 0
get_infrarot = 0


ser = serial.Serial ("/dev/ttyS0", 115200,timeout=1)
ser.flush()



#-------------------------------------------------------------------------------------

