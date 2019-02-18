# echo_server.py
import json
import socket
import struct
import threading
from math import ceil
import sys, os
from time import time, sleep
from multiprocessing import Process, set_start_method
import signal
import traceback
import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

DEFAULT_CONFIGURATIONS = {
            'cameras': {
                'cam0': {
                    'resolution': 240,
                    'quality'   : 25
                },
                'cam1': {
                    'resolution': 240,
                    'quality'   : 25
                },
                'cam2': {
                    'resolution': 240,
                    'quality'   : 25
                },
                'cam3': {
                    'resolution': 240,
                    'quality'   : 25
                }
            }
        }

HANDSHAKE_SIGNATURE = b'\n_\x92\xc3\x9c>\xbe\xfe\xc1\x98'

clientaddr = "127.0.0.1", 5801
cam_num = 1

class ReadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pastData = None
        self.writesockets = []

    def run(self):
        global clientaddr
        HOST, PORT = "0.0.0.0", 5800
        print("Read socket binded to port ", PORT)



        for i in range(cam_num):
            self.writesockets.append(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
            self.writesockets[i].connect("./socket" + str(i) + ".sock")


        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(5)
            BUFFER_SIZE = 1024

            self.conn, self.addr = s.accept()
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                 struct.pack('ii', 1, 0))



            try:
                print('Connection address:', self.addr)
                clientaddr = self.addr

                t0 = time.time()
                self.conn.send(struct.pack('i',1))
                t1,t2 = struct.unpack('dd',self.conn.recv(16))
                t3 = time.time()
                offset = ((t1-t0)+(t2-t3))/2
                print(offset)


                while True:
                    data = self.conn.recv(BUFFER_SIZE)
                    if data == self.pastData: continue
                    if not data: break

                    print("received data:", data)
                    try:
                        dec = data.decode().split('|')
                        settings = json.loads(dec[-2])
                        settings['ip'] = self.addr[0]
                        data = json.dumps(settings).encode()
                        for i in range(cam_num):
                            self.writesockets[i].send(data+b'|')
                        self.pastData = data
                    except:
                        print(traceback.format_exc(), file=sys.stderr, flush=True)


            except ConnectionResetError:
                print('Disconnected')
            finally:
                print('Finally TCP Connection Closed')
                self.conn.close()
            self.pastData = None


class NetworkTablesThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        NetworkTables.initialize()

    def run(self):
        rd = NetworkTables.getTable("RobotData")



def handler(signum, frame):
    try:
        server.readThread.conn.close()
        print('Handler TCP Connection Closed')
    except:
        print('UDP No TCP Connection to Close')
    for process in server.processes:
        process.kill()
    sys.exit()

def startupcam(i):
    os.execv(sys.executable, ['python', './camera_process.py', str(i)])

class MainUDP:

    def __init__(self):
        self.cam_num = cam_num
        self.readThread = ReadingThread()
        self.processes = []
        for i in range(self.cam_num):

            if os.path.exists("./socket%d.sock"%i):
                os.remove("./socket%d.sock"%i)
            #set_start_method('spawn', force=True)
            p = Process(target=startupcam, args=[i, ])
            p.start()
            self.processes.append(p)

        #flag = False
        while not all(os.path.exists("./socket%d.sock"%i) for i in range(self.cam_num)): pass

        self.readThread.start()

server = MainUDP()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGQUIT, handler)
