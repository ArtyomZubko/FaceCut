import sys, time, cv2 as cv, numpy as np
from multiprocessing import Process
import serial
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 9600
ser.close()
ser.open()

filename = 0
xoff= 0
yoff = 0
cap = cv.VideoCapture(0)

def serialWrite():
        #ser.write(xoff)
        #ser.write(yoff)
        print ("1")
p = Process(target=serialWrite)

if not cap.isOpened() :
    print("no")

while True:
    
 ok, img = cap.read() 
 if not ok: 
  break 

 faces = face_cascade.detectMultiScale(img, 1.3, 5)

 for (x,y,w,h) in faces:
    tempy = int((h-(h*0.56))/2)
    tempx = int((w-(w*0.86))/2)
    xoff= x
    yoff = y
    cv.rectangle(img,(int(x-tempx),int(y-tempy)),(x+w,y+h+tempy),(0,255,0),2)
 if not p.is_alive():
         p.start()
 
 cv.imshow("test", img)

 if cv.waitKey(10) == 49:
     k=0
     for (x,y,w,h) in faces:
         tempy = int((h-(h*0.56))/2)
         tempx = int((w-(w*0.86))/2)
         cropped = img[y-tempy: (y + h + tempy), x-tempx: (x + w)]
         k=k+1
         cv.imshow("Cropped image" + str(k), cropped)

         final_wide = 200 
         r = float(final_wide) / cropped.shape[1]
         dim = (final_wide, int(cropped.shape[0] * r))
         resized_pic = cv.resize(cropped, dim, interpolation = cv.INTER_AREA)
     
         filename = int(time.time()) + 1 
         cv.imwrite(str(filename + k) + ".png", resized_pic)
         
 cv.waitKey(30)

ser.close()
p.join()
