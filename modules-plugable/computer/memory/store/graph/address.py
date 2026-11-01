#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import struct
from typing import Sequence
_U16 = struct.Struct('>H')
_U64 = struct.Struct('>Q')
TAG_LAYOUT = 0
TAG_COMPACT = 1
TAG_PER_EDGE = 2
TAG_IN_COMPACT = 3
TAG_IN_PER_EDGE = 4
GRAPH_TAGS = frozenset({TAG_LAYOUT, TAG_COMPACT, TAG_PER_EDGE, TAG_IN_COMPACT, TAG_IN_PER_EDGE})

def pack(parts: Sequence[bytes]) -> bytes:
    out = bytearray()
    for each in parts:
        out += _U16.pack(len(each))
        out += each
    return bytes(out)

def take(buf: bytes, at: int) -> tuple[bytes, int]:
    length = _U16.unpack_from(buf, at)[0]
    at += 2
    return (buf[at:at + length], at + length)

def adj_key(tag: int, frm: bytes, relation: bytes) -> bytes:
    return bytes([tag]) + pack([frm, relation])

def layout_key(frm: bytes, relation: bytes) -> bytes:
    return adj_key(TAG_LAYOUT, frm, relation)

def per_edge_key(tag: int, frm: bytes, relation: bytes, slot: int) -> bytes:
    return adj_key(tag, frm, relation) + _U64.pack(slot)

def parse_adj(address: bytes) -> tuple[int, bytes, bytes] | None:
    if not isinstance(address, bytes) or len(address) < 2 or address[0] not in GRAPH_TAGS:
        return None
    if address[0] in (TAG_PER_EDGE, TAG_IN_PER_EDGE) and len(address) >= 10:
        try:
            frm, at = take(address, 1)
            relation, at = take(address, at)
            if at + 8 == len(address):
                return (address[0], frm, relation)
        except (struct.error, IndexError):
            return None
        return None
    try:
        frm, at = take(address, 1)
        relation, at = take(address, at)
        if at != len(address):
            return None
        return (address[0], frm, relation)
    except (struct.error, IndexError):
        return None

def parse_side_ref(ref: bytes) -> tuple[int, bytes, bytes, int] | None:
    if not ref or ref[0] not in (TAG_COMPACT, TAG_PER_EDGE, TAG_IN_COMPACT, TAG_IN_PER_EDGE):
        return None
    try:
        frm, at = take(ref, 1)
        relation, at = take(ref, at)
        if at + 8 != len(ref):
            return None
        slot = _U64.unpack_from(ref, at)[0]
        return (ref[0], frm, relation, slot)
    except (struct.error, IndexError):
        return None
