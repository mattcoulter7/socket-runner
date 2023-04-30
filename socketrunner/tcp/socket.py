import logging
from twisted.internet.address import IAddress
from typing import Callable

from .factory import TCPProtocolFactory
from ..base.protocol import BaseProtocol
from ..base.socket import BaseSocketProtocolEnd

logger = logging.getLogger("socket-runner::TCPSocketProtocolEnd")


class TCPSocketProtocolEnd(BaseSocketProtocolEnd):
    def __init__(
            self,
            server_host: str,
            server_port: int,
            **kwargs) -> None:
        logger.debug(f"Initializing TCPSocketProtocolEnd on {server_host}:{server_port}")
        super().__init__(
            protocol="TCP",
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

        self.factory = TCPProtocolFactory(
            protocol_config={
                "on_data_received_callback": self.on_data_received,
                "on_client_connection_callback": self.on_client_connection,
                "on_client_disconnection_callback": self.on_client_disconnection,
            }
        )
