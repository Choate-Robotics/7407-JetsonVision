# echo_server.py

import socketserver
import camera

client_address = " "

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def setup(self):
        print("Socket Opened")

    def handle(self):
        #data = self.request[0].strip()
        socket = self.request[1]
        #print("{} wrote:".format(self.client_address[0]))
        #print(data)
        while True:
            socket.sendto(b'hello', self.client_address)
            print(self.request)
            #data = self.request[0].strip()
            #print(data)

    def finish(self):
        print("Socket Closed")

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5801

    # instantiate the server, and bind to localhost on port 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()
