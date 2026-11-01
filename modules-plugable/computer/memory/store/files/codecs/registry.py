#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from typing import Callable, Protocol
_m_errors = import_module('modules-plugable.computer.memory.store.files.errors.errors')
BadCodec = _m_errors.BadCodec

class Files_Body_Codec(Protocol):

    def get_name(self) -> str:
        ...

    def pack(self, parts: dict[bytes, bytes]) -> tuple[bytes, dict[bytes, bytes]]:
        ...

    def unpack(self, body: bytes) -> dict[bytes, bytes] | None:
        ...

_FACTORIES: dict[str, Callable[[], Files_Body_Codec]] = {}

def register(name: str, factory: Callable[[], Files_Body_Codec]) -> None:
    _FACTORIES[name] = factory

def resolve(name: str) -> Files_Body_Codec:
    factory = _FACTORIES.get(name)
    if factory is None:
        raise BadCodec(name)
    return factory()

def registered_names() -> frozenset[str]:
    return frozenset(_FACTORIES)

def _load_builtins() -> None:
    if _FACTORIES:
        return
    json_mod = import_module('modules-plugable.computer.memory.store.files.codecs.json.body')
    yaml_mod = import_module('modules-plugable.computer.memory.store.files.codecs.yaml.body')
    register(json_mod.Files_JSON_Body_Codec().get_name(), json_mod.Files_JSON_Body_Codec)
    register(yaml_mod.Files_YAML_Body_Codec().get_name(), yaml_mod.Files_YAML_Body_Codec)

_load_builtins()
