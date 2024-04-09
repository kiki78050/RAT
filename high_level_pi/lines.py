import cv2
import numpy as np
import math
# ~ import time
import matplotlib.pyplot as plt

from picamera2 import Picamera2, Preview
piCam = Picamera2()


#### geänderte Point A und B
Point_A = (272,400)
Point_B = (272,300)
size = 5



### Umwandlung nach schwarz und weiß
def canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0) #Filter wird angwendet um das geblured mit einer 5 mal 5 Matrix -macht es weiccher
    ##### geänderte Canny
    canny = cv2.Canny(blur, 150, 255) #Blur Funktion mit unterem und oberen Threshold 
    return canny
        
def region_of_interest(image): 
    ##### originale roi_point
    roi_points = np.array([[(340, 479), (482, 479), (482, 300), (340, 300)], [(80, 479), (180, 479), (230, 300), (80, 300)]])
    

             ####          |   unten rechts          |    oben rechts         |       unten links     |      oben links
                ######     |    UR-L, UR-R           |    OR-R, OR-L           |     UL-L, UL-R        |     OL-R, OL-L  
    mask = np.zeros_like(image) 
    ####   erstellt eine schwarze Maske, gleiche Anzahl von Pixeln
    cv2.fillPoly(mask, roi_points, 255) 
    ####   Das Dreieck wir mit dieser Funktion auf das Bild gelegt, die 255 macht das Dreieck weiß
    masked_image =cv2.bitwise_and(image, mask) 
 
    ####   macht einen Bitvergleich, pixel für pixel, dadurch wird alles was nicht in der region of intrest liegt raus gelöscht
    return masked_image



###  Bestimmung und Rückgabe der linke-seite oder recht-Seite Linien als array
###  Die Mittellinie liegt am den Punkt 300 an der (2d) x,y-Graph der "image"
### und Durchschnitt
def avarage_slope_intercept(image, lines):
    left_lines = [] # Leere Arrays, in denen die Linien dann gespeichert werden 
    right_lines = []

    if lines is not None:
        for line in lines:

            x1, y1, x2, y2 = line.reshape(4) #Linien werden in (x1/y1) und (x2/y2) aufgeteilt 

            if x1 < 272:  #ob rechte oder linke Linie entscheidet sich nach dem X1 Wert 
                left_lines.append([x1, y1, x2, y2])
                
            else:
                right_lines.append([x1, y1, x2, y2])

    else:
        print("Keine Linien gefunden")


    left_lines = np.array(left_lines)
    right_lines = np.array(right_lines)

    #Berechnung der anderen Linie falls rechts oder links keine Linie gefunden wird 
    if len(left_lines) == 0:
        right_lines_average = np.mean(right_lines,axis =0)
        left_lines_average = right_lines_average - np.array([272,0,272,0])
    elif len(right_lines) == 0:
        left_lines_average = np.mean(left_lines,axis=0)
        right_lines_average = left_lines_average + np.array([272,0,272,0])
    else:
        left_lines_average = np.mean(left_lines,axis=0)
        right_lines_average = np.mean(right_lines,axis=0)

    return left_lines_average, right_lines_average


###  Die Berechnung der passenden Winkel durch Hypotenuse
###  Wenn X3 größer als X1 ist,  ist es der lenkwinkel nach links
###  Wenn X3 kleiner als X1 ist, ist Lenkwinkel nach rechts
###  (x1,y1) entspricht eine Mittellinie von Image
def get_lenkwinkel(A, B, C):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    line_length_GK = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
    line_length_HY = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)

    if x3 > x1:
        left_turn_angle = -int(math.degrees(math.asin(line_length_GK / line_length_HY)))
        return left_turn_angle
    elif x1 > x3:
        right_turn_angle = int(math.degrees(math.asin(line_length_GK / line_length_HY)))
        return right_turn_angle
    elif x1 == x3:
        return 0

### Zeichnung der Mittellinie und die Linien für die passende Winkel
def draw_points(x_left, x_right, frame):
    x = ((x_right + x_left) / 2)
    C = (int(x) , 400 )
    # ~ print(C)
    cv2.circle(frame, C, size, (0, 0, 255), -1)
    cv2.circle(frame, Point_A, size, (0, 255, 0), -1)
    cv2.circle(frame, Point_B, size, (0, 255, 0), -1)
    cv2.line(frame, Point_A, Point_B, (0, 255, 0), 2)
    cv2.line(frame, Point_B, C, (0, 255, 0), 2)
    cv2.line(frame, C, Point_A, (0, 255, 0), 2)
    # plt.imshow(frame)
    # plt.show()
    return C


# ~ # ###    Kamera_Initialisierung: Auflösung von (640x480), Bildformat: (RGB888)
def InitKamera():                                       
    piCam.preview_configuration.main.size=(640,480)         
    piCam.preview_configuration.main.format = "RGB888"
    piCam.preview_configuration.align()
    piCam.configure("preview")
    piCam.start()
    return 0

###    Bildaufnahme als Array
def getImg():
    
    frame = piCam.capture_array()       ## haupt programm
    
    return frame




InitKamera()



def get_lines():
    
    
    
        
    
    while True:
        
        frame = getImg()
      
     
        
        
     

    #Umformen des frames in die Bird-view Perpektive, die arrays sind durch probieren entstanden 
        pts1 = np.float32([[0,250],[0,330],[639,250],[639,330]])
        pts2 = np.float32([[0,0],[0,480],[640,0],[640,480]])
        ###    [[tl],[bl],[tr],[br]]

        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        transformed_frame = cv2.warpPerspective(frame,matrix,(640,480))
      
        warp_cany_image = canny(transformed_frame) #Canny Funktion wird angewendet 
 
        warp_cany_image_region = region_of_interest(warp_cany_image) #region of intrest wird angewendet 
    

   
        # plt.imshow(cropped_image)
        # plt.show()

        #cv2.imshow("wwarp ",warp_cany_image_region)
      #Der Hough-Algorythmus hilft dabei, über bestimmte Parameter Linien zu finden 
        lines = cv2.HoughLinesP(warp_cany_image_region, 1, np.pi/180, 50, np.array([]), minLineLength=10, maxLineGap=2)
      
        left_lines, right_lines = avarage_slope_intercept(warp_cany_image_region, lines) #Linien werden nach rechts oder links aufgeteit 
       
     

        
    #Es wird der durchschnittliche X-Wert für links und rechts erstellt 
        average_x_left = np.mean(left_lines [0::2])
        average_x_right = np.mean(right_lines [0::2])



        if left_lines is not None:
            Point_C = draw_points(average_x_left, average_x_right, frame ) # der Punkt welcher den Mittelpunkt zwischen den Linien definiert wird ermittelt 

        else:
            print("No_Line ")

        lenkwinkel = get_lenkwinkel(Point_A, Point_B, Point_C) #berechnung des Lenkwinkels 
        print(" ")
        print("Lenkwinkel in Grad ", lenkwinkel )
        print(" ")

        cv2.imshow("frame",frame)

        #cv2.imshow("result", cropped_image)
        cv2.imshow("result", warp_cany_image_region) 
        cv2.waitKey(30) 


        return lenkwinkel
            
           
    

# if __name__ == "__main__":
#     main()
