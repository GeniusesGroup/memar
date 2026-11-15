#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""handler.py — the handler of relayed MCP messages, which the server loads and knows nothing of.

A request of kind `relay` carries one JSON-RPC message from an agent app.

The program an agent app starts is a small relay: it reads a message from the app's standard input, sends it to the
server, and writes the answer back. The tools are generated here once from the command line the services declare,
and a tool call runs as the command line does (`cli/handler.py`). When the resident is busy, one message may run
in an isolated short-lived worker, so a slow call does not hold unrelated clients behind it.
"""
from __future__ import annotations

import json
import os
from importlib import import_module

KIND = 'relay'
_worker = None


def _session():
    global _worker
    if _worker is None:
        module = import_module('bundles.memar_adaptor.mcp.services._worker')
        _worker = module.Worker(import_module('bundles.memar_adaptor.cli.router'))
    return _worker


def answer(call: dict) -> dict:
    """The line that answers the message the call carries: {'line': text}, or None for a notification, which is answered with nothing."""
    return {'line': _reply(call.get('relay', ''))}


def _decode_child(done) -> dict:
    """The one JSON-RPC line emitted by an isolated MCP worker, or no line for a notification."""
    if done.returncode:
        detail = done.stderr.decode('utf-8', errors='replace').strip()
        raise RuntimeError(detail or f'MCP worker exited with status {done.returncode}')
    line = done.stdout.decode('utf-8', errors='replace').strip()
    return {'line': line or None}


def elsewhere(call: dict) -> dict | None:
    """Run one relay message in a fresh worker when the resident is occupied."""
    message = call.get('relay', '')
    try:
        decoded = json.loads(message)
    except (TypeError, ValueError):
        # Keep malformed-input handling in _reply, which returns the MCP parse
        # error without asking the worker to parse the same line a second way.
        return None
    if not isinstance(decoded, dict):
        return None
    location = import_module('bundles.memar.services.location.memar_location')
    return {
        'command': [*location.program(), 'mcp_worker'],
        'cwd': call.get('cwd') or os.getcwd(),
        'env': call.get('env') or dict(os.environ),
        'input': (message + '\n').encode('utf-8'),
        'decode': _decode_child,
    }


def _reply(line: str) -> str | None:
    try:
        message = json.loads(line)
    except ValueError:
        return json.dumps({'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'not a JSON-RPC message'}}, separators=(',', ':'))
    if not isinstance(message, dict):
        return json.dumps({'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'send one message a line'}}, separators=(',', ':'))
    reply = _session().answer(message)
    return None if reply is None else json.dumps(reply, ensure_ascii=False, separators=(',', ':'))
