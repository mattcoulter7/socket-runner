import time
import os

from dotenv import load_dotenv
from twisted.internet import reactor

from socketrunner import ManagedRunner
from socketrunner.messaging import Packet
from socketrunner.tcp import TCPClient
from socketrunner.udp import UDPClient

load_dotenv()
runner = ManagedRunner(
    TCPClient(
        server_host=os.getenv("tcp_host"),
        server_port=int(os.getenv("tcp_port"))
    ),
    UDPClient(
        server_host=os.getenv("udp_host"),
        server_port=int(os.getenv("udp_port"))
    )
)


def ping():
    for protocol in ["TCP"]:
        message = Packet(
            "ping",
            time=time.time_ns()
        )
        runner.send(
            message,
            protocol=protocol
        )
        reactor.callLater(1, ping)


def on_pong(data: Packet, sender):
    print(f'{data} from {sender}')
    send_time = data.data["time"]
    receive_time = time.time_ns()

    ping_ms = round((receive_time - send_time) / 1000000)
    print(f"Ping: {ping_ms}ms")


def on_data(data: Packet, sender):
    print(f'{data} from {sender}')


if __name__ == "__main__":
    runner.on("pong", on_pong)
    runner.on("data", on_data)
    reactor.callLater(1, ping)
    runner.start()
