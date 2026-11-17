# For license and copyright information please see the LEGAL file in the code repository

from threading import Lock
from .time_coordinate import coordinate_from_time
from .errors.generation import Identifier_Error_InvalidGeneratorInput
from .errors.already_initialized import Identifier_Error_AlreadyInitialized
from .errors.not_initialized import Identifier_Error_NotInitialized
from .errors.invalid_value import Identifier_Error_InvalidValue

MAXIMUM = (1 << 128) - 1


class IdentifierValue:
    __slots__ = ("_mint", "_time_view", "_reference_epoch", "_snapshot", "_lock")

    def __init__(self, mint, time_view, reference_epoch):
        if not callable(mint) or not callable(time_view):
            raise Identifier_Error_InvalidGeneratorInput()
        self._mint = mint
        self._time_view = time_view
        self._reference_epoch = reference_epoch
        self._snapshot = None
        self._lock = Lock()

    def is_empty(self):
        with self._lock:
            return self._snapshot is None

    def _publish(self, value):
        if type(value) is not int or not 0 <= value <= MAXIMUM:
            raise Identifier_Error_InvalidValue()
        coordinate = value >> 64
        view = self._time_view(coordinate)
        if coordinate_from_time(view, self._reference_epoch) != coordinate:
            raise Identifier_Error_InvalidGeneratorInput()
        self._snapshot = (value, view)

    def generate(self):
        with self._lock:
            if self._snapshot is not None:
                raise Identifier_Error_AlreadyInitialized()
            self._publish(self._mint())

    def load(self, value):
        with self._lock:
            if self._snapshot is not None:
                raise Identifier_Error_AlreadyInitialized()
            self._publish(value)

    def read_value(self):
        with self._lock:
            if self._snapshot is None:
                raise Identifier_Error_NotInitialized()
            return self._snapshot[0]

    def get_discriminator(self):
        return self.read_value() & ((1 << 64) - 1)

    def get_issuance_time(self):
        with self._lock:
            if self._snapshot is None:
                raise Identifier_Error_NotInitialized()
            return self._snapshot[1]

    def equivalence(self, other):
        value = self.read_value()
        if not isinstance(other, IdentifierValue):
            raise Identifier_Error_InvalidValue()
        return value == other.read_value()

    def precedes(self, other):
        value = self.read_value()
        if not isinstance(other, IdentifierValue):
            raise Identifier_Error_InvalidValue()
        return value < other.read_value()
