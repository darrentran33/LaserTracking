# LaserTracking

This project focuses on object detection using the OpenCV API. The PeopleTracker.py script is used to track an object's movement, meaning it takes the difference between the current frame and the preceding frame and any change will be highlight. The ToolTracker.py script is used track a specific tool. In this scripts case, a Haar cascade was trained on the Swiss Army knife logo and will detect and track that logo throughout the frames. In both of the scripts, the current location of the object is track and an algorithm is used to track the vertical and horizontal deviation from the center. the difference is then relayed two servo motors representing 2 DOF: one controlling pitch and another controllign yaw. Based on the object's location, a laser will be directed to point to the object.

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
