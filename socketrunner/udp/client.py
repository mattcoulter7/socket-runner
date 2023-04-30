import logging
from twisted.internet import reactor
from twisted.internet.address import IAddress

from .socket import UDPSocketProtocolEnd

logger = logging.getLogger("socket-runner::UDPClient")


class UDPClient(UDPSocketProtocolEnd):
    """Handles sending/receiving all messages over UDP as a client"""

    def __init__(
            self,
            server_host: str,
            server_port: int,
            port: int = 0,  # the clients port, 0 represents random assignment
            **kwargs) -> None:
        logger.debug(f"Initializing UDPClient to {server_host}:{server_port}")
        super().__init__(
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

        self.port = port  # port of the client

    def start(self):
        logger.info(f"Starting UDPClient to {self.server_host}:{self.server_port}")
        reactor.listenUDP(self.port, self.udp_protocol)
        self.udp_protocol.transport.connect(self.server_host, self.server_port)
        logger.info("Establishing a virtual connection")
        self.on_client_connection(
            self.udp_protocol,
            self.server_addr
        )
