import socket
from sys import argv

class router:

    NAME = None

    CLIENT = None
    CLIENT_ADDRESS = None

    SERVER_IP = None
    SERVER_PORT = 8001

    DATA = None

    def __init__(self, ip):

        self.ROUTER_IP = ip
        self.ROUTER_INCOMING_PORT = 8001
        self.ROUTER_OUTGOING_PORT = 8002

        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.CLIENT_SOCKET.bind((self.ROUTER_IP, self.ROUTER_INCOMING_PORT))
        self.SERVER_SOCKET.bind((self.ROUTER_IP, self.ROUTER_OUTGOING_PORT))

        print("Router ", self.NAME, " ONLINE at IP:", self.ROUTER_IP, " PORT: ", self.ROUTER_INCOMING_PORT)

    # keep on recieving data
    def listen(self):
        self.CLIENT_SOCKET.listen(1)

        while self.CLIENT is None:
            self.CLIENT, self.CLIENT_ADDRESS = self.CLIENT_SOCKET.accept()
            print("Got connection: ", self.CLIENT, self.CLIENT_ADDRESS)

        while True:
            self.data = self.CLIENT.recv(8)
            print(self.NAME, " Router recieved:", self.data)
            if not self.data:
                print("No data recieved. Closing socket!")
                break
            self.forward()

    # connect to the next router on the network
    def connect(self, server_ip):
        self.SERVER_IP = server_ip
        self.SERVER_SOCKET.connect((self.SERVER_IP, self.SERVER_PORT))

    # do crypto & forward the data to the next router
    def forward(self):
        # do_crypto()
        self.SERVER_SOCKET.send(self.data)

'''
r = router('127.0.0.1', 8001, 8002)
r.connect('127.0.0.1', 8003)
r.listen()
'''





































'''
class router:

    IP = None
    PORT = None
    SOCKET = None

    client_ip = None
    client_port = None
    client_socket = None

    destination_ip = None
    destination_port = None
    destination_socket = None
    
    data = None

    # create server
    def __init__(self, self_ip, self_port):
        self.IP = self_ip
        self.PORT = self_port

    # listen for incoming connections
    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _socket.bind((self.IP, self.PORT))
            self.SOCKET = _socket
            _socket.listen(1)
            self.client_socket, (self.client_ip, self.client_port) = _socket.accept()
        #print("connection recieved:", self.client_socket, self.client_ip, self.client_port)
            

    # connect to destination router/server
    def connect(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
            _socket.connect((ip, port))
        self.destination_ip = ip
        self.destination_port = port


    def recieve_from_client(self, size):
        print(self.client_socket)
        with self.client_socket as _socket:
            data = _socket.recv(size)
        print(data, "recieved from client")

    def send_to_client(self, socket):
        with self.client_socket as _socket:
            _socket.sendall(self.data)


    def recieve_from_destination(self, size):
        with self.destination_socket as _socket:
            data = _socket.recv(size)
        print(data, "recieved from destination")

    def send_to_destination(self, socket):
        with self.destination_socket as _socket:
            _socket.sendall(self.data)



r1 = router('127.0.0.1', int(argv[1]))
r1.serve()
while True:
    r1.recieve_from_client(5)
'''