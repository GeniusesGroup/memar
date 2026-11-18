# For license and copyright information please see the LEGAL file in the code repository

import re
from datetime import datetime, timedelta

from .identifier import complete_bytes
from .errors.not_decodable import Identifier_Error_NotDecodable

_EPOCH = datetime(1970, 1, 1)
_NANOSECONDS = 1000000000
_MAXIMUM_TIME = (1 << 64) - 1
_PATTERN = re.compile(r"([0-9]{4})([0-9]{2})([0-9]{2})-T([0-9]{2})([0-9]{2})([0-9]{2})\.([0-9]{9})Z-([0-9A-F]{16})")


def encode_readable(identity):
    raw = complete_bytes(identity)
    coordinate = int.from_bytes(raw[:8], "big")
    seconds, nanoseconds = divmod(coordinate, _NANOSECONDS)
    civil = _EPOCH + timedelta(seconds=seconds)
    return (
        f"{civil.year:04d}{civil.month:02d}{civil.day:02d}-T"
        f"{civil.hour:02d}{civil.minute:02d}{civil.second:02d}."
        f"{nanoseconds:09d}Z-{int.from_bytes(raw[8:], 'big'):016X}"
    )


def decode_readable(source):
    if type(source) is not str or len(source) != 44:
        raise Identifier_Error_NotDecodable()
    match = _PATTERN.fullmatch(source)
    if match is None:
        raise Identifier_Error_NotDecodable()
    year, month, day, hour, minute, second, nanoseconds = map(int, match.groups()[:7])
    try:
        civil = datetime(year, month, day, hour, minute, second)
    except ValueError as error:
        raise Identifier_Error_NotDecodable() from error
    elapsed = civil - _EPOCH
    coordinate = (elapsed.days * 86400 + elapsed.seconds) * _NANOSECONDS + nanoseconds
    if not 0 <= coordinate <= _MAXIMUM_TIME:
        raise Identifier_Error_NotDecodable()
    discriminator = int(match[8], 16)
    return coordinate.to_bytes(8, "big") + discriminator.to_bytes(8, "big")
