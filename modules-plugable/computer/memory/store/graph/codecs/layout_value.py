#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import struct
from dataclasses import dataclass
from typing import Sequence
_U16 = struct.Struct('>H')
_U64 = struct.Struct('>Q')

@dataclass
class Stored_Side:
    slot: int
    to: bytes
    fields: bytes
    ended: bool = False
    reverse_ref: bytes = b''
    inbound_ref: bytes = b''

@dataclass(frozen=True)
class Stored_Edge_Value:
    to: bytes
    fields: bytes
    ended: bool = False
    reverse_ref: bytes = b''
    inbound_ref: bytes = b''

def _take(buf: bytes, at: int) -> tuple[bytes, int]:
    length = _U16.unpack_from(buf, at)[0]
    at += 2
    return (buf[at:at + length], at + length)

class Graph_Default_Layout_Value_Codec:

    def pack_compact(self, sides: Sequence[Stored_Side]) -> bytes:
        out = bytearray()
        for each in sides:
            out += _U64.pack(each.slot)
            out.append(1 if each.ended else 0)
            out += _U16.pack(len(each.to))
            out += each.to
            out += _U16.pack(len(each.fields))
            out += each.fields
            out += _U16.pack(len(each.reverse_ref))
            out += each.reverse_ref
            out += _U16.pack(len(each.inbound_ref))
            out += each.inbound_ref
        return bytes(out)

    def unpack_compact(self, value: bytes) -> list[Stored_Side]:
        sides: list[Stored_Side] = []
        at = 0
        while at < len(value):
            slot = _U64.unpack_from(value, at)[0]
            at += 8
            ended = bool(value[at])
            at += 1
            to, at = _take(value, at)
            fields, at = _take(value, at)
            reverse_ref, at = _take(value, at)
            inbound_ref, at = _take(value, at)
            sides.append(Stored_Side(slot, to, fields, ended, reverse_ref, inbound_ref))
        return sides

    def pack_per_edge(self, edge: Stored_Edge_Value) -> bytes:
        return bytes([1 if edge.ended else 0]) + _U16.pack(len(edge.to)) + edge.to + _U16.pack(len(edge.fields)) + edge.fields + _U16.pack(len(edge.reverse_ref)) + edge.reverse_ref + _U16.pack(len(edge.inbound_ref)) + edge.inbound_ref

    def unpack_per_edge(self, value: bytes) -> Stored_Edge_Value:
        ended = bool(value[0])
        to, at = _take(value, 1)
        fields, at = _take(value, at)
        reverse_ref, at = _take(value, at)
        inbound_ref, _ = _take(value, at)
        return Stored_Edge_Value(to, fields, ended, reverse_ref, inbound_ref)
