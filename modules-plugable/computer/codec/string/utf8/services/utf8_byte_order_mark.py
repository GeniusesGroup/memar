#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
MARK = b'\xef\xbb\xbf'


class UTF8_ByteOrderMark:

    def detect(self, data):
        return data.startswith(MARK)

    def strip(self, data):
        if self.detect(data):
            return (data[len(MARK):], True)
        return (data, False)
