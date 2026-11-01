#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import base64
import json
from typing import Any
TEXT_ENVELOPE = '$files.text'
BYTES_ENVELOPE = '$files.bytes'

def part_to_json(data: bytes) -> Any:
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return {BYTES_ENVELOPE: base64.b64encode(data).decode('ascii')}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {TEXT_ENVELOPE: text}

def part_from_json(value: Any) -> bytes:
    if isinstance(value, dict):
        if set(value.keys()) == {BYTES_ENVELOPE} and isinstance(value[BYTES_ENVELOPE], str):
            return base64.b64decode(value[BYTES_ENVELOPE])
        if set(value.keys()) == {TEXT_ENVELOPE} and isinstance(value[TEXT_ENVELOPE], str):
            return value[TEXT_ENVELOPE].encode('utf-8')
    return json.dumps(value, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def stored_part_bytes(data: bytes) -> bytes:
    return part_from_json(part_to_json(data))

class Files_JSON_Body_Codec:

    def get_name(self) -> str:
        return 'json'

    def pack(self, parts: dict[bytes, bytes]) -> tuple[bytes, dict[bytes, bytes]]:
        stored = {key: stored_part_bytes(value) for key, value in parts.items()}
        body: dict[str, Any] = {}
        for key in sorted(stored):
            body[key.decode('ascii')] = part_to_json(stored[key])
        encoded = (json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
        return encoded, stored

    def unpack(self, body: bytes) -> dict[bytes, bytes] | None:
        try:
            parsed = json.loads(body.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(parsed, dict):
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
