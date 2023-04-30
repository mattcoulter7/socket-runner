import logging
from twisted.internet import reactor
from twisted.internet.address import IAddress

from .socket import TCPSocketProtocolEnd

logger = logging.getLogger("socket-runner::TCPClient")


class TCPClient(TCPSocketProtocolEnd):
    """Handles sending/receiving all messages over TCP as a client"""

    def __init__(
            self,
            server_host: str,
            server_port: int,
            **kwargs) -> None:
        logger.debug(f"Initializing TCPClient to {server_host}:{server_port}")
        super().__init__(
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

    def start(self):
        logger.info(f"Starting TCPClient to {self.server_host}:{self.server_port}")
        reactor.connectTCP(
            self.server_host,
            self.server_port,
            self.factory
        )
