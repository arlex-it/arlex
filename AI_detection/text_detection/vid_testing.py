#!/usr/bin/python3

import cv2
import numpy as np

# VIDEO READER

capture = cv2.VideoCapture('videos/cafe.mp4')

if not capture.isOpened():
    print("Error opening video stream")

while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Frame', gray)
        # Q to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
capture.release()
cv2.destroyAllWindows()
