import time
import socket

def connect(server_ip):
    connection = socket.socket()
    connection.connect((server_ip, 8001))

    print("client Connected to guard...")

    while True:
        connection.send(b'12345678')
        time.sleep(1)
        print(connection.recv(8))

