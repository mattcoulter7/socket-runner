from twisted.internet.address import IPv4Address, IAddress

from .protocol import BaseProtocol
from ..connection.pool import ClientPool


class BaseSocketProtocolEnd():
    def __init__(
            self,
            protocol,
            server_host,
            server_port,
            receive_callback=None,
            timeout: float = 30) -> None:
        self.protocol = protocol  # serve host
        self.server_host = server_host  # serve host
        self.server_port = server_port  # serve host

        self.receive_callback = receive_callback

        self.client_pool = ClientPool(
            timeout=timeout
        )

    def start(self):
        raise NotImplementedError()

    def send(self, data: bytes, addr: IAddress):
        client = self.client_pool.get_client(addr)
        if client is None:
            raise Exception(f"Connection not established with {addr}")

        client.protocol.send(
            data=data,
            addr=client.addr
        )

    def broadcast(self, data: bytes):
        clients = self.client_pool.get_clients()
        for client in clients:
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
        if self.receive_callback is not None:
            self.receive_callback(data, addr)
