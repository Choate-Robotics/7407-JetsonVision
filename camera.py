import numpy as np
import cv2
import time
from processors import Frame

class CameraModule:
    def __init__(self, cam_num):
        self.caps = []
        for i in range(cam_num):
            self.caps.append(cv2.VideoCapture(i))
        self.large_cam = 0
        self.cam_num = cam_num
        self.large_screen = 240
        self.small_screen = 0 if cam_num <= 1 else self.large_screen//(cam_num-1)
        self.frame = []



    def set_large_cam(self, large_cam_num):
        self.large_cam = large_cam_num

    def start_capture(self):
        while (True):
            #start = time.time()
            # Capture frame-by-frame
            self.sf = []
            self.frames = []

            for i in range(self.cam_num):
                self.frames.append(self.caps[i].read()[1])

            for i in range(self.cam_num):
                self.sf.append(Frame(self.frames[i]))
                if i == self.large_cam:
                    self.sf[i].resize(self.large_screen)
                else:
                    self.sf[i].resize(self.small_screen)

            self.frame = self.sf[self.large_cam].stitch_images([s.frame for s in (self.sf[:self.large_cam] + self.sf[self.large_cam+1:])])
            self.frame = self.frame.frame
            #print(time.time()-start)


    def __del__(self):
        for cap in self.caps:
            cap.release()






    # Our operations on the frame come here

    # Display the resulting frame
    # cv2.imshow('frame',fr1.frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    #print(time.time()-start)

# When everything done, release the capture


