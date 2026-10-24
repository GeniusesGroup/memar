#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/owed.py — owed marks found on one side only: hints, not defects.

Shared with `check`, which prints them apart from the problems it counts.

Owed capability is marked by an opaque identifier ([Content Rule → Owed or
planned capability](../../../modules-plugable/knowledge/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance)):
a line `Owed: <id>` in a Markdown document, and `owed:<id>` in the title of a
pending Test ([Test Practice → Pending](../../../modules/process/test/test.practice.md#the-cycle)).
Only the identifiers are read; no path is opened or resolved, so moving or
rewording anything leaves the finding true. A mention inside a code span or a
fence, or in the middle of a prose line, is not a mark. An identifier on one
side only is reported; a pending Test that has begun to pass while the mark
remains cannot be seen without running it, so is not judged here.
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path
import re
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
without_code = _m_markdown.without_code
ID = '[a-z0-9]+(?:[.-][a-z0-9]+)*'
_DOCUMENT_MARK = re.compile(f'(?m)^Owed: ({ID})[ \\t]*$')
_TEST_MARK = re.compile(f'(?<![A-Za-z0-9_.-])owed:({ID})(?![A-Za-z0-9_-])')
TEST_SUFFIXES = ('.py', '.ts', '.js', '.mjs', '.kh')

def owed_hints(paths: list[Path]) -> list[str]:
    """One report per identifier found in documents only or in Tests only."""
    in_documents: dict[str, str] = {}
    in_tests: dict[str, str] = {}
    for path in paths:
        suffix = path.suffix
        if suffix != '.md' and suffix not in TEST_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        if suffix == '.md':
            for match in _DOCUMENT_MARK.finditer(without_code(text)):
                in_documents.setdefault(match.group(1), str(path))
        else:
            for match in _TEST_MARK.finditer(text):
                in_tests.setdefault(match.group(1), str(path))
    reports = [f'Owed: {identifier} in {where} has no pending Test carrying owed:{identifier} (a hint: the work may be owed with no Test, or the mark may be stale)' for identifier, where in sorted(in_documents.items()) if identifier not in in_tests]
    reports += [f'owed:{identifier} in {where} has no Owed line carrying it (a hint: the Test may be pending for a claim not yet written, or its mark may be stale)' for identifier, where in sorted(in_tests.items()) if identifier not in in_documents]
    return reports
