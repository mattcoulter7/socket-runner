from twisted.internet.address import IAddress

from .factory import TCPProtocolFactory
from ..base.protocol import BaseProtocol
from ..base.socket import BaseSocketProtocolEnd


class TCPSocketProtocolEnd(BaseSocketProtocolEnd):
    def __init__(
            self, 
            server_host:str, 
            server_port:int,
            timeout:float=30,
            on_connection_callback=None,
            on_disconnection_callback=None,
            **kwargs,
        ) -> None:
        super().__init__(
            protocol="TCP",
            server_host=server_host, 
            server_port=server_port,
            timeout=timeout,
            **kwargs
        )
        
        self.on_connection_callback = on_connection_callback
        self.on_disconnection_callback = on_disconnection_callback
        
        self.factory = TCPProtocolFactory(
            protocol_config={
                "receive_callback": self._receive,
                "connect_callback": self._on_connection,
                "disconnect_callback": self._on_disconnection,
            }
        )

    def _receive(self, data: bytes, protocol: BaseProtocol, addr: IAddress):
        self.client_pool.register_client(addr, protocol)
        return super()._receive(data, protocol, addr)

    def _on_connection(self, protocol: BaseProtocol, addr: IAddress):
        self.client_pool.register_client(addr, protocol)
        # Invoke a custom callback
        if self.on_connection_callback is not None:
            self.on_connection_callback(protocol, addr)
    
    def _on_disconnection(self, protocol: BaseProtocol, addr: IAddress):
        self.client_pool.deregister_client(addr)
        # Invoke a custom callback
        if self.on_disconnection_callback is not None:
            self.on_disconnection_callback(protocol, addr)