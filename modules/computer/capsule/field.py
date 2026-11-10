# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from typing import Iterable


class LimitToUseBy:

    def __init__(self, allowed_types: Iterable[str] = ()) -> None:
        self._allowed_types = tuple(allowed_types)

    def allowed_types(self) -> tuple[str, ...]:
        return self._allowed_types


class ImmediateComposer:
    pass


class Unrestricted:
    pass


class Field:

    def __init__(
        self,
        *,
        title: str,
        value_type: str,
        authorization: object | None = None,
    ) -> None:
        self._title = title
        self._value_type = value_type
        self._authorization = Unrestricted() if authorization is None else authorization

    def get_title(self) -> str:
        return self._title

    def value_type(self) -> str:
        return self._value_type

    def authorization(self) -> object:
        return self._authorization


class Fields:

    def __init__(self, fields: Iterable[Field] = ()) -> None:
        self._fields = list(fields)

    def add(self, field: Field) -> None:
        self._fields.append(field)

    def get_occupied_length(self) -> int:
        return len(self._fields)

    def get_element(self, offset: int) -> Field:
        return self._fields[offset]


class FieldBag:

    def __init__(self) -> None:
        self._fields = Fields()

    def add(self, field: Field) -> None:
        self._fields.add(field)

    def get_fields(self) -> Fields:
        return self._fields
