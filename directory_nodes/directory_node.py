"""
IPs for directory nodes: 192.168.10.10, 192.168.10.11
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import main


registered_relays = {}

IP = main.IP

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


@app.post("/register_relay")
async def post_register_relay(ip: str, relay_type: str, public_key: str):
    #validate response
    relay = [relay_type, ip, public_key]
    registered_relays[ip] = relay


@app.get("/get_relays", response_class=PlainTextResponse)
async def get_get_relays():
    relay_data = []
    # ip1:public_key1\nip2:public_key2...
    #return '\n'.join(':'.join(i) for i in registered_relays)
    #return str(registered_relays)
    for i in registered_relays:
        relay_data.append(':'.join(registered_relays[i]))
    return '\n'.join(relay_data)
