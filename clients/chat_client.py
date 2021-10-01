import time
import socket
from base64 import b16encode
from sys import exit

from utils import crypto


DATA_PORT = 8001
BUFFER_SIZE = 512


def connect(server_ip, guard_key, middle_key, exit_key):
    connection = socket.socket()

    try:
        connection.connect((server_ip, DATA_PORT))
    except:
        print("FAILED to Connect to guard! Guard is Offline")
        exit(0)

    print("Client Connected to IP", server_ip)

    while True:

        message = input('Me >>> ')
        message = message.encode()
        message = crypto.encrypt(exit_key, message)
        message = crypto.encrypt(middle_key, message)
        message = crypto.encrypt(guard_key, message)

        connection.send(message)
        time.sleep(1)

        message = connection.recv(BUFFER_SIZE)
        message = crypto.decrypt(guard_key, message)
        message = crypto.decrypt(middle_key, message)
        message = crypto.decrypt(exit_key, message)
        message = message.decode()

        print("Server <<< ", message)
