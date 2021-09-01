from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from requests import get
import random


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]

PORT = 8000
available_relays = []

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


def get_relays():
    global available_relays
    tried_directory_nodes = []
    success = False

    for directory_node in DIRECTORY_NODES:
        request = get("http://" + directory_node + ':' + str(PORT) + "/get_relays")
        if request.status_code == 200:
            try:
                available_relays = [i.split(":") for i in request.text.split("\n")]
                success = True
            except:
                continue
        if success:
            break
    if not success:
        print("Failed to fetch available relays")

@app.get("/home", response_class=PlainTextResponse)
async def home():
    get_relays()
    return str(available_relays)