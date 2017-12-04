import sys, time, cv2 as cv, numpy as np
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
userFace = cv.imread('e7f8a296d3.jpg')

filename = 0

cap = cv.VideoCapture(0)

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

    if x-tempx < 0:
        continue
    if y-tempy < 0:
        continue
    #if x > w:
    #    continue
    #if y > h + tempy - 3:
    #    continue
    userFaceRecized = cv.resize(userFace,  (w + tempx,h+tempy * 2), interpolation = cv.INTER_AREA)
    #mask = cv.threshold(userFaceRecized, 10, 255, cv.THRESH_BINARY)
    #userFaceRecized = cv.bitwise_not(mask)
    img[y-tempy: (y + h + tempy), x-tempx: (x + w)] = userFaceRecized
    #cv.rectangle(img,(int(x-tempx),int(y-tempy)),(x+w,y+h+tempy),(0,255,0),2)
 
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
