import json


class Packet(object):
    def __init__(self, event: str, **data) -> None:
        self.event = event
        self.data = data

    def as_bytes(self) -> bytes:
        return json.dumps({
            "event": self.event,
            **self.data
        }).encode()

    @staticmethod
    def from_bytes(data: bytes):
        try:
            json_data = json.loads(data.decode())
        except Exception as e:
            return None
        
        return Packet(
            **json_data
        )
