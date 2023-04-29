import logging
from twisted.internet import reactor

from .socket import UDPSocketProtocolEnd

logger = logging.getLogger("socket-runner::UDPServer")


class UDPServer(UDPSocketProtocolEnd):
    """Handles sending/receiving all messages over UDP as a server"""

    def __init__(
            self,
            host: str,
            port: int,
            **kwargs) -> None:
        logger.debug(f"Initializing UDPServer on {host}:{port}")
        super().__init__(
            server_host=host,
            server_port=port,
            **kwargs
        )

    def start(self):
        logger.info(f"Starting UDPServer on {self.server_host}:{self.server_port}")
        reactor.listenUDP(self.server_port, self.udp_protocol, interface=self.server_host)
