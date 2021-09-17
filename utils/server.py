'''
import socket

connection = socket.socket()

SERVER_IP = "192.168.10.13"
SERVER_PORT = 8001
connection.bind((SERVER_IP, SERVER_PORT))

connection.listen(1)
connection, addr = connection.accept()

#print("connected:", connection, addr)

#connection.send("HELLO".encode())
#if connection.recv(5) != b'HELLO':
#    connection.close()

while True:
    message = connection.recv(512).decode()
    if message == "":
        break
    print(message)
    message = input('Me > ')
    if message == "":
        connection.send(b'')
        break
    connection.send(message.encode())
'''

import socket

connection = socket.socket()

SERVER_IP = "192.168.10.13"
SERVER_PORT = 8001
connection.bind((SERVER_IP, SERVER_PORT))

connection.listen(1)
connection, addr = connection.accept()

print("connected:", connection, addr)

while True:
    message = connection.recv(8).decode()
    print(message)
    if not message:
        break
