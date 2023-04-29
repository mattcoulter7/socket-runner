from twisted.internet import reactor
from twisted.internet.address import IAddress

from .socket import TCPSocketProtocolEnd


class TCPClient(TCPSocketProtocolEnd):
    """Handles sending/receiving all messages over TCP as a client"""

    def __init__(self,
            server_host,
            server_port,
            **kwargs
        ) -> None:
        super().__init__(
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

    def start(self):
        reactor.connectTCP(
            self.server_host, 
            self.server_port, 
            self.factory
        )

    def send(self, data: bytes, addr: IAddress=None):
        addr = addr or self.server_addr
        return super().send(data, addr)
