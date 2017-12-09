import sys, time, cv2 as cv, numpy as np
import threading
import serial

ser = serial.Serial('COM8',9600)




face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

filename = 0
servpos = 90
xrecount = 0
cap = cv.VideoCapture(1)

if not cap.isOpened() :
    print("no")
ser.write(chr(servpos).encode('ascii'))

def printPos(xp):
        ser.write(chr(xp).encode('ascii'))
        print(xp)
        

while True:
    
 ok, img = cap.read() 
 if not ok: 
  break 

 
 faces = face_cascade.detectMultiScale(img, 1.3, 8)
 
 for (x,y,w,h) in faces:
    tempy = int((h-(h*0.56))/2)
    tempx = int((w-(w*0.86))/2)
    cv.rectangle(img,(int(x-tempx),int(y-tempy)),(x+w,y+h+tempy),(0,255,0),2)
    xrecount = int(x / 3.5)

    if xrecount < 65:
        if servpos+1 <= 120:
            servpos = servpos + 1
        t1 = threading.Thread(target=printPos, args=(servpos,))
        if not t1.isAlive():
            t1.start()
    elif xrecount > 65:
        if servpos-1 >= 0:
            servpos = servpos - 1
        t1 = threading.Thread(target=printPos, args=(servpos,))
        if not t1.isAlive():
            t1.start()

        
 cv.imshow("test", img)

 if cv.waitKey(10) == 49:
     k=0
     for (x,y,w,h) in faces:
         tempy = int((h-(h*0.56))/2)
         tempx = int((w-(w*0.86))/2)
         cropped = img[y-tempy + 2: (y + h + tempy - 1), x-tempx + 2: (x + w - 1)]
         k=k+1
         cv.imshow("Cropped image" + str(k), cropped)

         final_wide = 200 
         r = float(final_wide) / cropped.shape[1]
         dim = (final_wide, int(cropped.shape[0] * r))
         resized_pic = cv.resize(cropped, dim, interpolation = cv.INTER_AREA)
     
         filename = int(time.time()) + 1 
         cv.imwrite(str(filename + k) + ".png", resized_pic)
         
 cv.waitKey(1)
