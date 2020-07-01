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
# Collects the angle information

x_center = int(cols/2)
x_moving_center = int(cols/2)

y_center = int(rows/2)
y_moving_center = int(rows/2)

x_angle = 90
y_angle = 90

while True:
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tool = tool_cascade.detectMultiScale(gray, scaleFactor =1.05, minNeighbors=5, minSize = (50,50))
    # Adjust scale factor for better detection

    for (x,y,w,h) in tool:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        GPIO.output(17,GPIO.HIGH)
        
        x_moving_center = int((x + x + w)/2)
        y_moving_center = int((y + y + h)/2)
        # parameter to change the laser position
        
        break
    
    cv2.imshow('img',img)
    ret, img = cap.read()
    
    x_angle = round((slope_x*x_moving_center)+180)
    kit.servo[0].angle = x_angle
    
    y_angle = round(-1*slope_y*y_moving_center)
    kit.servo[3].angle = y_angle
    
    ch = cv2.waitKey(30)
    #change this to alter lag in camera feed
    if ch & 0xFF == ord('q'):
        GPIO.output(17,GPIO.LOW)
        break

cap.release()
cv2.destroyAllWindows()
