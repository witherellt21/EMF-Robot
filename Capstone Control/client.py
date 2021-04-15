'''
Author: Taylor Witherell
Filename: client.py
Description: Contains client class for connecting to a host server and establishing a communications pipeline
'''

import socket

class Client():

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    def connect( self ):
        self.s.connect( (self.IP, self.PORT) )

    def send( self, string ):
        self.s.sendall( bytes( string, "utf-8" )  )

    def receive( self ):
        return self.s.recv(1024).decode("utf-8")
