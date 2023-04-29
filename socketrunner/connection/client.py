import time
import logging

logger = logging.getLogger("socket-runner::Client")


class Client():
    def __init__(
            self,
            protocol,
            addr) -> None:
        logger.debug(f"Initializing Client {addr}")
        self.protocol = protocol
        self.addr = addr
        self.registered_time = time.time()
        self.reregistered_time = time.time()
        self.expiry_time = time.time()

    def reregister(self, timeout):
        logger.debug(f"Reregistering Client `{self.addr}` with timeout=`{timeout}`")
        self.reregistered_time = time.time()
        self.expiry_time = time.time() + timeout
