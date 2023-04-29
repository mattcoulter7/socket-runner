from twisted.internet import protocol
from twisted.internet.address import IAddress

from .protocol import TCPProtocol

class TCPProtocolFactory(protocol.ClientFactory):
    def __init__(self, protocol_config = {}) -> None:
        super().__init__()

        self.protocol = TCPProtocol

        self.protocol_config = protocol_config

    def buildProtocol(self, addr: IAddress):
        protocol = super().buildProtocol(addr)

        protocol.addr = addr

        for k,v in self.protocol_config.items():
            protocol.__setattr__(k, v)

        return protocol