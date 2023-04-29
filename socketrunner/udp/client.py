from twisted.internet import reactor
from twisted.internet.address import IAddress

from .socket import UDPSocketProtocolEnd

class UDPClient(UDPSocketProtocolEnd):
    """Handles sending/receiving all messages over UDP as a client"""

    def __init__(
            self, 
            server_host, 
            server_port, 
            port=0,
            **kwargs
        ) -> None:
        super().__init__(
            server_host=server_host,
            server_port=server_port,
            **kwargs
        )

        self.port = port  # port of the client

    def send(self, data: bytes, addr: IAddress=None):
        addr = addr or self.server_addr
        return super().send(data, addr)

    def start(self):
        reactor.listenUDP(self.port, self.udp_protocol)
        self.udp_protocol.transport.connect(self.server_host, self.server_port)
