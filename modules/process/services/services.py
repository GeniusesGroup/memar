#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations


class Process_Services:

    def __init__(self) -> None:
        self._by_id: dict[str, object] = {}
        self._by_media_type: dict[str, object] = {}
        self._order: list[object] = []

    def register(self, service: object) -> None:
        operation_id = _operation_id(service)
        if not operation_id:
            raise ValueError('service does not provide an operation id')
        if operation_id in self._by_id:
            raise ValueError(f'service operation id {operation_id} is already registered')
        media_type = _media_type(service)
        if media_type and media_type in self._by_media_type:
            raise ValueError(f'service media type {media_type!r} is already registered')
        self._by_id[operation_id] = service
        if media_type:
            self._by_media_type[media_type] = service
        self._order.append(service)

    def delete(self, service: object) -> None:
        operation_id = _operation_id(service)
        held = self._by_id.pop(operation_id, None)
        media_type = _media_type(held if held is not None else service)
        if media_type:
            self._by_media_type.pop(media_type, None)
        self._order = [item for item in self._order if _operation_id(item) != operation_id]

    def get_by_id(self, operation_id: str) -> object | None:
        return self._by_id.get(operation_id)

    def get_by_media_type(self, media_type: str) -> object | None:
        return self._by_media_type.get(media_type)

    def services(self) -> list[object]:
        return list(self._order)


def _operation_id(service: object) -> str:
    if hasattr(service, 'operation_id'):
        value = service.operation_id
        return str(value() if callable(value) else value)
    return ''


def _media_type(service: object | None) -> str:
    if service is None or not hasattr(service, 'media_type'):
        return ''
    value = service.media_type
    return str(value() if callable(value) else value)
