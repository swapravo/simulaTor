#!/bin/python3

from uvicorn import run
from sys import argv

import guard

IP = argv[1]
PORT = 8000

if __name__ == "__main__":
    print("Starting GAURD RELAY at IP", IP, "PORT", PORT)
    run("guard:app", host=IP, port=PORT, reload=True, workers=1, log_level="error")
    print("Stopped GAURD RELAY at IP", IP, "PORT", PORT)
