#!/bin/python3

from uvicorn import run

import guard


if __name__ == "__main__":
    run("guard:app", host=guard.IP, port=guard.PORT, reload=True, workers=1)
