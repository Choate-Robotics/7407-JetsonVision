import cv2 as cv
import numpy as np
import base64

class Frame:

    def __init__(self, frame):
        self.frame = frame

    def resize(self, width=240):
        self.frame = cv.resize(self.frame, (width,int(width*9/16)))
        return self

    def stitch_images(self, smallCam1, smallCam2):
        concat = np.concatenate((smallCam1.frame, smallCam2.frame), axis=1)
        self.frame = np.concatenate((self.frame, concat), axis=0)
        return self

    def conv_jpeg(self):
        encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
        result, encimg = cv.imencode('.jpg', self.frame, encode_param)
        jpg_as_text = base64.b64encode(encimg)
        return jpg_as_text
