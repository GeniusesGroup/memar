#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from typing import Any
from importlib import import_module
_json = import_module('modules-plugable.computer.memory.store.files.codecs.json.body')
part_to_json = _json.part_to_json
part_from_json = _json.part_from_json
stored_part_bytes = _json.stored_part_bytes
TEXT_ENVELOPE = _json.TEXT_ENVELOPE
BYTES_ENVELOPE = _json.BYTES_ENVELOPE

def _scalar(value: Any) -> str:
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if '\n' in value or ':' in value or value == '' or value[0] in '-?[]{}#&*!|>\'"@`':
            return json_quote(value)
        return value
    raise TypeError(value)

def json_quote(text: str) -> str:
    import json
    return json.dumps(text, ensure_ascii=False)

def _dump_block(value: Any, indent: int) -> str:
    pad = '  ' * indent
    if isinstance(value, dict):
        if not value:
            return '{}'
        lines = []
        for key in sorted(value):
            item = value[key]
            if isinstance(item, (dict, list)):
                lines.append(f'{pad}{key}:\n{_dump_block(item, indent + 1)}')
            else:
                lines.append(f'{pad}{key}: {_scalar(item)}')
        return '\n'.join(lines)
    if isinstance(value, list):
        if not value:
            return '[]'
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f'{pad}-\n{_dump_block(item, indent + 1)}')
            else:
                lines.append(f'{pad}- {_scalar(item)}')
        return '\n'.join(lines)
    return f'{pad}{_scalar(value)}'

def dump_yaml(value: Any) -> bytes:
    return (_dump_block(value, 0) + '\n').encode('utf-8')

def _load_scalar(text: str) -> Any:
    if text == 'true':
        return True
    if text == 'false':
        return False
    if text == 'null':
        return None
    if text and text[0] in '"\'':
        import json
        return json.loads(text)
    try:
        if '.' in text or 'e' in text.lower():
            return float(text)
        return int(text)
    except ValueError:
        return text

def _parse_lines(lines: list[str], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return ({}, index)
    line = lines[index]
    if not line.strip():
        return ({}, index + 1)
    stripped = line.lstrip(' ')
    current = len(line) - len(stripped)
    if current < indent:
        return ({}, index)
    if stripped.startswith('- '):
        items: list[Any] = []
        while index < len(lines):
            line = lines[index]
            stripped = line.lstrip(' ')
            if not stripped:
                index += 1
                continue
            current = len(line) - len(stripped)
            if current < indent or not stripped.startswith('- '):
                break
            payload = stripped[2:]
            if payload == '':
                index += 1
                nested, index = _parse_lines(lines, index, indent + 2)
                items.append(nested)
            elif payload.endswith(':'):
                key = payload[:-1]
                index += 1
                nested, index = _parse_lines(lines, index, indent + 2)
                items.append({key: nested})
            else:
                items.append(_load_scalar(payload))
                index += 1
        return (items, index)
    body: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip(' ')
        if not stripped:
            index += 1
            continue
        current = len(line) - len(stripped)
        if current < indent:
            break
        if ':' not in stripped:
            break
        key, rest = stripped.split(':', 1)
        key = key.strip()
        rest = rest.strip()
        if rest == '':
            index += 1
            nested, index = _parse_lines(lines, index, indent + 2)
            body[key] = nested
        else:
            body[key] = _load_scalar(rest)
            index += 1
    return (body, index)

def load_yaml(data: bytes) -> Any:
    text = data.decode('utf-8')
    lines = text.splitlines()
    if not lines:
        return {}
    parsed, end = _parse_lines(lines, 0, 0)
    if end < len(lines) and any(each.strip() for each in lines[end:]):
        return None
    return parsed

class Files_YAML_Body_Codec:

    def get_name(self) -> str:
        return 'yaml'

    def pack(self, parts: dict[bytes, bytes]) -> tuple[bytes, dict[bytes, bytes]]:
        stored = {key: stored_part_bytes(value) for key, value in parts.items()}
        body: dict[str, Any] = {}
        for key in sorted(stored):
            body[key.decode('ascii')] = part_to_json(stored[key])
        return dump_yaml(body), stored

    def unpack(self, body: bytes) -> dict[bytes, bytes] | None:
        try:
            parsed = load_yaml(body)
        except UnicodeDecodeError:
            return None
        if parsed is None or not isinstance(parsed, dict):
            return None
        parts: dict[bytes, bytes] = {}
        for key, value in parsed.items():
            if not isinstance(key, str):
                return None
            try:
                domain = key.encode('ascii')
            except UnicodeEncodeError:
                return None
            parts[domain] = part_from_json(value)
        return parts
