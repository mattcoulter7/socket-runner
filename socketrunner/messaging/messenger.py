from typing import Callable

from .packet import Packet


class Messenger(object):
    def __init__(self) -> None:
        self.subs = {}

    def pub(self, event: str, *args, **kwargs):
        if event in self.subs:
            for callback in self.subs[event]:
                callback(*args, **kwargs)

    def sub(self, event: str, callback: Callable):
        if event in self.subs:
            self.subs[event].append(callback)
        else:
            self.subs[event] = [callback]
