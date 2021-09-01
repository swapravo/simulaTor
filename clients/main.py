#!/bin/python3

from uvicorn import run

import client


if __name__ == "__main__":
    run("client:app", host=client.IP, port=client.PORT, reload=True, workers=1)
