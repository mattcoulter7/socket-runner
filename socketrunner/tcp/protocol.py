from twisted.internet import protocol

from ..base import BaseProtocol

class TCPProtocol(protocol.Protocol, BaseProtocol):
    connect_callback = None
    disconnect_callback = None

    def send(self, data: bytes, **kwargs):
        self.transport.write(data)

    def connectionMade(self):
        print("TCP connection made")
        self.connect()

    def dataReceived(self, data: bytes):
        self.receive(data)

    def connectionLost(self, reason):
        print("TCP connection lost:", reason)
        self.disconnect()

    def connect(self):
        if self.addr is not None and self.connect_callback is not None:
            self.connect_callback(self, self.addr)

    def disconnect(self):
        if self.addr is not None and self.disconnect_callback is not None:
            self.disconnect_callback(self, self.addr)
