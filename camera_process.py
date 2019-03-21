import numpy as np
from time import time,sleep
import threading, socket
import struct
import os, sys
from math import ceil, floor
import json
import signal
import traceback
import cProfile
from video_frame import VideoStream,AngleDetection

HANDSHAKE_SIGNATURE = b'\n_\x92\xc3\x9c>\xbe\xfe\xc1\x98'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def chunk(frame):
    chunks = []
    for i in range(int(ceil(len(frame) / 1020))):
        chunks.append(i.to_bytes(4, "big") + frame[1020 * i:1020 * (i + 1)])
    return chunks





class SendingThread(threading.Thread):
    def __init__(self, camera_number, camera_module, test, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera_number = camera_number
        self.camera_module = camera_module
        self.test = test
        self.ip = '127.0.0.1'

    def run(self):
        if self.test == 0:
            HOST, PORT = "0.0.0.0", (5800 + self.camera_number + 1)
        else:
            HOST, PORT = "0.0.0.0", (5800 + self.camera_number + 2)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        print("Write socket bound to port", PORT)
        frameIndex = 0

        while True:
            if self.camera_module.camReady:
                chunks = chunk(self.camera_module.encframe)


                times = struct.pack('>IIdd', int(ceil(len(self.camera_module.encframe) / 1020)), frameIndex,
                                    self.camera_module.timestamp,
                                    time() - self.camera_module.timestamp)
                s.sendto(HANDSHAKE_SIGNATURE + times,
                         (self.ip, (5800 + self.camera_number + 1)))  # Send handshake

                frameIndex += 1

                for i in chunks:
                    s.sendto(i, (self.ip, (5800 + self.camera_number + 1)))
                self.camera_module.camReady = False



class ReadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pastData=None

    def run(self):
        global img_quality,resolution,ip
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind("./socket" + str(camera_number) + ".sock")
        print("Unix socket bind to ./socket" + str(camera_number) + ".sock", )

        while True:
            s.listen(2)
            BUFFER_SIZE = 1024
            self.conn, self.addr = s.accept()
            l_onoff = 1
            l_linger = 0
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                           struct.pack('ii', l_onoff, l_linger))

            try:
                while True:
                    data = self.conn.recv(BUFFER_SIZE)
                    if data == self.pastData: continue
                    if not data: break
                    print("Camera",camera_number,"received data:", data)
                    try:
                        dec = data.decode().split('|')
                        print(dec)
                        settings = json.loads(dec[-2])
                        img_quality = settings['cam' + str(camera_number)]['quality']
                        resolution = settings['cam' + str(camera_number)]['resolution']
                        ip = settings['ip']
                        self.pastData = data
                        print('Settings Updated')
                    except:
                        print(traceback.format_exc(), file=sys.stderr, flush=True)


            except ConnectionResetError:
                print('Disconnected')
            except OSError:
                print('Camera Killed Read Thread')
            finally:
                print("Camera Finally TCP Connection Closed")
                self.conn.close()


def handler(signum, frame):
    try:
        reading_thread.conn.close()
        print('Camera Handler TCP Connection Closed')
    except:
        print(traceback.format_exc(), file=sys.stderr, flush=True)



signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGQUIT, handler)

camera_number=int(sys.argv[1])
camera=VideoStream(camera_number)



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 5801 + camera_number))
print("Write socket bound to port", 5801 + camera_number)
frameIndex = 0
ip='127.0.0.1'
img_quality=80
resolution=240

reading_thread=ReadingThread()
reading_thread.start()

while True:
    time_started=time()
    frame=camera.getCompressedFrame()
    # f=open('img/%d.jpg'%frameIndex,'wb+')
    # f.write(frame.tobytes())
    # f.close()
    # print('%d bytes written to img/%d.jpg  %s'%(len(frame),frameIndex,frame.tobytes().hex()))
    # print('frame captured')

    chunks=chunk(frame)
    
    times = struct.pack('>IIdd', int(ceil(len(frame) / 1020)), frameIndex,
                        time_started,
                        time() - time_started)
    s.sendto(HANDSHAKE_SIGNATURE + times,
             (ip, (5801 + camera_number)))  # Send handshake
    frameIndex += 1
    for i in chunks:
        s.sendto(i, (ip, (5801 + camera_number)))
    camera.setQuality(img_quality)
    camera.setResolution(resolution)





