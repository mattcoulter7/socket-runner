import logging
from twisted.internet.address import IAddress

from ..base.protocol import BaseProtocol
from ..base.socket import BaseSocketProtocolEnd
from .protocol import UDPProtocol
from ..connection.client import Client

logger = logging.getLogger("socket-runner::UDPSocketProtocolEnd")


class UDPSocketProtocolEnd(BaseSocketProtocolEnd):
    def __init__(
            self,
            server_host: str,
            server_port: int,
            **kwargs) -> None:
        logger.debug(f"Initializing UDPSocketProtocolEnd on {server_host}:{server_port}")
        super().__init__(
            protocol="UDP",
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

        self.udp_protocol = UDPProtocol()
        self.udp_protocol.on_data_received_callback = self.on_data_received
