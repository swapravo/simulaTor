from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from requests import get, post
from base64 import b64encode

import main
from utils import crypto, utils


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]
DIRECTORY_NODE_PORT = 8000
IP = main.IP
RELAY_TYPE = "exit"
PUBLIC_KEY, PRIVATE_KEY = crypto.generate_asymmetric_keys()

connected_clients = {}
app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


@app.get("/register", response_class=PlainTextResponse)
async def get_register():
    post_data = {"ip": IP, "relay_type": RELAY_TYPE, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
    for directory_node in DIRECTORY_NODES:
        response = post("http://" + directory_node + ':' + str(DIRECTORY_NODE_PORT) + "/register_relay", params=post_data)
    return "Registered! as IP:" + str(IP) + ' as RELAY TYPE:' + RELAY_TYPE + '\n'

@app.get("/public_key", response_class=PlainTextResponse)
async def get_public_key():
    return utils.encode(bytes(PUBLIC_KEY))


# exchange public keys & establish shared symmetric key
@app.post("/handshake", response_class=PlainTextResponse)
async def post_handshake(ip: str, public_key: str):

    public_key = crypto.decode_public_key(public_key)
    symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, public_key)

    _relay = utils.Relay(ip=ip, public_key=public_key, symmetric_key=symmetric_key, relay_type='guard')
    connected_clients[ip] = _relay


# create circuit
@app.post("/bootstrap", response_class=PlainTextResponse)
async def post_bootsrap(ip: str, data: str):

    if ip in connected_clients:

        # decode data
        data = utils.decode(data)

        # decrypt this data
        data = crypto.decrypt(connected_clients[ip].symmetric_key, data)

        # deserialise data
        _public_key, data = utils.deserialise(data)
        _public_key = crypto.decode_public_key(_public_key)
        _symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, _public_key)

        # remember this client's keys
        _client = utils.Client(public_key=_public_key, symmetric_key=_symmetric_key)

        data = crypto.decrypt(_client.symmetric_key, data)

        print(data)
        #print(utils.deserialise(data))

