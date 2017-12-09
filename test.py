import sys, time, cv2 as cv, numpy as np
import threading
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',115200)

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

filename = 0

servpos = 90
xrecount = 0
prevx = 0
cap = cv.VideoCapture(1)

if not cap.isOpened() :
    print("no")

ser.write(chr(servpos).encode('ascii'))

def printPos():
    while True:
        ser.write(chr(servpos).encode('ascii'))
        
        

t1 = threading.Thread(target=printPos, args=())
t1.daemon = True
t1.start()

while True:
    xprev = xrecount  
    ok, img = cap.read()
 
    if not ok: 
        break 

 
    faces = face_cascade.detectMultiScale(img, 1.3, 8)
 
    for (x,y,w,h) in faces:
        tempy = int((h-(h*0.56))/2)
        tempx = int((w-(w*0.86))/2)
        cv.rectangle(img,(int(x-tempx),int(y-tempy)),(x+w,y+h+tempy),(0,255,0),2)
        
        xrecount = int(x / 3.5)
        
        print(servpos)
    offcet = np.abs(65-xrecount)
    if xrecount < 65:    
        if (servpos + offcet) < 120:
            servpos += offcet
    elif xrecount > 65: 
        if (xrecount - offcet) > 0:
            servpos -= offcet


        
    cv.imshow("test", img)

    
    cv.waitKey(1)
