import time
import os
import logging

from dotenv import load_dotenv
from twisted.internet import reactor

from socketrunner import SocketRunner
from socketrunner.messaging import Packet
from socketrunner.tcp import TCPClient
from socketrunner.udp import UDPClient
from socketrunner.connection.client import Client
from socketrunner.utils import parse_ports

logger = logging.getLogger()
load_dotenv()
logging.basicConfig(level=logging.DEBUG)

TCP_HOST = os.getenv("tcp_host")
TCP_PORTS = parse_ports(os.getenv("tcp_port"))
UDP_HOST = os.getenv("udp_host")
UDP_PORTS = parse_ports(os.getenv("udp_port"))

runner = SocketRunner(
    ends=[
        *[
            TCPClient(
                server_host=TCP_HOST,
                server_port=port
            ) for port in TCP_PORTS
        ],
        *[
            UDPClient(
                server_host=TCP_HOST,
                server_port=port
            ) for port in UDP_PORTS
        ]
    ]
)


def share_position():
    runner.send(
        data=Packet(
            "global",
            time=time.time_ns(),
            position=[5, 3, 2]
        ),
        protocol="UDP"
    )
    reactor.callLater(1, ping)


def ping():
    runner.send(
        data=Packet(
            "ping",
            time=time.time_ns()
        )
    )
    reactor.callLater(1, ping)


def on_pong(data: Packet, sender: Client):
    logger.info(f'{data} from {sender}')
    send_time = data.data["time"]
    receive_time = time.time_ns()

    ping_ms = round((receive_time - send_time) / 1000000)
    logger.info(f"Ping: {ping_ms}ms")


def on_data(data: Packet, sender: Client):
    logger.info(f'{data} from {sender}')


if __name__ == "__main__":
    runner.on("pong", on_pong)
    runner.on("data", on_data)
    reactor.callLater(1, ping)
    reactor.callLater(1, share_position)
    runner.start()
