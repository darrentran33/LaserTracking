import numpy as np
import cv2
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 60

kit = ServoKit(channels=16)
kit.servo[0].angle = 90
kit.servo[3].angle = 90

cap = cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

rows, cols, _ = frame.shape 

x_center = int(cols/2)
x_moving_center = int(cols/2)

y_center = int(row/2)
y_moving_center = int(row/2)

x_angle = 90
y_angle = 90

print(frame1.shape)
while True:
    GPIO.output(17,GPIO.HIGH)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        #cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.line(frame1, (x_moving_center,0),(x_moving_center,480),(0,250,0),2)
        cv2.line(frame1, (0,y_moving_center),(480,y_moving_center),(0,250,0),2)
        
        M= cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        x_moving_center = int((x + x + w)/2)
        y_moving_center = int((y + y + h)/2)
        
        print("X-coord: {}, Y-coord: {}" .format(cX,cY))
        
        break
       
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    while x_angle < 180 and x_angle > 0:
        if x_moving_center < x_center-30:
            x_angle += 1.5
        elif x_moving_center > x_center+30:
            x_angle -= 1.5
        kit.servo[0].angle = x_angle
    
    while y_angle < 180 and y_angle > 0:
        if y_moving_center < y_center-30:
            y_angle += 1.5
        elif y_moving_center > y_center+30:
            y_angle -= 1.5
        kit.servo[3].angle = y_angle
    
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
out.release()
