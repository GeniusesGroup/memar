# For license and copyright information please see the LEGAL file in the code repository

from threading import Lock
from .time_coordinate import coordinate_from_time
from .errors.generation import Identifier_Error_InvalidGeneratorInput
from .errors.already_initialized import Identifier_Error_AlreadyInitialized
from .errors.not_initialized import Identifier_Error_NotInitialized
from .errors.invalid_value import Identifier_Error_InvalidValue
from .errors.not_decodable import Identifier_Error_NotDecodable
from .errors.buffer_failure import Identifier_Error_BufferFailure
from .errors.value import Identifier_Error_InvalidBytes
from .identifier import complete_bytes
from .readable import encode_readable, decode_readable
from modules.computer.codec.string.errors.not_supported import Stringer_Error_NotSupported

MAXIMUM = (1 << 128) - 1


class IdentifierValue:
    __slots__ = ("_mint", "_time_view", "_reference_epoch", "_snapshot", "_lock", "_string_encoder", "_string_decoder")

    def __init__(self, mint, time_view, reference_epoch, *, string_encoder=encode_readable, string_decoder=decode_readable):
        if not callable(mint) or not callable(time_view):
            raise Identifier_Error_InvalidGeneratorInput()
        if any(binding is not None and not callable(binding) for binding in (string_encoder, string_decoder)):
            raise Identifier_Error_InvalidValue()
        self._string_encoder = string_encoder
        self._string_decoder = string_decoder
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

    def get_serialization_length(self):
        return 16

    def get_media_type(self):
        return "application/octet-stream"

    def encode(self, destination):
        data = self.read_value().to_bytes(16, "big")
        offset = 0
        while offset < len(data):
            written = destination.write(data[offset:])
            if type(written) is not int or not 0 < written <= len(data) - offset:
                raise Identifier_Error_BufferFailure()
            offset += written

    def decode(self, source):
        with self._lock:
            if self._snapshot is not None:
                raise Identifier_Error_AlreadyInitialized()
            data = bytearray()
            while len(data) < 16:
                remaining = 16 - len(data)
                part = source.read(remaining)
                if type(part) is not bytes or not 0 < len(part) <= remaining:
                    raise Identifier_Error_NotDecodable()
                data.extend(part)
            self._publish(int.from_bytes(data, "big"))

    def to_string(self):
        value = self.read_value()
        if self._string_encoder is None:
            raise Stringer_Error_NotSupported()
        result = self._string_encoder(value.to_bytes(16, "big"))
        if type(result) is not str:
            raise Identifier_Error_InvalidValue()
        return result

    def from_string(self, source):
        with self._lock:
            if self._snapshot is not None:
                raise Identifier_Error_AlreadyInitialized()
            if self._string_decoder is None:
                raise Stringer_Error_NotSupported()
            if type(source) is not str:
                raise Identifier_Error_NotDecodable()
            decoded = self._string_decoder(source)
            try:
                raw = complete_bytes(decoded)
            except Identifier_Error_InvalidBytes as error:
                raise Identifier_Error_InvalidValue() from error
            self._publish(int.from_bytes(raw, "big"))

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
