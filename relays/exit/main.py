#!/bin/python3

from uvicorn import run
from sys import argv

import exit

IP = argv[1]
PORT = 8000

if __name__ == "__main__":
    print("Starting EXIT RELAY at IP", IP, "PORT", PORT)
    run("exit:app", host=IP, port=PORT, reload=True, workers=1)
    print("Stopped EXIT RELAY at IP", IP, "PORT", PORT)
