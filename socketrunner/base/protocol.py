import logging
from typing import Callable
from twisted.internet.address import IAddress

logger = logging.getLogger("socket-runner::BaseProtocol")


class BaseProtocol():
    addr: IAddress = None
    on_data_received_callback: Callable[[bytes, object, IAddress], None] = None
    on_client_connection_callback: Callable[[object, IAddress], None] = None
    on_client_disconnection_callback: Callable[[object, IAddress], None] = None

    def send(self, data: bytes, **kwargs):
        raise NotImplementedError()

    def receive(self, data: bytes, addr: IAddress = None):
        addr = addr or self.addr
        logger.debug(f"Receiving Data from {addr}")
        logger.debug(f"data=`{data}`")
        if addr is not None and self.on_data_received_callback is not None:
            logger.debug(f"Forwarding data to `{self.on_data_received_callback}`")
            self.on_data_received_callback(data, self, addr)

    def connect(self):
        if self.addr is not None and self.on_client_connection_callback is not None:
            logger.debug(f"Forwarding connection to `{self.on_client_connection_callback}`")
            self.on_client_connection_callback(self, self.addr)

    def disconnect(self):
        if self.addr is not None and self.on_client_disconnection_callback is not None:
            logger.debug(f"Forwarding disconnection to `{self.on_client_disconnection_callback}`")
            self.on_client_disconnection_callback(self, self.addr)
