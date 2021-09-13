
class Client:
    def __init__(self, ip, public_key, symmetric_key, next_server = None):
        self.ip = ip
        self.public_key = public_key
        self.symmetric_key = symmetric_key
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
    def __init__(self, ip, public_key, symmetric_key, next_server, relay_type):
            super().__init__(ip, public_key, symmetric_key, next_server)
            self.relay_type = relay_type

    def display(self):
        super().display()
        print(self.relay_type)

    #TODO FIX THIS
    def __eq__(self, other):
        return self.ip == other.ip and self.public_key == other.public_key and self.symmetric_key == other.symmetric_key and self.next_server == other.next_server and self.relay_type == other.relay_type


r = Relay(ip="ip", public_key="pk", symmetric_key="sym", next_server="nxt", relay_type="Rel")
r.display()