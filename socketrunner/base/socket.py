import logging
import socket
from typing import Callable
from twisted.internet.address import IPv4Address, IAddress

from .protocol import BaseProtocol
from ..connection.pool import ClientPool, Client

logger = logging.getLogger("socket-runner::BaseSocketProtocolEnd")


class BaseSocketProtocolEnd():
    on_data_received_callback: Callable[[bytes, BaseProtocol, IAddress, object], None] = None
    on_client_connection_callback: Callable[[BaseProtocol, IAddress, object], None] = None
    on_client_disconnection_callback: Callable[[BaseProtocol, IAddress, object], None] = None

    def __init__(
            self,
            protocol: str,
            server_host: str,
            server_port: int) -> None:
        logger.debug(f"Initializing BaseSocketProtocolEnd on {server_host}:{server_port} using protocol=`{protocol}`")
        self.protocol = protocol  # serve host
        self.server_host = socket.gethostbyname(server_host)  # serve host
        self.server_port = server_port  # serve host

    def start(self):
        raise NotImplementedError()

    def send(self, data: bytes, client: Client):
        logger.info(f"Sending data to {client.addr} via {self.protocol}")
        logger.debug(f"data=`{data}`")

        client.protocol.send(
            data=data,
            addr=client.addr
        )

    @property
    def server_addr(self):
        return IPv4Address(
            self.protocol,
            self.server_host,
            self.server_port
        )

    def on_data_received(self, data: bytes, protocol: BaseProtocol, addr: IAddress):
        if self.on_data_received_callback is not None:
            logger.debug(f"Forwarding data to `{self.on_data_received_callback}`")
            self.on_data_received_callback(data, protocol, addr, self)

    def on_client_connection(self, protocol: BaseProtocol, addr: IAddress):
        if self.on_client_connection_callback is not None:
            logger.debug(f"Forwarding connection to `{self.on_client_connection_callback}`")
            self.on_client_connection_callback(protocol, addr, self)

    def on_client_disconnection(self, protocol: BaseProtocol, addr: IAddress):
        if self.on_client_disconnection_callback is not None:
            logger.debug(f"Forwarding disconnection to `{self.on_client_disconnection_callback}`")
            self.on_client_disconnection_callback(protocol, addr, self)
