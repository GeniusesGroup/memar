#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from typing import Any
_m_errors = import_module('modules.computer.types.errors.errors')
Unknown = _m_errors.Unknown

class Types:

    def __init__(self) -> None:
        self._by_id: dict[bytes, Any] = {}

    def register(self, dt: Any) -> Unknown | None:
        if dt.type_id in self._by_id:
            return Unknown.REGISTERED
        self._by_id[dt.type_id] = dt
        return None

    def get_by_id(self, id: bytes) -> Any:
        return self._by_id.get(id, Unknown.NOT_REGISTERED)

    def get_value_equality(self, id: bytes) -> Any:
        dt = self.get_by_id(id)
        if isinstance(dt, Unknown):
            return dt
        if not hasattr(dt, 'values_equal'):
            return Unknown.NO_EQUALITY
        return dt

    def get_value_order(self, id: bytes) -> Any:
        dt = self.get_value_equality(id)
        if isinstance(dt, Unknown):
            return Unknown.NO_ORDER if dt is Unknown.NO_EQUALITY else dt
        if not hasattr(dt, 'compare_values'):
            return Unknown.NO_ORDER
        return dt
