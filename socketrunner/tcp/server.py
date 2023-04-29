from twisted.internet import reactor

from .socket import TCPSocketProtocolEnd

class TCPServer(TCPSocketProtocolEnd):
    """Handles sending/receiving all messages over TCP as a server"""

    def __init__(self,
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
        reactor.listenTCP(
            self.server_port,
            self.factory, 
            interface=self.server_host
        )
