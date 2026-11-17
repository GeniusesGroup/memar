# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from typing import Any
from modules.identity.identifier.identifier import complete_bytes
from modules.identity.identifier.errors.value import Identifier_Error_InvalidBytes

_m_errors = import_module('modules.computer.types.errors.errors')
Unknown = _m_errors.Unknown


class Types:

    def __init__(self) -> None:
        self._by_id: dict[bytes, Any] = {}

    def register(self, dt: Any) -> Unknown | Identifier_Error_InvalidBytes | None:
        try:
            identity = complete_bytes(getattr(dt, 'type_id', None))
        except Identifier_Error_InvalidBytes as error:
            return error
        if identity in self._by_id:
            return Unknown.REGISTERED
        self._by_id[identity] = dt
        return None

    def get_by_id(self, id: bytes) -> Any:
        try:
            identity = complete_bytes(id)
        except Identifier_Error_InvalidBytes as error:
            return error
        return self._by_id.get(identity, Unknown.NOT_REGISTERED)

    def get_value_equality(self, id: bytes) -> Any:
        dt = self.get_by_id(id)
        if isinstance(dt, (Unknown, Identifier_Error_InvalidBytes)):
            return dt
        if not hasattr(dt, 'values_equal'):
            return Unknown.NO_EQUALITY
        return dt

    def get_value_order(self, id: bytes) -> Any:
        dt = self.get_value_equality(id)
        if isinstance(dt, (Unknown, Identifier_Error_InvalidBytes)):
            return Unknown.NO_ORDER if dt is Unknown.NO_EQUALITY else dt
        if not hasattr(dt, 'compare_values'):
            return Unknown.NO_ORDER
        return dt
