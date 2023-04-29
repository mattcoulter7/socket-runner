import logging
from twisted.internet import protocol
from twisted.internet.address import IAddress

from .protocol import TCPProtocol

logger = logging.getLogger("socket-runner::TCPProtocolFactory")


class TCPProtocolFactory(protocol.ClientFactory):
    def __init__(
            self,
            protocol_config: dict = {}) -> None:
        logger.debug(f"Initializing TCPProtocolFactory with config=`{protocol_config}`")
        super().__init__()

        self.protocol = TCPProtocol

        self.protocol_config = protocol_config

    def buildProtocol(self, addr: IAddress):
        logger.info(f"Building a new TCPProtocol for {addr}")
        protocol = super().buildProtocol(addr)

        protocol.addr = addr

        for k, v in self.protocol_config.items():
            protocol.__setattr__(k, v)

        return protocol
