# For license and copyright information please see the LEGAL file in the code repository

import hmac
from os import getpid
from secrets import token_bytes
from threading import Lock

from .errors.generation import (
    Identifier_Error_InvalidGeneratorInput,
    Identifier_Error_EntropyUnavailable,
    Identifier_Error_ClockRollback,
    Identifier_Error_GenerationExhausted,
    Identifier_Error_GeneratorSessionUnverified,
)

MAXIMUM = (1 << 64) - 1
DOMAIN = b"memar/identifier/session-seed\x00"


class CandidateGenerator:
    __slots__ = (
        "_anchor", "_max_rollback", "_max_per_tick", "_session", "_session_token",
        "_invalid", "_lock", "_reservation",
    )

    def __init__(self, *, max_rollback_ticks, max_per_tick, source=b"", entropy=token_bytes, session=getpid):
        if type(max_rollback_ticks) is not int or not 0 <= max_rollback_ticks <= MAXIMUM:
            raise Identifier_Error_InvalidGeneratorInput()
        if type(max_per_tick) is not int or not 1 <= max_per_tick <= MAXIMUM:
            raise Identifier_Error_InvalidGeneratorInput()
        if type(source) is not bytes or len(source) not in (0, 16):
            raise Identifier_Error_InvalidGeneratorInput()
        if not callable(entropy) or not callable(session):
            raise Identifier_Error_InvalidGeneratorInput()
        self._max_rollback = max_rollback_ticks
        self._max_per_tick = max_per_tick
        self._session = session
        self._invalid = False
        self._session_token = self._read_session()
        try:
            key = entropy(32)
        except Exception as error:
            raise Identifier_Error_EntropyUnavailable() from error
        if type(key) is not bytes or len(key) != 32:
            raise Identifier_Error_EntropyUnavailable()
        transcript = DOMAIN + bytes((len(source),)) + source
        self._anchor = int.from_bytes(hmac.digest(key, transcript, "sha256")[:8], "big")
        self._check_session()
        self._lock = Lock()
        self._reservation = None

    def _read_session(self):
        try:
            token = self._session()
        except Exception as error:
            self._invalid = True
            raise Identifier_Error_GeneratorSessionUnverified() from error
        if type(token) is not int or token <= 0:
            self._invalid = True
            raise Identifier_Error_GeneratorSessionUnverified()
        return token

    def _check_session(self):
        if self._invalid:
            raise Identifier_Error_GeneratorSessionUnverified()
        if self._read_session() != self._session_token:
            self._invalid = True
            raise Identifier_Error_GeneratorSessionUnverified()
        if self._invalid:
            raise Identifier_Error_GeneratorSessionUnverified()

    def generate(self, observed_tick):
        self._check_session()
        if type(observed_tick) is not int or not 0 <= observed_tick <= MAXIMUM:
            raise Identifier_Error_InvalidGeneratorInput()
        with self._lock:
            self._check_session()
            previous = self._reservation
            if previous is None or observed_tick > previous[0]:
                tick, tail, count = observed_tick, self._anchor, 1
            else:
                tick, tail, count = previous
                if tick - observed_tick > self._max_rollback:
                    raise Identifier_Error_ClockRollback()
                if count == self._max_per_tick or tail == MAXIMUM:
                    raise Identifier_Error_GenerationExhausted()
                tail += 1
                count += 1
            self._check_session()
            self._reservation = (tick, tail, count)
            return (tick << 64) | tail
