import cv2
import numpy as np
import base64

class BaseFrame:
    def __init__(self, frame:np.array):
        self.frame = frame
        self.process()
    
    def process(self):
        raise NotImplementedError
    
    def conv_jpeg(self, quality) -> bytes:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', self.frame, encode_param)
        return encimg.tobytes()
    
    def resize(self, width=240):
        self.frame = cv2.resize(self.frame, (width, int(width * 9 / 16)), interpolation = cv2.INTER_CUBIC)
        return self

    def GaussianBlur(self, radius):
        self.frame = cv2.GaussianBlur(self.frame, (radius, radius), 0)
        return self

    def flip_img(self):
        self.frame = cv2.flip(self.frame, 0)
        return self

class VideoStreamingFrame(BaseFrame):
    def process(self):
        pass

class AngleDetectionFrame(BaseFrame):
    def process(self):
        img = cv2.GaussianBlur(self.frame, (3, 3), 0)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, img = cv2.threshold(img, 192, 255, cv2.THRESH_BINARY)
        img, contours, hierarchy = cv2.findContours(img, 1, 2)
        c = max(contours, key=lambda c: sum(cv2.minAreaRect(c)[1]))
        rect = cv2.minAreaRect(c)
        b = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(self.frame, [b], -1, (0, 0, 255), 2)
        cv2.putText(self.frame, str(round(rect[2], 2)) + 'deg', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

