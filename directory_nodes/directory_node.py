from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


#IP = "192.168.10.10"
IP = "127.0.0.1"
PORT = 8000
registered_relays = []

app = FastAPI(
    #debug=True,
    #docs_url=None,
    #redoc_url=None,
    #openapi_url=None,
)


@app.get("/get_relays", response_class=PlainTextResponse)
async def get_directories():
    # ip1:public_key1\nip2:public_key2...
    return '\n'.join(':'.join(i) for i in registered_relays)

#curl -v -X POST 'http://127.0.0.1:8000/register_relay?ip=127.0.0.1'
@app.post("/register_relay")
async def post_register_relay(ip: str):
    #validate response
    registered_relays.append([ip])
