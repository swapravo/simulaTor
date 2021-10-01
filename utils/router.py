import socket
from sys import argv, exit
from base64 import b16decode
from os import getpid, kill
from signal import SIGTERM

import crypto


class router:

    NAME = None

    CLIENT = None
    CLIENT_ADDRESS = None

    SERVER_IP = None
    SERVER_PORT = 8001

    BUFFER_SIZE = 512


    def __init__(self, ip, key):
        self.ROUTER_IP = ip
        self.KEY = b16decode(key)
        self.ROUTER_INCOMING_PORT = 8001
        self.ROUTER_OUTGOING_PORT = 8002

        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.CLIENT_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.CLIENT_SOCKET.bind((self.ROUTER_IP, self.ROUTER_INCOMING_PORT))
        self.SERVER_SOCKET.bind((self.ROUTER_IP, self.ROUTER_OUTGOING_PORT))

        print("Router ONLINE at IP:", self.ROUTER_IP, " PORT: ", self.ROUTER_INCOMING_PORT)


    # keep on recieving data
    def listen(self):
        self.CLIENT_SOCKET.listen(1)

        while self.CLIENT is None:
            self.CLIENT, self.CLIENT_ADDRESS = self.CLIENT_SOCKET.accept()
            print("Router", self.ROUTER_IP, "GOT CONNECTION from IP ", self.CLIENT_ADDRESS[0])

        while True:
            self.request = self.CLIENT.recv(self.BUFFER_SIZE)
            if not self.request:
                print("No data recieved. Shutting Down Router!")
                # close socket
                kill(getpid(), SIGTERM)
                

            # forward request
            self.forward()
            # fetch reply
            self.fetch()
            # send reply back
            self.CLIENT.send(self.response)
            if not self.response:
                print("No data recieved. Shutting Down Router!")
                # close socket
                kill(getpid(), SIGTERM)


    # connect to the next router on the network
    def connect(self, server_ip):
        self.SERVER_IP = server_ip
        print("Router", self.ROUTER_IP, "connecting to", self.SERVER_IP)
        self.SERVER_SOCKET.connect((self.SERVER_IP, self.SERVER_PORT))
        print("Router", self.ROUTER_IP, "connected to", self.SERVER_IP)


    # do crypto & forward the data to the next router
    def forward(self):
        self.request = crypto.decrypt(self.KEY, self.request)
        self.SERVER_SOCKET.send(self.request)


    # fetch the reply & do crypto
    def fetch(self):
        self.response = self.SERVER_SOCKET.recv(self.BUFFER_SIZE)
        self.response = crypto.encrypt(self.KEY, self.response)


self_ip = argv[1]
key = argv[2]
server_ip = argv[3]

Router = router(self_ip, key)
Router.connect(server_ip)
Router.listen()

