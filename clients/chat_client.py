import time
import socket
from base64 import b16encode

from utils import crypto

def connect(server_ip, guard_key, middle_key, exit_key):
    connection = socket.socket()
    connection.connect((server_ip, 8001))

    print("client Connected to guard...")

    print("guard key", guard_key)
    print("middle_key", middle_key)
    print("exit key", exit_key)


    #print("guard key", guard_key)
    #print("middle_key", middle_key)
    #print("exit key", exit_key)

    while True:

        message = "12345678"
        message = message.encode()
        message = crypto.encrypt(exit_key, message)
        message = crypto.encrypt(middle_key, message)
        message = crypto.encrypt(guard_key, message)

        connection.send(message)
        time.sleep(1)

        message = connection.recv(512)
        message = crypto.decrypt(guard_key, message)
        message = crypto.decrypt(middle_key, message)
        message = crypto.decrypt(exit_key, message)

        print(message)
