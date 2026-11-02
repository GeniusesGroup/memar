#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import uuid
TASK = 'task'
LABELS = 'labels'
CONTENT = 'content'
TEXT = 'text'
MEDIA_MARKDOWN = 'text/markdown'


def json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def uuid_text(at: bytes) -> str:
    return str(uuid.UUID(bytes=at))
