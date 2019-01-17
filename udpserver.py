# echo_server.py

import socketserver
from camera import CameraModule
import socket
from _thread import *
import threading
import cv2
import time
import pickle

print_lock = threading.Lock()

cam = CameraModule(1)
def threaded():
    time.sleep(1)

    while True:
        # data received from client
        #data = c.recv(1024)
        # if not data:
        #     print('Socket Closed')
        #
        #     # lock released on exit
        #     print_lock.release()
        #     break
        #print(cam.frame)
        #c.send(pickle.dumps(cam.frame))
        print(pickle.dumps(cam.frame))





        # connection closed
    #c.close()

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5801
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("socket binded to port", PORT)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # c, addr = s.accept()
    # print('Connected to :', addr[0], ':', addr[1])

    print_lock.acquire()
    start_new_thread(threaded, ())
    cam.start_capture()

    # lock acquired by client



    # Start a new thread and return its identifier
    #start_new_thread(threaded, (c,))

    s.close()
