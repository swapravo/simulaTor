import nacl.utils
from nacl.public import PrivateKey, Box, SealedBox, PublicKey
from nacl.secret import SecretBox #  xsalsa20poly1305
from nacl.utils import random as nacl_random
from base64 import b64encode, b64decode


def generate_asymmetric_keys():
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    return (public_key, private_key)

def generate_shared_secret(private_key_1, public_key_2):
    b = Box(private_key_1, public_key_2)
    return b.shared_key()


def encode_public_key(key):
    return b64encode(bytes(key))

def decode_public_key(key):
    return PublicKey(b64decode(key))


def encrypt(key: bytes, message: bytes):
    box = SecretBox(key)
    return box.encrypt(message, nacl_random(SecretBox.NONCE_SIZE))

def decrypt(key: bytes, message: bytes):
	try:
	    box = SecretBox(key)
	    return box.decrypt(message)
	except:
	    return b''
