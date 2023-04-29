from twisted.internet.address import IAddress

from ..base.protocol import BaseProtocol
from ..base.socket import BaseSocketProtocolEnd
from .protocol import UDPProtocol

class UDPSocketProtocolEnd(BaseSocketProtocolEnd):
    def __init__(
            self,
            server_host:str,
            server_port:int,
            timeout:float=30,
            **kwargs
        ) -> None:
        super().__init__(
            protocol="UDP",
            server_host=server_host,
            server_port=server_port,
            timeout=timeout,
            **kwargs
        )

        self.udp_protocol = UDPProtocol()
        self.udp_protocol.receive_callback = self._receive

    def send(self, data: bytes, addr: IAddress):
        # We don't need to check for client as connections aren't maintained in UDP
        self.udp_protocol.send(
            data=data,
            addr=addr
        )

    def _receive(self, data: bytes, protocol: BaseProtocol, addr: IAddress):
        # client pool on receive message simply for keeping track of past connections
        self.client_pool.register_client(addr, protocol)
        return super()._receive(data, protocol, addr)
