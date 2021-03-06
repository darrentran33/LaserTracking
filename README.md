# LaserTracking

This project focuses on object detection using the OpenCV API. The PeopleTracker.py script is used to track an object's movement, meaning it takes the difference between the current frame and the preceding frame and any change will be highlight. The ToolTracker.py script is used track a specific tool. In this script's case, a Haar cascade was trained on the Swiss Army knife logo and will detect and track that logo throughout the frames The Haar cascade has a 30% flase positive rate and 99% identification rate. 

In both of the scripts, the current location of the object is track and an algorithm is used to track the vertical and horizontal deviation from the center. the difference is then relayed to two servo motors representing 2 DOF by an I2C connection: one controlling pitch and another controlling yaw. Based on the object's location, a laser will be directed to point to the object.

<img src="https://github.com/darrentran33/LaserTracking/blob/master/Screenshots/physrep.gif" width="900" height="500">
<img src="https://github.com/darrentran33/LaserTracking/blob/master/Screenshots/tracking3.gif" width="900" height="500">

## Software Libraries Used

* OpenCV 4.2.0
* NumPy 1.19.0
* Adafruit_servokit
* RPi.GPIO

## Hardware Used

* 2 x MG996R Servo Motors
* 4 AA Battery Holder
* PCA9685 Motor Driver Board
* Raspberry Pi 2 Model B
* Raspberry Pi Camera Module 5MP 1080p

<img src="https://github.com/darrentran33/LaserTracking/blob/master/Screenshots/Camera.JPG" width="600" height="500">
