from twisted.internet import reactor

from .socket import UDPSocketProtocolEnd

class UDPServer(UDPSocketProtocolEnd):
    """Handles sending/receiving all messages over UDP as a server"""

    def __init__(
            self, 
            host, 
            port,
            **kwargs
        ) -> None:
        super().__init__(
            server_host=host, 
            server_port=port,
            **kwargs
        )

    def start(self):
        reactor.listenUDP(self.server_port, self.udp_protocol, interface=self.server_host)
