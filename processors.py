import cv2
import numpy as np
import base64

class Frame:

    def __init__(self, frame):
        self.frame = frame

    def resize(self, width=240):
        self.frame = cv2.resize(self.frame, (width, int(width * 9 / 16)), interpolation = cv2.INTER_CUBIC)
        return self

    def GaussianBlur(self, radius):
        self.frame = cv2.GaussianBlur(self.frame, (radius, radius), 0)
        return self

    def flip_img(self):
        self.frame = cv2.flip(self.frame, 0)
        return self

    def conv_jpeg(self, quality):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', self.frame, encode_param)

        #cv.imshow('frame', encimg)
        #jpg_as_text = base64.b64encode(encimg)
        return encimg.tobytes()
