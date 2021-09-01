"""
IPs for directory nodes: 192.168.10.10, 192.168.10.11
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import main

registered_relays = []
IP = main.IP

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


#curl -v -X POST 'http://127.0.0.1:8000/register_relay?ip=127.0.0.1'
@app.post("/register_relay")
async def post_register_relay(ip: str, relay_type: str):
    #validate response
    registered_relays.append([ip, relay_type])


@app.get("/get_relays", response_class=PlainTextResponse)
async def get_get_relays():
    # ip1:public_key1\nip2:public_key2...
    return '\n'.join(':'.join(i) for i in registered_relays)
