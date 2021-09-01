#!/bin/python3

from uvicorn import run
from sys import argv

import middle

IP = argv[1]
PORT = 8000

if __name__ == "__main__":
    print("Starting MIDDLE RELAY at IP", IP, "PORT", PORT)
    run("middle:app", host=IP, port=PORT, reload=True, workers=1)
    print("Stopped MIDDLE RELAY at IP", IP, "PORT", PORT)
