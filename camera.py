import numpy as np
import cv2
from time import time
from processors import Frame
import threading, socket
import struct
import os, sys
from math import ceil
import json
import signal
import traceback

HANDSHAKE_SIGNATURE = b'\n_\x92\xc3\x9c>\xbe\xfe\xc1\x98'

def chunk(frame):
    chunks = []
    for i in range(ceil(len(frame) / 1020)):
        chunks.append(i.to_bytes(4, "big") + frame[1020 * i:1020 * (i + 1)])
    return chunks

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
            self.frame = Frame(self.caps.read()[1]).GaussianBlur(3).resize(self.screen_size)
            self.encframe = self.frame.conv_jpeg(self.img_quality)

    def __del__(self):
        self.caps.release()

class SendingThread(threading.Thread):
    def __init__(self, camera_number, camera_module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera_number = camera_number
        self.camera_module = camera_module
        self.ip = '127.0.0.1'

    def run(self):
        HOST, PORT = "0.0.0.0", (5800 + self.camera_number + 1)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        print("Write socket binded to port", PORT)
        frameIndex = 0
        threading.Thread(target=self.camera_module.start_capture, args=[]).start()

        while True:
            if self.camera_module.encframe is not None:
                chunks = chunk(self.camera_module.encframe)
                times = struct.pack('>IIdd', int(ceil(len(self.camera_module.encframe) / 1020)), frameIndex,
                                    self.camera_module.timestamp,
                                    time() - self.camera_module.timestamp)
                s.sendto(HANDSHAKE_SIGNATURE + times,
                         (self.ip, (5800 + self.camera_number + 1)))  # Send handshake
                frameIndex += 1

                for i in chunks:
                    s.sendto(i, (self.ip, (5800 + self.camera_number + 1)))
                self.camera_module.encframe = None


class ReadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camNum = int(sys.argv[1])

    def run(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind("/tmp/socket" + str(self.camNum) + ".sock")

        while True:
            s.listen(1)
            BUFFER_SIZE = 1024
            self.conn, self.addr = s.accept()

            try:
                while True:
                    data = self.conn.recv(BUFFER_SIZE)
                    if not data: break
                    print("received data:", data)
                    settings = json.loads(data.decode())
                    print(settings)

                    cam.cameraModule.img_quality = settings['cam' + str(self.camNum)]['quality']
                    cam.cameraModule.screen_size = settings['cam' + str(self.camNum)]['resolution']
                    cam.sendingThread.ip = settings['ip']
            finally:
                print("Finally TCP Connection Closed")
                l_onoff = 1
                l_linger = 0
                self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                     struct.pack('ii', l_onoff, l_linger))
                self.conn.close()


def handler(signum, frame):
    try:
        l_onoff = 1
        l_linger = 0
        cam.readConfig.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                          struct.pack('ii', l_onoff, l_linger))
        cam.readConfig.conn.close()
        print('TCP Connection Closed')
        print('TCP Connection Closed')
    except:
        print(traceback.format_exc(), file=sys.stderr, flush=True)


class cameraWrapper:

    def __init__(self):
        print(sys.argv)
        self.camNum = int(sys.argv[1])
        self.cameraModule = CameraModule(self.camNum)
        self.sendingThread = SendingThread(self.camNum, self.cameraModule)
        self.readConfig = ReadingThread()

cam = cameraWrapper()
cam.readConfig.start()
cam.sendingThread.start()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGQUIT, handler)




