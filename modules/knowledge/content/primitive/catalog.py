#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Iterator
from zlib import crc32
from modules.knowledge.content.primitive.section import Section
from modules.knowledge.content.primitive.word import Word

DECLARES = re.compile(r'^class\s+\w+\(', re.M)

class Catalog:
    __slots__ = ('_members',)

    def __init__(self, folder: Path, label: str) -> None:
        found = []
        for path in sorted(Path(folder).glob('*.py')):
            if path.name.startswith('_'):
                continue
            if not DECLARES.search(path.read_text(encoding='utf-8')):
                continue
            module = self._load(path.resolve())
            for value in vars(module).values():
                if isinstance(value, type) and issubclass(value, (Section, Word)) and value.__module__ == module.__name__ and label in value.labels:
                    found.append(value)
        self._members = tuple(sorted(found, key=lambda member: (member.order, member.__name__)))

    @staticmethod
    def _load(path: Path):
        name = f'_catalog_{crc32(str(path).encode()):08x}_{path.stem}'
        if name in sys.modules:
            return sys.modules[name]
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _name(member: type) -> str:
        return member.heading if issubclass(member, Section) else member.word

    def headings(self) -> tuple[str, ...]:
        return tuple(member.heading for member in self._members if issubclass(member, Section))

    def words(self) -> tuple[str, ...]:
        return tuple(member.word for member in self._members if issubclass(member, Word))

    def read(self, text: str) -> type | None:
        wanted = text.strip().lower()
        return next((member for member in self._members if self._name(member).lower() == wanted), None)

    def listing(self) -> str:
        words = self.words()
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]

    def __iter__(self) -> Iterator[type]:
        return iter(self._members)

    def __len__(self) -> int:
        return len(self._members)
