#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum

class Unknown(enum.Enum):
    NOT_REGISTERED = 'TypeNotRegistered'
    REGISTERED = 'TypeRegistered'
    NO_EQUALITY = 'TypeDeclaresNoEquality'
    NO_ORDER = 'TypeDeclaresNoOrder'

    def summary(self) -> str:
        return {Unknown.NOT_REGISTERED: 'a TypeUUID that no registered type has', Unknown.REGISTERED: 'a type whose TypeUUID is already registered', Unknown.NO_EQUALITY: 'a type that declares no equality of its values', Unknown.NO_ORDER: 'a type that declares no order of its values'}[self]
