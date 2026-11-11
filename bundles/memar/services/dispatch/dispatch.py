#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

import importlib
import io
import os
import sys
from types import SimpleNamespace
from typing import Any

FIELDS = 'fields'
RUNS = 'runs'
CWD = 'cwd'
ENV = 'env'
STDIN = 'stdin'
ARGV = 'argv'


class Refused(ValueError):
    pass


def _load_run(ref: str):
    if ':' not in ref:
        raise Refused(f'run ref {ref!r} is module:attr')
    module_name, attr = ref.rsplit(':', 1)
    module = importlib.import_module(module_name)
    run = getattr(module, attr, None)
    if not callable(run):
        raise Refused(f'run ref {ref!r} is not callable')
    return run


def _checked(call: dict) -> dict:
    if not isinstance(call, dict):
        raise Refused('a Server_Call is an object')
    if ARGV in call:
        raise Refused('the server does not accept argv; a face sends fields and runs')
    fields = call.get(FIELDS)
    runs = call.get(RUNS)
    cwd = call.get(CWD)
    env = call.get(ENV)
    stdin = call.get(STDIN, '')
    if not isinstance(fields, dict):
        raise Refused('fields is an object')
    if not isinstance(runs, list) or not all(isinstance(each, str) for each in runs):
        raise Refused('runs is a list of module:attr strings')
    if not isinstance(cwd, str):
        raise Refused('cwd is a folder path string')
    if not isinstance(env, dict):
        raise Refused('env is an object')
    if not isinstance(stdin, str):
        raise Refused('stdin is a string')
    return {'fields': fields, 'runs': runs, 'cwd': cwd, 'env': env, 'stdin': stdin}


def handle(call: dict) -> dict[str, Any]:
    checked = _checked(call)
    args = SimpleNamespace(**checked['fields'])
    kept_environment, kept_folder = dict(os.environ), os.getcwd()
    # Bytes + TextIOWrapper(newline=None): print() matches the platform line ending the CLI uses.
    out_bytes, err_bytes = io.BytesIO(), io.BytesIO()
    out = io.TextIOWrapper(out_bytes, encoding='utf-8', newline=None, write_through=True)
    err = io.TextIOWrapper(err_bytes, encoding='utf-8', errors='backslashreplace', newline=None, write_through=True)
    status = 0
    try:
        os.chdir(checked['cwd'])
        os.environ.clear()
        os.environ.update({str(key): str(value) for key, value in checked['env'].items()})
        sys.stdin = io.StringIO(checked['stdin'])
        sys.stdout = out
        sys.stderr = err
        try:
            for ref in checked['runs']:
                result = _load_run(ref)(args)
                if result:
                    status = int(result)
                    break
        except SystemExit as stop:
            if stop.code is None:
                status = 0
            elif isinstance(stop.code, int):
                status = stop.code
            else:
                err.write(str(stop.code))
                if not str(stop.code).endswith('\n'):
                    err.write('\n')
                status = 1
        except Exception:
            import traceback
            traceback.print_exc(file=err)
            status = 1
    finally:
        for stream in (out, err):
            try:
                stream.flush()
            except ValueError:
                pass
        os.environ.clear()
        os.environ.update(kept_environment)
        os.chdir(kept_folder)
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    return {
        'status': status,
        'stdout': out_bytes.getvalue().decode('utf-8'),
        'stderr': err_bytes.getvalue().decode('utf-8', errors='replace'),
    }
