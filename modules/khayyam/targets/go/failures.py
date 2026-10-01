"""The two failures this tool raises: a source that will not scan, and a run that
has a reason to refuse. A refusal carries every reason it found, in the order it
found them and without repeats, so one run reports all of them."""

from typing import Iterable


class BridgeFailure(Exception):
    def __init__(self, messages: Iterable[str]):
        self.messages = list(dict.fromkeys(str(message) for message in messages))
        super().__init__("\n".join(self.messages))


class SourceFailure(Exception):
    pass
