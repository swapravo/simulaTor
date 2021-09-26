from socket import socket, SOL_SOCKET, SO_REUSEADDR

SERVER_IP = "192.168.10.25"
SERVER_PORT = 8001

connection = socket()
connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
connection.bind((SERVER_IP, SERVER_PORT))

print("Server running...")
connection.listen(1)
connection, addr = connection.accept()

print("Got connection from IP: ", connection.getpeername()[0])

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
