from twisted.internet.address import IAddress


class BaseProtocol():
    addr: IAddress = None
    receive_callback = None
    
    def send(self, data: bytes, **kwargs):
        raise NotImplementedError()

    def receive(self, data: bytes, addr: IAddress=None):
        addr = addr or self.addr
        if addr is not None and self.receive_callback is not None:
            self.receive_callback(data, self, addr)