import sys, time, cv2 as cv, numpy as np


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

filename = 0

cap = cv.VideoCapture(0) 

while True:
    
 ok, img = cap.read() 
 if not ok: 
  break 

 faces = face_cascade.detectMultiScale(img, 1.3, 5)
 for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y-40),(x+w,y+h),(0,255,0),2)
 
 cv.imshow("test", img)

 if cv.waitKey(10) == 49: 
     cropped = img[y-1: (y + h)-1, x+2: (x + w)-1]
     cv.imshow("Cropped image", cropped)

     final_wide = 200 
     r = float(final_wide) / cropped.shape[1]
     dim = (final_wide, int(cropped.shape[0] * r))
     resized_pic = cv.resize(cropped, dim, interpolation = cv.INTER_AREA)
     
     filename = int(time.time()) + 1 
     cv.imwrite(str(filename) + ".png", resized_pic)
 cv.waitKey(30)
