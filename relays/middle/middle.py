from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from requests import post
import main


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]
DIRECTORY_NODE_PORT = 8000
IP = main.IP
RELAY_TYPE = "middle"

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)

def register():
    post_data = {"ip": IP, "relay_type": RELAY_TYPE}
    for directory_node in DIRECTORY_NODES:
        response = post("http://" + directory_node + ':' + str(DIRECTORY_NODE_PORT) + "/register_relay", params=post_data)


@app.get("/register", response_class=PlainTextResponse)
async def home():
    register()
    return "registered!"
