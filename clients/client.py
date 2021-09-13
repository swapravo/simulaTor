from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from requests import get, post
import random

import main
from utils import crypto, utils


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]
DIRECTORY_NODE_PORT = 8000
IP = main.IP
PUBLIC_KEY, PRIVATE_KEY = crypto.generate_asymmetric_keys()

relays = {
    'guard': [],
    'middle': [],
    'exit': []
    }
circuit = {
    'guard': None,
    'middle': None,
    'exit': None
    }
app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
    )

def choose_relays():
    global circuit

    try:
        circuit['guard'] = random.choice(relays['guard'])
        circuit['middle'] = random.choice(relays['middle'])
        circuit['exit'] = random.choice(relays['exit'])
    except IndexError:
        print("No relays found!")


@app.get("/get_relays", response_class=PlainTextResponse)
async def get_get_relays():
    global relays
    available_relays = []

    for directory_node in DIRECTORY_NODES:
        request = get("http://" + directory_node + ':' + str(DIRECTORY_NODE_PORT) + "/get_relays")
        if request.status_code == 200:
            try:
                available_relays = [i.split(":") for i in request.text.split("\n")]

                for relay in available_relays:
                    relay_type, ip, public_key = relay
                    public_key = crypto.decode_public_key(public_key)
                    symmetric_key = crypto.generate_shared_secret(PRIVATE_KEY, public_key)

                    _relay = utils.Relay(ip=ip, public_key=public_key, symmetric_key=symmetric_key, relay_type=relay_type)
                    if _relay not in relays[relay_type]:
                        relays[relay_type].append(_relay)
                        #print("New relay Added:")
                        #_relay.display()
            except Exception as e:
                print("Error while fetching relays:")
                print(str(e))
                continue
        else:
            print(directory_node, " seems to be offline!")
            continue


@app.get("/handshake", response_class=PlainTextResponse)
async def get_handshake():
    choose_relays()
    post_data = {"ip": IP, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
    response = post("http://" + circuit['guard'].ip + ":8000/handshake", params=post_data)


@app.get("/bootstrap", response_class=PlainTextResponse)
async def get_bootstrap():

    def pack3(data):
        data = data.encode('utf-8')

        # encrypt for exit relay
        data = crypto.encrypt(circuit['exit'].symmetric_key, data)

        # tell midle relay about exit relay
        data = utils.serialise([circuit['exit'].ip, data])
        # encrypt for middle relay
        data = crypto.encrypt(circuit['middle'].symmetric_key, data)        

        # tell gaurd relay about middle relay
        data = utils.serialise([circuit['middle'].ip, data])
        # encrypt for gaurd relay
        data = crypto.encrypt(circuit['guard'].symmetric_key, data)

        return data


    server = "example.com"
    data = utils.encode(pack3(server))

    print(circuit['guard'])

    post_data = {"ip": IP, "data": data}
    response = post("http://" + circuit['guard'].ip + ":8000/bootstrap", params=post_data)
 