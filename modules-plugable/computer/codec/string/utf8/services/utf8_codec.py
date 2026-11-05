#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_mark = import_module('modules-plugable.computer.codec.string.utf8.services.utf8_byte_order_mark')
_m_errors = import_module('modules-plugable.computer.codec.string.utf8.errors.errors')


class UTF8_Codec:

    def decode(self, data):
        rest, had_mark = _m_mark.UTF8_ByteOrderMark().strip(data)
        return (self.decode_bare(rest), had_mark)

    def decode_bare(self, data):
        try:
            return bytes(data).decode('utf-8')
        except UnicodeDecodeError as error:
            raise _m_errors.UTF8_Error_NotUtf8(str(error)) from None

    def decode_named(self, data):
        try:
            return bytes(data).decode('utf-8')
        except UnicodeDecodeError as error:
            raise _m_errors.UTF8_Error_NamedTextNotUtf8(str(error)) from None

    def encode(self, text):
        return text.encode('utf-8')
