import logging
from typing import Callable
from twisted.internet.address import IAddress

logger = logging.getLogger("socket-runner::BaseProtocol")


class BaseProtocol():
    addr: IAddress = None
    receive_callback: Callable[[bytes, any, IAddress], None] = None

    def send(self, data: bytes, **kwargs):
        raise NotImplementedError()

    def receive(self, data: bytes, addr: IAddress = None):
        addr = addr or self.addr
        logger.debug(f"Receiving Data from {addr}")
        logger.debug(f"data=`{data}`")
        if addr is not None and self.receive_callback is not None:
            logger.debug(f"Forwarding data to `{self.receive_callback}`")
            self.receive_callback(data, self, addr)
