#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/services/_worker.py — the worker `memar mcp serve` starts: answers MCP's requests with Memar's verbs as tools.

It speaks the part of MCP a tool server needs: `initialize`, `ping`, `tools/list` and `tools/call`;
every other request is answered as a method it does not have. The tools are made once, when the
worker starts, from the command line the router assembles (`_tools.py`), and a call is run by
`_call.py`; the worker is replaced by the relay when the code they are made of changes, so it never
has to notice that itself.

The conversation runs on copies of the descriptors the worker was started with. Descriptors 0 and 1
themselves are pointed at the null device, so that nothing a verb or a child process of one writes
or reads outside a call can reach the conversation; during a call they are the call's.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
scratch_root = _m_fs_memar.scratch_root
import json
import os
import sys
from pathlib import Path
SERVER = {'name': 'memar', 'title': 'Memar', 'version': 'provisional'}
PROTOCOL_VERSIONS = ('2025-06-18', '2025-03-26', '2024-11-05')
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
RUN = 'memar/run'
STATUS = 'memar/status'

def _load_router(scripts: Path):
    """The router, the `memar` file beside the shelves, loaded as a module (it has no `.py`)."""
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader('memar_router', str(scripts / 'memar'))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module

class Worker:

    def __init__(self, scripts: Path, top: Path) -> None:
        from mcp.services import _call
        recorded = _call.Globals(top)
        recorded.watch_imports()
        from mcp.mcp import COMMAND
        from mcp.services import _tools
        from modules.knowledge.text.services import index
        self.tools_module = _tools
        router = _load_router(scripts)
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
            return {'protocolVersion': asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0], 'capabilities': {'tools': {'listChanged': True}}, 'serverInfo': SERVER, 'instructions': 'Each tool is one verb of the `memar` command and answers exactly what it prints. Start with the tool `commands`.'}
        if method == 'ping':
            return {}
        if method == 'tools/list':
            return {'tools': [self.tools_module.definition(tool) for tool in self.tools.values()]}
        if method == 'tools/call':
            tool = self.tools.get(params.get('name'))
            if tool is None:
                raise self.tools_module.Refused(f"no tool is named {params.get('name')!r}")
            argv, stdin = self.tools_module.argv(tool, params.get('arguments') or {})
            output = self.runner.run(argv, stdin)
            content = [{'type': 'text', 'text': output.stdout}]
            if output.stderr:
                content.append({'type': 'text', 'text': output.stderr})
            return {'content': content, 'isError': output.status != 0, '_meta': {STATUS: output.status}}
        if method == RUN:
            return self._run(params)
        raise LookupError(f'this server has no method {method!r}')

    def _run(self, params: dict) -> dict:
        """The CLI's run of `argv` in the folder and environment the caller had, its stdout and stderr whole and its status."""
        argv, stdin = (params.get('argv'), params.get('stdin') or '')
        folder, environment = (params.get('cwd'), params.get('env'))
        if not isinstance(argv, list) or not all((isinstance(word, str) for word in argv)):
            raise self.tools_module.Refused('argv is a list of strings')
        if not isinstance(environment, dict) or not isinstance(folder, str):
            raise self.tools_module.Refused('cwd is a folder and env a mapping')
        kept_environment, kept_folder = (dict(os.environ), os.getcwd())
        try:
            os.chdir(folder)
            os.environ.clear()
            os.environ.update({str(key): str(value) for key, value in environment.items()})
            output = self.runner.run(argv, stdin)
        finally:
            os.environ.clear()
            os.environ.update(kept_environment)
            os.chdir(kept_folder)
        return {'stdout': output.stdout, 'stderr': output.stderr, 'status': output.status}

def main(scripts: str, top: str) -> None:
    incoming = os.fdopen(os.dup(0), 'rb')
    outgoing = os.fdopen(os.dup(1), 'wb')
    null = os.open(os.devnull, os.O_RDWR)
    os.dup2(null, 0)
    os.dup2(null, 1)
    os.close(null)
    sys.stdin = open(os.devnull, encoding='utf-8')
    sys.stdout = sys.stderr
    worker = Worker(Path(scripts), Path(top))
    for line in iter(incoming.readline, b''):
        if not line.strip():
            continue
        answer = worker.answer(json.loads(line))
        if answer is not None:
            outgoing.write(json.dumps(answer, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n')
            outgoing.flush()
