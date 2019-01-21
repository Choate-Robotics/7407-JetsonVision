import numpy as np
import cv2
from time import time
from processors import Frame
import struct

class CameraModule:
    def __init__(self, camNum):
        self.caps = cv2.VideoCapture(camNum)
        self.large_cam = 0
        self.frame = []
        self.encframe = None
        self.timestamp = None
        self.img_quality = 25
        self.screen_size = 240

    def start_capture(self):
        while True:
            self.timestamp = time()
            #print("timestamp len: " + str(len(self.timestamp)))
            self.frame = Frame(self.caps.read()[1]).GaussianBlur(3).resize(self.screen_size)
            self.encframe = self.frame.conv_jpeg(self.img_quality)

    def __del__(self):
        self.caps.release()


