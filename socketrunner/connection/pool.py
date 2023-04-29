import threading
import time
import logging

from twisted.internet.address import IAddress

from .client import Client

logger = logging.getLogger("socket-runner::ClientPool")


class ClientPool():
    def __init__(self, timeout: float) -> None:
        logger.debug(f"Initializing ClientPool with timeout=`{timeout}`")
        self.clients = {}
        self.lock = threading.Lock()
        self.cleaner_thread = threading.Thread(target=self._clean_expired_clients)
        self.cleaner_thread.daemon = True
        self.cleaner_thread.start()

        self.timeout = timeout

    def register_client(self, addr: IAddress, protocol):
        logger.debug(f"Registering Client {addr}")
        with self.lock:
            client_id = self._get_address_id(addr)
            if client_id not in self.clients:
                self.clients[client_id] = Client(
                    protocol=protocol,
                    addr=addr
                )

            self.clients[client_id].reregister(self.timeout)

    def deregister_client(self, addr: IAddress):
        logger.debug(f"Deregistering Client {addr}")
        with self.lock:
            client_id = self._get_address_id(addr)
            if client_id in self.clients:
                del self.clients[client_id]

    def get_client(self, addr: IAddress) -> Client:
        logger.debug(f"Getting Client {addr}")
        with self.lock:
            client_id = self._get_address_id(addr)
            if client_id in self.clients:
                return self.clients[client_id]

            logger.debug(f"Client {addr} not found")
            return None

    def get_clients(self):
        logger.debug(f"Getting Clients")
        with self.lock:
            return self.clients.values()

    def _clean_expired_clients(self):
        while True:
            logger.debug(f"Check for any clients to expire")
            current_time = time.time()
            clients_to_remove = []

            with self.lock:
                for client_id, client in self.clients.items():
                    if current_time > client.expiry_time:
                        clients_to_remove.append(client_id)

                for client_to_remove in clients_to_remove:
                    logger.warning(f"Client `{client_to_remove}` has expired")
                    del self.clients[client_to_remove]

            time.sleep(5)  # Check for expired clients every few seconds

    def _get_address_id(self, addr: IAddress):
        return f"{addr.type}::{addr.host}::{addr.port}"
