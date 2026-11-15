#!/usr/bin/env python3
from __future__ import annotations

import json

NOT_HANDLED = object()
INVALID_PARAMS = -32602


def answer(line: str) -> str | None | object:
    try:
        message = json.loads(line)
    except (TypeError, ValueError):
        return NOT_HANDLED
    if not isinstance(message, dict) or message.get("method") != "ping":
        return NOT_HANDLED
    if "id" not in message:
        return None
    identity = message["id"]
    params = message.get("params") or {}
    if not isinstance(params, dict):
        response = {
            "jsonrpc": "2.0",
            "id": identity,
            "error": {
                "code": INVALID_PARAMS,
                "message": "the params of a request are an object",
            },
        }
    else:
        response = {"jsonrpc": "2.0", "id": identity, "result": {}}
    return json.dumps(response, ensure_ascii=False, separators=(",", ":"))
