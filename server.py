import os

from dotenv import load_dotenv
from twisted.internet import reactor

from socketrunner import ManagedRunner
from socketrunner.messaging import Packet
from socketrunner.tcp import TCPServer
from socketrunner.udp import UDPServer

load_dotenv()
runner = ManagedRunner(
    TCPServer(
        host=os.getenv("tcp_host"),
        port=int(os.getenv("tcp_port"))
    ),
    UDPServer(
        host=os.getenv("udp_host"),
        port=int(os.getenv("udp_port"))
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
