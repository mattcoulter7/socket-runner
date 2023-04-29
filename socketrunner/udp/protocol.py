import logging
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.address import IPv4Address, IAddress

from ..base.protocol import BaseProtocol

logger = logging.getLogger("socket-runner::UDPProtocol")


class UDPProtocol(DatagramProtocol, BaseProtocol):
    def send(self, data: bytes, addr: IAddress):
        logger.info("Sending data via UDP")
        self.transport.write(data, (addr.host, addr.port))

    def startProtocol(self):
        logger.info("UDP (virtual) connection made")

    def datagramReceived(self, data: bytes, addr: tuple):
        addr = IPv4Address("UDP", addr[0], addr[1])  # ensure ipv4 is a consistent format
        logger.info("Receiving data via UDP")
        self.receive(data, addr)

    def stopProtocol(self):
        logger.warning("UDP (virtual) protocol stopped")
