'''
import socket

connection = socket.socket()

SERVER_IP = "192.168.10.10"
SERVER_PORT = 8001
HELLO = "HELLO".encode()


connection.connect((SERVER_IP, SERVER_PORT))

#if connection.recv(5) != HELLO:
#    connection.close()
#connection.send(HELLO)

while True:

    message = input("me > ")
    if message == "":
        connection.send(b'')
        connection.close()
        break

    connection.send(message.encode())
    message = connection.recv(512).decode()
    if message == "":
        break
    print(message)
'''

import socket, time

def f():
    connection = socket.socket()
    SERVER_IP = "192.168.10.10"
    SERVER_PORT = 8001
    connection.connect((SERVER_IP, SERVER_PORT))

    while True:
        connection.send(b'12345678')
        time.sleep(1)
        print(connection.recv(8))

