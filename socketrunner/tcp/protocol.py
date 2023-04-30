import logging
from twisted.internet import protocol

from ..base import BaseProtocol

logger = logging.getLogger("socket-runner::TCPProtocol")


class TCPProtocol(protocol.Protocol, BaseProtocol):
    connect_callback = None
    disconnect_callback = None

    def send(self, data: bytes, **kwargs):
        logger.info("Sending data via TCP")
        logger.debug(f"data=`{data}`")
        self.transport.write(data)

    def connectionMade(self):
        logger.info("TCP connection made")
        self.connect()

    def dataReceived(self, data: bytes):
        logger.info("Receiving data via TCP")
        self.receive(data)

    def connectionLost(self, reason):
        logger.warning(f"TCP connection lost due to reason=`{reason}`")
        self.disconnect()
