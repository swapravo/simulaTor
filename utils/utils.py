from msgpack import packb, unpackb
from base64 import b64encode, b64decode


class Client:
    def __init__(self, public_key, symmetric_key, ip=None, next_server=None):
        self.public_key = public_key
        self.symmetric_key = symmetric_key
        self.ip = ip
        self.next_server = next_server

    def display(self):
        print()
        print("IP: ", self.ip)
        print("Public Key: ", self.public_key)
        print("Symmetric Key: ", self.symmetric_key)
        print("Next Server: ", self.next_server)

    def __eq__(self, other):
        return self.ip == other.ip and self.public_key == other.public_key and self.symmetric_key == other.symmetric_key and self.next_server == other.next_server


class Relay(Client):
    def __init__(self, ip, public_key, symmetric_key, relay_type, next_server=None):
            super().__init__(public_key, symmetric_key, ip, next_server)
            if relay_type in ['guard', 'middle', 'exit']:
                self.relay_type = relay_type
            else:
                raise ValueError

    def display(self):
        super().display()
        print("Relay Type: ", self.relay_type)

    #TODO FIX THIS
    def __eq__(self, other):
        return self.ip == other.ip and self.public_key == other.public_key and self.symmetric_key == other.symmetric_key and self.next_server == other.next_server and self.relay_type == other.relay_type


def serialise(message):
	return packb(message, use_bin_type=True)

def deserialise(message):
	try:
		return unpackb(message, raw=False)
	except:
		return b''


def encode(data: bytes) -> str:
    return b64encode(data)

def decode(data: str) -> bytes:
    return b64decode(data)
