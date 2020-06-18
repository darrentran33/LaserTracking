import numpy as np
import cv2
from PCA9685 import PCA9685
import RPi.GPIO as GPIO

GPI.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(0, GPIO.OUT)

pwm = = PCA9685(0x40, debug = False)
pwm.setPWMFreq(60)
pwm.setServoPosition(0,90)
rows, cols, _ = frame.shape 


cap = cv2.VideoCapture(0)

cap.set(3,480)
cap.set(4,320)

x_center = int(cols/2)
x_moving_center = int(cols/2)

y_center = int(row/2)
y_moving_center = int(row/2)

x_angle = 90
y_angle = 90

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        M= cv2.Moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        moving_center = int((x + x + w)/2)
        
        print("X-coord: {}, Y-coord: {}" .format(cX,cY))
        
        break
       
    #image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    GPIO.output(0,GPIO.HIGH)
    
    if x_moving_center < x_center
        x_angle += 1.5
    if x_moving_center > x_center
        x_angle -= 1.5
    pwm.setServoPosition(0,0,x_angle)
    
    if y_moving_center < y_center
        y_angle += 1.5
    if y_moving_center > y_center
        y_angle -= 1.5
    pwm.setServoPosition(3,0,y_angle)
    
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
out.release()
