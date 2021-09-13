class Client:
    def __init__(self, ip, public_key, symmetric_key, next_server):
        self.ip = ip
        self.public_key = public_key
        self.symmetric_key = symmetric_key
        self.next_server = next_server

class Relay(Client):
    def __init__(self, ip, public_key, symmetric_key, next_server, relay_type):
            super().__init__(ip, public_key, symmetric_key, next_server)
            self.relay_type = relay_type
