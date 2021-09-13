#!/bin/python3

from uvicorn import run
from sys import argv

import client

IP = argv[1]
PORT = 8000

if __name__ == "__main__":
    print("Starting CLIENT at IP", IP, "PORT", PORT)
    run("client:app", host=IP, port=PORT, reload=True, workers=1)
    print("Stopped CLIENT at IP", IP, "PORT", PORT)
