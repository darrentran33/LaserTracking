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

width = 320
height = 240

slope_x = (180/(-1*width))
slope_y = (180/(-1*height))
cap.set(3,width)
cap.set(4,height)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

rows, cols, _ = frame1.shape 

x_center = int(cols/2)
x_moving_center = int(cols/2)

y_center = int(row/2)
y_moving_center = int(row/2)

x_angle = 90
y_angle = 90

while True:
    
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            #adjust the contour area for better detection
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        GPIO.output(17,GPIO.HIGH)
        
        M= cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        x_moving_center = int((x + x + w)/2)
        y_moving_center = int((y + y + h)/2)
        
        break
       
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    while x_angle < 180 and x_angle > 0:
        x_angle = round((slope_x*x_moving_center)+180)
        kit.servo[0].angle = x_angle
    
    while y_angle < 180 and y_angle > 0:
        y_angle = round(-1*slope_y*y_moving_center)
        kit.servo[3].angle = y_angle
    
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
