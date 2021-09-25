from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from requests import get, post
from base64 import b64encode
import time
import subprocess

import main
from utils import crypto, utils, router


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]
DIRECTORY_NODE_PORT = 8000
IP = main.IP
RELAY_TYPE = "middle"
PUBLIC_KEY, PRIVATE_KEY = crypto.generate_asymmetric_keys()

connected_clients = {}
app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


# register yourself to the directory nodes
#@app.get("/register", response_class=PlainTextResponse)
def get_register():
    post_data = {"ip": IP, "relay_type": RELAY_TYPE, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
    for directory_node in DIRECTORY_NODES:
        response = post("http://" + directory_node + ':' + str(DIRECTORY_NODE_PORT) + "/register_relay", params=post_data)

    return "Registered! as IP:" + str(IP) + ' as RELAY TYPE:' + RELAY_TYPE + '\n'


# host your public key
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

    #print("at middle")
    #print("Relay handshake completed:")
    #_relay.display()


def launch_router(server_ip):
    print("entering launch router from middle")
    subprocess.Popen(["python3", "relays/exit/r.py" , IP, server_ip])
    print("exiting launch router from middle")  
    # give the router some time to start up
    time.sleep(3)


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

        # decrypt layer 2 of 3
        data = crypto.decrypt(_client.symmetric_key, data)

        # deserialise data
        next_server, data = utils.deserialise(data)

        connected_clients[ip].next_server = next_server
        # Now exchange keys/handshake with the exit relay

        # fetch the exit relay's key and generate the shared secret
        request = get("http://" + connected_clients[ip].next_server + ":8000/public_key")
        public_key = crypto.decode_public_key(request.text)
        symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, public_key)

        _relay = utils.Relay(ip=next_server, public_key=public_key, symmetric_key=symmetric_key, relay_type="exit")
        connected_clients[next_server] = _relay

        # send the middle's relay's public key to the exit relay
        post_data = {"ip": IP, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
        response = post("http://" + connected_clients[ip].next_server + ":8000/handshake", params=post_data)

        # tell the exit relay the public key of the client
        # so that he derives the secret shared between the client
        # and himself
        data = [crypto.encode_public_key(_public_key), data]

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


        #print("AT MIDDLE")
        #for i in connected_clients:
        #    connected_clients[i].display()
        launch_router(connected_clients[ip].next_server)
        print("leaving middle relay ")


time.sleep(5)
get_register()
