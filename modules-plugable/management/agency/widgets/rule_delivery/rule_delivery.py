#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
from typing import Callable
MOST = 8
WORD = re.compile(r'[a-z0-9][a-z0-9_-]*')

class RuleDelivery:

    def __init__(self, find, titles: Callable[[], tuple[str, ...]]) -> None:
        self._find = find
        self._titles = titles

    def for_subject(self, subject: str) -> list:
        if not subject.strip():
            raise ValueError('subject')
        declared = {title.lower() for title in self._titles()}
        topics: list[str] = []
        for word in WORD.findall(subject.lower()):
            if word in declared and word not in topics:
                topics.append(word)
        return self._find.do(subject, topics, MOST)
