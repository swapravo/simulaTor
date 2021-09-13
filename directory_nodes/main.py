#!/bin/python3

from uvicorn import run
from sys import argv

import directory_node

IP = argv[1]
PORT = 8000

if __name__ == "__main__":
    print("Starting DIRECTORY NODE at IP", IP, "PORT", PORT)
    run("directory_node:app", host=IP, port=PORT, reload=True, workers=1)
    print("Stopped DIRECTORY NODE at IP", IP, "PORT", PORT)
