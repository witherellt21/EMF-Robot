'''
Filename: server.py
Written by: Taylor Witherell
Description: Creates a server socket established on the RPi's IP address available for client connection
'''

import socket

class Server():
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.disconnect_counter = 1

    def start(self):
        self.s.bind((self.IP, self.PORT))
        self.s.listen()

    def receiveConnection(self):
        print('Awaiting connection to ', self.IP, ' at ', self.PORT)
        self.conn, self.addr = self.s.accept()
        self.disconnect_counter = 0
        print('Connected by', self.addr)

    def send(self, string):
        self.conn.send( bytes( string, "utf-8"))

    def receive(self):
        data = self.conn.recv(1024)
        msg = data.decode("utf-8")
        if msg:
            return msg
        else:
            self.disconnect_counter += 1


'''
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    clientsocket.send( bytes( "Hey there!!!", "utf-8"))
    clientsocket.close()
'''
