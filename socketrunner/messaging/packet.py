import logging
import json

logger = logging.getLogger("socket-runner::Packet")


class Packet(object):
    def __init__(self, event: str, **data) -> None:
        logger.debug("Initializing Packet")

        logger.debug(f"event=`{event}`")
        self.event = event

        logger.debug(f"data=`{data}`")
        self.data = data

    def as_bytes(self) -> bytes:
        logger.debug("Converting packet to bytes")
        return json.dumps({
            "event": self.event,
            **self.data
        }).encode()

    @staticmethod
    def from_bytes(data: bytes):
        logger.debug("Converting bytes to packet")
        try:
            json_data = json.loads(data.decode())
        except Exception as e:
            logger.warning(f"Failure during parsing of data. Skipping...")
            return None

        return Packet(
            **json_data
        )
