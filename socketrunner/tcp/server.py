import logging
from twisted.internet import reactor

from .socket import TCPSocketProtocolEnd

logger = logging.getLogger("socket-runner::TCPServer")


class TCPServer(TCPSocketProtocolEnd):
    """Handles sending/receiving all messages over TCP as a server"""

    def __init__(
            self,
            host: str,
            port: int,
            **kwargs) -> None:
        logger.debug(f"Initializing TCPServer on {host}:{port}")
        super().__init__(
            server_host=host,
            server_port=port,
            **kwargs
        )

    def start(self):
        logger.info(f"Starting TCPServer on {self.server_host}:{self.server_port}")
        reactor.listenTCP(
            self.server_port,
            self.factory,
            interface=self.server_host
        )
