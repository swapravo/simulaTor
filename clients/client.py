from requests import get, post
import random
import socket
import time

from utils import crypto, utils
import chat_client


# these IPs & their public keys are pinned into the tor client
DIRECTORY_NODES = ["192.168.10.10", "192.168.10.11"]
CONTROL_PORT = 8000
DATA_PORT = 8001
IP = "192.168.10.27"
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


# fetch relay info from directory nodes
def get_relays():
    global relays
    available_relays = []

    for directory_node in DIRECTORY_NODES:
        request = get("http://" + directory_node + ':' + str(CONTROL_PORT) + "/get_relays")
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
            except Exception as e:
                print("Error while fetching relays:\n", e)
                continue
        else:
            print("Directory Node ", directory_node, " seems to be offline!")
            continue


# select relays to form a circuit with
def choose_relays():
    global circuit

    try:
        circuit['guard'] = random.choice(relays['guard'])
        circuit['middle'] = random.choice(relays['middle'])
        circuit['exit'] = random.choice(relays['exit'])
    except IndexError:
        print("No relays found!")


# exchange public keys & establish shared symmetric key
def handshake():
    post_data = {"ip": IP, "public_key": crypto.encode_public_key(PUBLIC_KEY)}
    response = post("http://" + circuit['guard'].ip + ":" + str(CONTROL_PORT) + "/handshake", params=post_data)


# make the guard relay connect with the middle relay &
# make the middle relay connect with the exit relay
def bootstrap():

    handshake()

    def pack3(server_ip):

        data = utils.serialise([crypto.encode_public_key(PUBLIC_KEY), server_ip])
        # encrypt for exit relay
        data = crypto.encrypt(circuit['exit'].symmetric_key, data)

        # tell midle relay about the exit relay & client's public key
        data = utils.serialise([circuit['exit'].ip, crypto.encode_public_key(PUBLIC_KEY), data])
        # encrypt for middle relay
        data = crypto.encrypt(circuit['middle'].symmetric_key, data)        

        # tell gaurd relay about middle relay
        data = utils.serialise([circuit['middle'].ip, data])
        # encrypt for gaurd relay
        data = crypto.encrypt(circuit['guard'].symmetric_key, data)

        return data

    server = "192.168.10.25"
    data = utils.encode(pack3(server))

    post_data = {"ip": IP, "data": data}
    response = post("http://" + circuit['guard'].ip + ":" + str(CONTROL_PORT) + "/bootstrap", params=post_data)

def main():

    get_relays()
    choose_relays()
    bootstrap()

    chat_client.connect(circuit['guard'].ip, circuit['guard'].symmetric_key, circuit['middle'].symmetric_key, circuit['exit'].symmetric_key)

main()
