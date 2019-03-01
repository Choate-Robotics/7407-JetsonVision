import sys
import time
import cv2
caps = []
for i in range(7):
    try:
        print(str(i) + ' -----------------------------------------')
        caps.append(cv2.VideoCapture(i, cv2.CAP_V4L))
        if caps[-1].read() != (False, None):
            print("Works")
        self.caps[-1].set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        if caps[-1].read() != (False, None):
            print("works with mjpg")
        self.caps[-1].set(cv2.CAP_PROP_FPS, 60)
        if caps[-1].read() != (False, None):
            print("works with 60fps")
    except:
        pass
    caps.pop()
    time.sleep(1)
