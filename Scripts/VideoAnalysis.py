import numpy as np
import cv2

cap = cv2.Videocapture(0)

if (cap.isOpened()== False)
    print("Error opening video capture")

while(True)
    ret, frame = cap.read()

    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("Frame", frame)

    ch = cv2.waitkey(1)
    if ch & 0xFF == ord('q')
        break

cap.release()
cv2.destroyAllWindows