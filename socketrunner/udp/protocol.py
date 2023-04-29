from twisted.internet.protocol import DatagramProtocol
from twisted.internet.address import IPv4Address, IAddress

from ..base.protocol import BaseProtocol

class UDPProtocol(DatagramProtocol, BaseProtocol):
    def send(self, data: bytes, addr: IAddress):
        self.transport.write(data, (addr.host, addr.port))

    def startProtocol(self):
        print("UDP protocol started")

    def datagramReceived(self, data: bytes, addr: tuple):
        addr = IPv4Address("UDP", addr[0], addr[1])  # ensure ipv4 is a consistent format
        self.receive(data, addr)

    def stopProtocol(self):
        print("UDP protocol stopped")