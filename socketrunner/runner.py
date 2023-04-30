import logging

from typing import Callable, List
from twisted.internet import reactor
from twisted.internet.address import IAddress

from .messaging.packet import Packet
from .messaging.messenger import Messenger

from .connection.pool import ClientPool
from .connection.client import Client
from .base import BaseSocketProtocolEnd, BaseProtocol

logger = logging.getLogger("socket-runner::SocketRunner")


class SocketRunner():
    def __init__(
            self,
            ends: List[BaseSocketProtocolEnd],
            client_timeout: float = 30):
        logger.debug("Initializing Socket Runner")
        if len(ends) == 0:
            raise Exception("Must provide at least 1 Socket End to run")
        self.ends = ends
        for end in ends:
            end.on_data_received_callback = self.on_data_received
            end.on_client_connection_callback = self.on_client_connection
            end.on_client_disconnection_callback = self.on_client_disconnection
        self._ends = {p2.protocol: [p for p in self.ends if p.protocol == p2.protocol] for p2 in self.ends}

        self.client_pool = ClientPool(
            timeout=client_timeout
        )

        self.messenger = Messenger()

    def start(self):
        """Start the server // Connect to a server"""
        logger.info("Starting Socket Runner")
        for end in self.ends:
            end.start()

        logger.debug("Starting Twisted Reactor")
        reactor.run()

    def send(
            self,
            data: Packet,
            client: Client = None,
            client_addr: IAddress = None,
            protocol: str = None,
            owner_addr: IAddress = None,):
        """Send a message for a given method"""
        logger.info(f"Sending data via {protocol}")
        data_bytes = data.as_bytes()

        clients: List[Client] = [client] if client else self.client_pool.get_clients(
            owner_host=owner_addr.host if owner_addr else None,
            owner_port=owner_addr.port if owner_addr else None,
            protocol=protocol,
            child_host=client_addr.host if client_addr else None,
            child_port=client_addr.port if client_addr else None,
        )
        if len(clients) == 0:
            logger.warning("Attempting to send data to no recipients")

        logger.debug(f"clients=`{clients}`")
        for client in clients:
            client.owner.send(
                data_bytes,
                client
            )

    def on(self, event: str, callback: Callable) -> None:
        self.messenger.sub(event, callback)

    def on_client_connection(
            self,
            protocol: BaseProtocol,
            addr: IAddress,
            owner: BaseSocketProtocolEnd):
        logger.info("Handling client connection")
        self.client_pool.register_client(
            addr=addr,
            protocol=protocol,
            owner=owner
        )

    def on_client_disconnection(
            self,
            protocol: BaseProtocol,
            addr: IAddress,
            owner: BaseSocketProtocolEnd):
        logger.info("Handling client disconnection")
        self.client_pool.deregister_client(
            addr=addr
        )

    def on_data_received(
            self,
            data: bytes,
            protocol: BaseProtocol,
            addr: IAddress,
            owner: BaseSocketProtocolEnd):
        logger.info("Handling data received")
        packet = Packet.from_bytes(data)
        if packet is None:
            return

        client: Client = self.client_pool.register_client(
            addr=addr,
            owner=owner,
            protocol=protocol
        )

        self.messenger.pub(
            packet.event,
            packet,
            client
        )
