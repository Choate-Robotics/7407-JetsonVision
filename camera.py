import numpy as np
import cv2
import time
from processors import Frame

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap3 = cv2.VideoCapture(2)
large_cam = 0
cam_num = 3
large_screen = 240
small_screen = large_screen//(cam_num-1)


while(True):
    # Capture frame-by-frame
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()
    ret, frame3 = cap3.read()
    #ret, frame = cap2.read()
    #ret,

    if large_cam == 0:
        fr1 = Frame(frame1)
        fr2 = Frame(frame2)
        fr3 = Frame(frame3)
    if large_cam == 1:
        fr1 = Frame(frame2)
        fr2 = Frame(frame1)
        fr3 = Frame(frame3)
    if large_cam == 2:
        fr1 = Frame(frame3)
        fr2 = Frame(frame1)
        fr3 = Frame(frame3)


    #start=time.time()

    fr1.resize(large_screen)
    fr2.resize(small_screen)
    fr3.resize(small_screen)
    frame = fr1.stitch_images(fr2, fr3)


    # Our operations on the frame come here

    # Display the resulting frame
    # cv2.imshow('frame',fr1.frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    #print(time.time()-start)

# When everything done, release the capture
cap1.release()
cap2.release()
cap3.release()

cv2.destroyAllWindows()