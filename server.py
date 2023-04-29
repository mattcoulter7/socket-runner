import os
import socket
import logging

from dotenv import load_dotenv

from socketrunner import ManagedRunner
from socketrunner.messaging import Packet
from socketrunner.tcp import TCPServer
from socketrunner.udp import UDPServer

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

TCP_HOST = os.getenv("tcp_host")
TCP_PORT = int(os.getenv("tcp_port"))
UDP_HOST = os.getenv("udp_host")
UDP_PORT = int(os.getenv("udp_port"))

TCP_HOST = socket.gethostbyname(TCP_HOST)
UDP_HOST = socket.gethostbyname(UDP_HOST)

runner = ManagedRunner(
    TCPServer(
        host=TCP_HOST,
        port=TCP_PORT
    ),
    UDPServer(
        host=UDP_HOST,
        port=UDP_PORT
    )
)


def share(data: Packet, sender):
    print(f'{data} from {sender}')
    runner.broadcast(
        data=data,
        protocol=sender.type
    )


def pong(data: Packet, sender):
    print(f'{data} from {sender}')
    message = Packet(
        event="pong",
        **data.data
    )
    runner.send(
        data=message,
        protocol=sender.type,
        addr=sender
    )


if __name__ == "__main__":
    runner.on("ping", pong)
    runner.on("data", share)
    runner.start()
