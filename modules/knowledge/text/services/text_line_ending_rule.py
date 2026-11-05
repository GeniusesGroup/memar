#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
LF = '\n'
CRLF = '\r\n'


class Text_LineEnding:

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def get_sequence(self) -> str:
        return self.sequence


class Text_LineEnding_Rule:

    def detect(self, held):
        crlf = held.count(CRLF)
        lf = held.count(LF) - crlf
        if crlf and (not lf):
            return Text_LineEnding(CRLF)
        return Text_LineEnding(LF)

    def choose(self, choice, held):
        if choice.is_given():
            return choice.get_line_ending()
        return self.detect(held)

    def normalize(self, text, line_ending):
        sequence = line_ending.get_sequence()
        text = text.replace(CRLF, LF).replace('\r', LF)
        if sequence != LF:
            text = text.replace(LF, sequence)
        if text and (not text.endswith(sequence)):
            text += sequence
        return text
