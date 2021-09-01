#!/bin/python3

from uvicorn import run

import directory_node


if __name__ == "__main__":
    run("directory_node:app", host=directory_node.IP, port=directory_node.PORT, reload=True, workers=1)
