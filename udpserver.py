# echo_server.py
import json
import socket
import struct
import threading
import dill
from math import ceil
import sys, os
from time import time, sleep
from multiprocessing import Process, set_start_method
import signal
import traceback

HANDSHAKE_SIGNATURE = b'\n_\x92\xc3\x9c>\xbe\xfe\xc1\x98'

clientaddr = "127.0.0.1", 5801


class ReadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        global clientaddr
        HOST, PORT = "0.0.0.0", 5800
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Read socket binded to port ", PORT)
        s.bind((HOST, PORT))

        self.writesockets = []
        for i in range(server.cam_num):
            self.writesockets.append(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
            self.writesockets[i].connect("/tmp/socket" + str(i) + ".sock")


        while True:
            s.listen(5)
            BUFFER_SIZE = 1024


            self.conn, self.addr = s.accept()
            l_onoff = 1
            l_linger = 0
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                 struct.pack('ii', l_onoff, l_linger))
            try:
                print('Connection address:', self.addr)
                clientaddr = self.addr

                while True:
                    data = self.conn.recv(BUFFER_SIZE)
                    if not data: break
                    print("received data:", data)
                    settings = json.loads(data.decode())
                    settings['ip'] = self.addr[0]
                    data = json.dumps(settings).encode()

                    for i in range(server.cam_num):
                        self.writesockets[i].send(data)

            except ConnectionResetError:
                print('Disconnected')
            finally:
                print('Finally TCP Connection Closed')

                self.conn.close()



def handler(signum, frame):
    try:
        l_onoff = 1
        l_linger = 0
        server.readThread.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                             struct.pack('ii', l_onoff, l_linger))
        server.readThread.conn.close()
        print('TCP Connection Closed')
    except:
        print(traceback.format_exc(), file=sys.stderr, flush=True)

def startupcam(i):
    os.execv(sys.executable, ['python', './camera.py', str(i)])

class MainUDP:

    def __init__(self):
        self.cam_num = 1
        self.readThread = ReadingThread()
        for i in range(self.cam_num):

            if os.path.exists("/tmp/socket%d.sock"%i):
                os.remove("/tmp/socket%d.sock"%i)
            set_start_method('spawn', force=True)
            Process(target=startupcam, args=[i,]).start()

        #flag = False
        while not all(os.path.exists("/tmp/socket%d.sock"%i) for i in range(self.cam_num)):pass

        self.readThread.start()

if __name__ == '__main__':
    server = MainUDP()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGQUIT, handler)