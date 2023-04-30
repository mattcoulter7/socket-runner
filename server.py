import os
import logging

from dotenv import load_dotenv

from socketrunner import SocketRunner
from socketrunner.messaging import Packet
from socketrunner.tcp import TCPServer
from socketrunner.udp import UDPServer
from socketrunner.connection.client import Client
from socketrunner.utils import parse_ports

load_dotenv()
logging.basicConfig(level=logging.INFO)

TCP_HOST = os.getenv("tcp_host")
TCP_PORTS = parse_ports(os.getenv("tcp_port"))
UDP_HOST = os.getenv("udp_host")
UDP_PORTS = parse_ports(os.getenv("udp_port"))

runner = SocketRunner(
    ends=[
        *[
            TCPServer(
                host=TCP_HOST,
                port=port
            ) for port in TCP_PORTS
        ],
        *[
            UDPServer(
                host=TCP_HOST,
                port=port
            ) for port in UDP_PORTS
        ]
    ]
)


def share(data: Packet, sender: Client):
    print(f'{data} from {sender}')
    runner.send(
        data=data,
        owner_addr=sender.owner.server_addr
    )


def pong(data: Packet, sender: Client):
    print(f'{data} from {sender}')
    message = Packet(
        event="pong",
        **data.data
    )
    runner.send(
        data=message,
        client=sender
    )


if __name__ == "__main__":
    runner.on("ping", pong)
    runner.on("data", share)
    runner.start()
