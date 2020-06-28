import numpy as np
import cv2
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

tool_cascade = cv2.CascadeClassifier('cascade.xml')

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

width = 320
height = 240

slope_x = (180/(-1*width))
slope_y = (180/(-1*height))
cap.set(3,width)
cap.set(4,height)

ret, img = cap.read()
rows, cols, _ = img.shape 

x_center = int(cols/2)
x_moving_center = int(cols/2)

y_center = int(rows/2)
y_moving_center = int(rows/2)

x_angle = 90
y_angle = 90

while True:
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tool = tool_cascade.detectMultiScale(gray, scaleFactor =1.05, minNeighbors=5, minSize = (50,50))

    for (x,y,w,h) in tool:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        GPIO.output(17,GPIO.HIGH)
        
        M= cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        x_moving_center = int((x + x + w)/2)
        y_moving_center = int((y + y + h)/2)
        
        break
    
    cv2.imshow('img',img)
    ret, img = cap.read()
    while x_angle < 180 and x_angle > 0:
        x_angle = round((slope_x*x_moving_center)+180)
        kit.servo[0].angle = x_angle
    
    while y_angle < 180 and y_angle > 0:
        y_angle = round(-1*slope_y*y_moving_center)
        kit.servo[3].angle = y_angle
    
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
