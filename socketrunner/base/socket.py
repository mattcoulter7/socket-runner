import logging
import socket
from typing import Callable
from twisted.internet.address import IPv4Address, IAddress

from .protocol import BaseProtocol
from ..connection.pool import ClientPool

logger = logging.getLogger("socket-runner::BaseSocketProtocolEnd")


class BaseSocketProtocolEnd():
    def __init__(
            self,
            protocol: str,
            server_host: str,
            server_port: int,
            receive_callback: Callable[[bytes, IAddress], None] = None,
            timeout: float = 30) -> None:
        logger.debug(f"Initializing BaseSocketProtocolEnd on {server_host}:{server_port} using protocol=`{protocol}`")
        self.protocol = protocol  # serve host
        self.server_host = socket.gethostbyname(server_host)  # serve host
        self.server_port = server_port  # serve host

        self.receive_callback = receive_callback

        self.client_pool = ClientPool(
            timeout=timeout
        )

    def start(self):
        raise NotImplementedError()

    def send(self, data: bytes, addr: IAddress):
        logger.info(f"Sending data to {addr} via {self.protocol}")
        logger.debug(f"data=`{data}`")
        client = self.client_pool.get_client(addr)
        if client is None:
            raise Exception(f"Connection not established with {addr}")

        client.protocol.send(
            data=data,
            addr=client.addr
        )

    def broadcast(self, data: bytes):
        logger.info(f"Broadcasting data via {self.protocol}")
        logger.debug(f"data=`{data}`")
        clients = self.client_pool.get_clients()
        for client in clients:
            logger.debug(f"Sending data to addr={client.addr} via {self.protocol}")
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

    def _receive(self, data: bytes, protocol: BaseProtocol, addr: IAddress):
        logger.info(f"Data received from {addr} via {self.protocol}")
        logger.debug(f"data=`{data}`")
        if self.receive_callback is not None:
            logger.debug(f"Forwarding data to `{self.receive_callback}`")
            self.receive_callback(data, addr)
