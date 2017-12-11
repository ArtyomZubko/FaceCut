import sys, time, cv2 as cv, numpy as np
import threading
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',57600)

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

servpos = 90
servo_step = 1
err = 10
face_middlex = 0
cap = cv.VideoCapture(1)

if not cap.isOpened() :
    print("no")

ser.write(chr(servpos).encode('ascii'))

def printPos():
    while True:
        #print(servpos)
        ser.write(chr(servpos).encode('ascii'))
                
t1 = threading.Thread(target=printPos, args=())
t1.daemon = True
t1.start()

while True:
    ok, img = cap.read()
    
    height, width, channels = img.shape 
    img_centerx = width / 2
 
    if not ok: 
        break 
 
    faces = face_cascade.detectMultiScale(img, 1.3, 8)
    
    for (x,y,w,h) in faces:
        face_middlex = x + w/2
        k = int(np.abs(img_centerx - x)*0.009)
        if len(faces) != 0:                 
            if face_middlex > (img_centerx - err):
                if servpos >=5 and (servpos - (servo_step + k)) > 0 :
                    servpos -= servo_step + k
            
            elif face_middlex < (img_centerx + err):
                if servpos <=125 and (servpos + (servo_step + k)) < 127:
                    servpos += servo_step + k
        
        cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        print(str(servpos)+"\t" + str(x))         
        
    cv.imshow("test", img)    
    cv.waitKey(1)
