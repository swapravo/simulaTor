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
RELAY_TYPE = "guard"
PUBLIC_KEY, PRIVATE_KEY = crypto.generate_asymmetric_keys()

connected_clients = {}

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
    )


# register yourself to the directory nodes
@app.get("/register", response_class=PlainTextResponse)
async def get_register():
    post_data = {"ip": IP, "relay_type": RELAY_TYPE, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
    for directory_node in DIRECTORY_NODES:
        response = post("http://" + directory_node + ':' + str(DIRECTORY_NODE_PORT) + "/register_relay", params=post_data)
    return str(post_data)


# host your public key
@app.get("/public_key", response_class=PlainTextResponse)
async def get_public_key():
    return utils.encode(bytes(PUBLIC_KEY))


# exchange public keys & establish shared symmetric key
@app.post("/handshake", response_class=PlainTextResponse)
async def post_handshake(ip: str, public_key: str):

    public_key = crypto.decode_public_key(public_key)
    symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, public_key)

    client = utils.Client(ip=ip, public_key=public_key, symmetric_key=symmetric_key)
    connected_clients[ip] = client


# create circuit
@app.post("/bootstrap", response_class=PlainTextResponse)
async def post_bootsrap(ip: str, data: str):

    if ip in connected_clients:

        # decode data
        data = utils.decode(data)

        # decrypt this data
        data = crypto.decrypt(connected_clients[ip].symmetric_key, data)

        # deserialise data
        next_server, data = utils.deserialise(data)
        connected_clients[ip].next_server = next_server

        print("At guard:")
        print(next_server, data)

        # Now exchange keys/handshake with the middle relay

        # fetch the middle relay's key and generate the shared secret
        request = get("http://" + connected_clients[ip].next_server + ":8000/public_key")
        public_key = crypto.decode_public_key(request.text)
        symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, public_key)

        _relay = utils.Relay(ip=next_server, public_key=public_key, symmetric_key=symmetric_key, relay_type="middle")
        connected_clients[next_server] = _relay

        # send the gaurd's public key to the middle relay
        post_data = {"ip": IP, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
        response = post("http://" + connected_clients[ip].next_server + ":8000/handshake", params=post_data)

        # tell the middle relay the public key of the client
        # so that he derives the secret shared between the client
        # and himself
        data = [crypto.encode_public_key(connected_clients[ip].public_key), data]

        # now reserialise this
        data = utils.serialise(data)

        # now encrypt this with the key shared between
        # the gaurd and the middle relay
        data = crypto.encrypt(connected_clients[next_server].symmetric_key, data)

        # encode data before sending it over to the middle relay
        data = utils.encode(data)

        # bootstrap with the middle relay
        post_data = {"ip": IP, "data": data}
        response = post("http://" + connected_clients[ip].next_server + ":8000/bootstrap", params=post_data)
