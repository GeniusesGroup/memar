#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
scratch_root = _m_memar_location.scratch_root
import json
import os
import sys
from machine.console import CALLER_ENV, MCP_CALLER
SERVER = {'name': 'memar', 'title': 'Memar', 'version': 'provisional'}
PROTOCOL_VERSIONS = ('2025-06-18', '2025-03-26', '2024-11-05')
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
RUN = 'memar/run'
STATUS = 'memar/status'
INDEX = 'modules.knowledge.text.services.index'

class Worker:

    def __init__(self, router) -> None:
        from bundles.memar_adaptor.mcp.services import _call
        recorded = _call.Globals((*router.DECLARED, INDEX))
        recorded.watch_imports()
        from bundles.memar_adaptor.mcp.mcp import COMMAND
        from bundles.memar_adaptor.mcp.services import _tools
        from modules.knowledge.text.services import index
        self.router = router
        self.tools_module = _tools
        recorded.values.pop(router.__name__, None)
        self.runner = _call.Runner(router, recorded, scratch_root())
        parser, _ = router.assemble(router.services())
        index.keep()
        recorded.record(index)
        self.tools = {tool.name: tool for tool in _tools.tools(parser, left_out=(COMMAND,))}

    def answer(self, message: dict) -> dict | None:
        method, identity = (message.get('method'), message.get('id'))
        params = message.get('params') or {}
        if 'id' not in message:
            return None
        try:
            if not isinstance(params, dict):
                raise self.tools_module.Refused('the params of a request are an object')
            result = self._result(method, params)
        except LookupError as missing:
            return {'jsonrpc': '2.0', 'id': identity, 'error': {'code': METHOD_NOT_FOUND, 'message': str(missing)}}
        except self.tools_module.Refused as refused:
            return {'jsonrpc': '2.0', 'id': identity, 'error': {'code': INVALID_PARAMS, 'message': str(refused)}}
        return {'jsonrpc': '2.0', 'id': identity, 'result': result}

    def _result(self, method: str, params: dict) -> dict:
        if method == 'initialize':
            asked = params.get('protocolVersion')
            catalog = next((tool.name for tool in self.tools.values() if getattr(tool.parser, '_memar_legacy_words', ()) == ('commands',)), '')
            return {'protocolVersion': asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0], 'capabilities': {'tools': {}}, 'serverInfo': SERVER, 'instructions': f"Each tool has the same call name as the `memar` CLI and answers as it does. A tool's description holds its help; call the tool directly. The tool `{catalog}` lists the services."}
        if method == 'ping':
            return {}
        if method == 'tools/list':
            return {'tools': [self.tools_module.definition(tool) for tool in self.tools.values()]}
        if method == 'tools/call':
            tool = self.tools.get(params.get('name'))
            if tool is None:
                raise self.tools_module.Refused(f"no tool is named {params.get('name')!r}")
            argv, stdin = self.tools_module.argv(tool, params.get('arguments') or {})
            answer = self._answer_from_argv(argv, stdin)
            content = [{'type': 'text', 'text': answer['stdout']}]
            if answer['stderr']:
                content.append({'type': 'text', 'text': answer['stderr']})
            return {'content': content, 'isError': answer['status'] != 0, '_meta': {STATUS: answer['status']}}
        if method == RUN:
            return self._run(params)
        raise LookupError(f'this server has no method {method!r}')

    def _answer_from_argv(self, argv: list[str], stdin: str='') -> dict:
        """The words of a tool call run as a command is: parsed here, answered whole; a wrong call is a status, not a dead worker."""
        from bundles.memar_adaptor.cli import handler
        environment = {**os.environ, CALLER_ENV: MCP_CALLER}
        return handler.answer({'argv': argv, 'cwd': os.getcwd(), 'env': environment, 'stdin': stdin})

    def _dispatch(self, call: dict) -> dict:
        from bundles.memar.services.dispatch import dispatch
        try:
            return dispatch.handle(call)
        except dispatch.Refused as refused:
            raise self.tools_module.Refused(str(refused)) from refused

    def _run(self, params: dict) -> dict:
        """One Server_Call: fields and runs the face already filled, answered without argv."""
        return self._dispatch(params)

def main(router) -> None:
    from bundles.memar_adaptor.mcp.services._call import align_windows_std_handles
    incoming = os.fdopen(os.dup(0), 'rb')
    outgoing = os.fdopen(os.dup(1), 'wb')
    null = os.open(os.devnull, os.O_RDWR)
    os.dup2(null, 0)
    os.dup2(null, 1)
    os.close(null)
    align_windows_std_handles()
    sys.stdin = open(os.devnull, encoding='utf-8')
    sys.stdout = sys.stderr
    worker = Worker(router)
    for line in iter(incoming.readline, b''):
        if not line.strip():
            continue
        answer = worker.answer(json.loads(line))
        if answer is not None:
            outgoing.write(json.dumps(answer, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n')
            outgoing.flush()
