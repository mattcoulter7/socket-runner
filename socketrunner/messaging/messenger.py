import logging
from typing import Callable

from .packet import Packet

logger = logging.getLogger("socket-runner::Messenger")


class Messenger(object):
    def __init__(self) -> None:
        logger.debug("Initializing Messenger")
        self.subs = {}

    def pub(self, event: str, *args, **kwargs):
        logger.debug(f"Publishing Event `{event}`")
        if event in self.subs:
            for callback in self.subs[event]:
                logger.debug(f"Invoking callback `{callback}`")
                callback(*args, **kwargs)

    def sub(self, event: str, callback: Callable):
        logger.debug(f"Subscribing Event `{event}` to callback=`{callback}`")
        if event in self.subs:
            self.subs[event].append(callback)
        else:
            self.subs[event] = [callback]
