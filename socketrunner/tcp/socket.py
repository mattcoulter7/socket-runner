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
            timeout: float = 30,
            on_connection_callback: Callable[[BaseProtocol, IAddress], None] = None,
            on_disconnection_callback: Callable[[BaseProtocol, IAddress], None] = None,
            **kwargs) -> None:
        logger.debug(f"Initializing TCPSocketProtocolEnd on {server_host}:{server_port}")
        super().__init__(
            protocol="TCP",
            server_host=server_host,
            server_port=server_port,
            timeout=timeout,
            **kwargs
        )

        self.on_connection_callback = on_connection_callback
        self.on_disconnection_callback = on_disconnection_callback

        self.factory = TCPProtocolFactory(
            protocol_config={
                "receive_callback": self._receive,
                "connect_callback": self._on_connection,
                "disconnect_callback": self._on_disconnection,
            }
        )

    def _receive(self, data: bytes, protocol: BaseProtocol, addr: IAddress):
        logger.debug(f"Handling received data from {addr} via TCP")
        self.client_pool.register_client(addr, protocol)
        return super()._receive(data, protocol, addr)

    def _on_connection(self, protocol: BaseProtocol, addr: IAddress):
        logger.debug(f"Handling connection with {addr}")
        self.client_pool.register_client(addr, protocol)
        # Invoke a custom callback
        if self.on_connection_callback is not None:
            self.on_connection_callback(protocol, addr)

    def _on_disconnection(self, protocol: BaseProtocol, addr: IAddress):
        logger.debug(f"Handling disconnection with {addr}")
        self.client_pool.deregister_client(addr)
        # Invoke a custom callback
        if self.on_disconnection_callback is not None:
            logger.debug(f"Forwarding disconnection ")
            self.on_disconnection_callback(protocol, addr)
