import time

class Client():
    def __init__(
            self, 
            protocol, 
            addr
        ) -> None:
        self.protocol = protocol
        self.addr = addr
        self.registered_time = time.time()
        self.reregistered_time = time.time()
        self.expiry_time = time.time()

    def reregister(self, timeout):
        self.reregistered_time = time.time()
        self.expiry_time = time.time() + timeout
