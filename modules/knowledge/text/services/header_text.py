#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import json
PLAIN_START = '"\'[]{}&*!|>%@`-?#,'


def scalar(value: str) -> str:
    if value == '' or value != value.strip() or ': ' in value or ' #' in value or value[0] in PLAIN_START or '\n' in value:
        return json.dumps(value, ensure_ascii=False)
    return value


def bare(item: str) -> str:
    item = item.strip()
    return item[2:] if item.startswith('- ') else item


def render(pairs: dict, blocks: tuple = (), bare_blocks: tuple = ()) -> str:
    lines = []
    for key, value in pairs.items():
        if value in (None, ''):
            continue
        value = str(value)
        if key in blocks or key in bare_blocks or '\n' in value:
            lines.append(f'{key}:')
            lines += [f'  - {scalar(item) if key not in bare_blocks else bare(item)}' for item in value.split('\n') if item]
        else:
            lines.append(f'{key}: {scalar(value)}')
    return '\n'.join(lines) + ('\n' if lines else '')


def parse(lines: list) -> dict:
    found: dict = {}
    current = None
    for line in lines:
        if line[:1] in (' ', '\t') and current is not None:
            child = line.strip()
            child = child[2:] if child.startswith('- ') else child
            if child[:1] == '"':
                child = json.loads(child)
            if child:
                found[current] = f'{found[current]}\n{child}' if found[current] else child
        elif ':' in line and line.partition(':')[0].strip() and (line.partition(':')[2][:1] in ('', ' ')):
            key, _, value = line.partition(':')
            current = key.strip()
            value = value.strip()
            found[current] = json.loads(value) if value[:1] == '"' else value
        else:
            current = None
    return {key: value for key, value in found.items() if value}
