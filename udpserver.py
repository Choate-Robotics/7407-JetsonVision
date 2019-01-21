# echo_server.py
import json
import socket
import struct
import threading
from math import ceil
from time import time

from camera import CameraModule

HANDSHAKE_SIGNATURE = b'\n_\x92\xc3\x9c>\xbe\xfe\xc1\x98'

clientaddr = "127.0.0.1", 5801


def chunk(frame):
    chunks = []
    for i in range(ceil(len(frame) / 1020)):
        chunks.append(i.to_bytes(4, "big") + frame[1020 * i:1020 * (i + 1)])
    return chunks


def workerRead():
    global clientaddr
    HOST, PORT = "0.0.0.0", 5800
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print("Read socket binded to port", PORT)

    while True:
        data, address = s.recvfrom(1024)
        clientaddr = address
        print(data, address)


class ReadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        global clientaddr
        HOST, PORT = "0.0.0.0", 5800
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))

        while True:
            s.listen(5)
            BUFFER_SIZE = 1024

            conn, addr = s.accept()
            try:
                print('Connection address:', addr)
                clientaddr = addr

                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data: break
                    print("received data:", data)
                    settings = json.loads(data.decode())
                    print(settings)

                    for i in range(server.cam_num):
                        getattr(server, 'cameras')[i].camera_module.img_quality = settings['cam' + str(i)]['quality']
                        getattr(server, 'cameras')[i].camera_module.screen_size = settings['cam' + str(i)]['resolution']
            finally:
                conn.close()


class SendingThread(threading.Thread):
    def __init__(self, camera_number, camera_module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera_number = camera_number
        self.camera_module = camera_module

    def run(self):
        global clientaddr
        HOST, PORT = "0.0.0.0", (5800 + self.camera_number + 1)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        print("Write socket binded to port", PORT)
        frameIndex = 0
        threading.Thread(target=self.camera_module.start_capture, args=[]).start()

        while True:
            if self.camera_module.encframe is not None:
                # print(clientaddr)
                # print(len(cam.encframe))
                # print(self.camera_module.screen_size)
                chunks = chunk(self.camera_module.encframe)
                times = struct.pack('>IIdd', int(ceil(len(self.camera_module.encframe) / 1023)), frameIndex,
                                    self.camera_module.timestamp,
                                    time() - self.camera_module.timestamp)
                # print("processing time len: " + str(len(processingtime)))
                s.sendto(HANDSHAKE_SIGNATURE + times,
                         (clientaddr[0], (5800 + self.camera_number + 1)))  # Send handshake
                # s.sendto(times, (clientaddr[0], (5800 + camNum + 1)))
                frameIndex += 1

                for i in chunks:
                    s.sendto(i, (clientaddr[0], (5800 + self.camera_number + 1)))
                self.camera_module.encframe = None


class MainUDP:
    cam_num = 1
    cameras = []
    readThread = ReadingThread()
    for i in range(cam_num):
        cameras.append(SendingThread(i, CameraModule(i)))

    def __init__(self):
        for i in range(self.cam_num):
            self.cameras[i].start()

        #threading.Thread(target=workerRead, args=[]).start()
        self.readThread.start()


server = MainUDP()
