#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
from dataclasses import dataclass, field

class ViewRefusal(enum.Enum):
    UNIGNORED_FOLDER = 'UnignoredFolder'
    FOREIGN_FILES = 'ForeignFiles'
    MALFORMED_PATH = 'MalformedPath'
    UNAVAILABLE = 'Unavailable'

    def summary(self) -> str:
        return {ViewRefusal.UNIGNORED_FOLDER: 'the folder is in a working tree under version control, which does not ignore it', ViewRefusal.FOREIGN_FILES: 'the folder holds a file the builder did not write', ViewRefusal.MALFORMED_PATH: 'the presentation gave a path that leaves the folder, names the list, or shows two things', ViewRefusal.UNAVAILABLE: 'the store did not answer every read'}[self]

@dataclass(frozen=True)
class ViewRefused:
    reason: ViewRefusal
    detail: str = field(default='', compare=False)

    def summary(self) -> str:
        return f'{self.reason.summary()}: {self.detail}' if self.detail else self.reason.summary()

@dataclass(frozen=True)
class BadPreference:
    detail: str = field(default='', compare=False)

    def summary(self) -> str:
        return f'the key `view` is not one `class=folder` pair: {self.detail}' if self.detail else 'the key `view` is not one `class=folder` pair'
