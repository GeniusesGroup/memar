#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

class Error(Exception):
    def __init__(self, detail: str = '') -> None:
        super().__init__(detail)
        self.detail = detail

class Refusal(Error):
    pass

class NotNamed(Refusal):
    pass

class ContentOfTask(Refusal):
    pass

class NotAFolder(Refusal):
    pass

class PathAbsent(Refusal):
    pass

class ScratchInTaskFolder(Refusal):
    pass

class LinkExists(Refusal):
    pass

class LinkFailed(Error):
    pass

class TrashFailed(Error):
    pass

class RootUnresolved(Error):
    pass
