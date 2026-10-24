#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/propagation.py — the `Propagates to` entries a changelog still owes: obligations, not defects.

Shared by `obligations`, which prints the work-list, and by `check`, which
prints it apart from the problems it counts. One reading of the field, so the
two never report a different list.

A changelog entry's `Propagates to` field names another artifact and the state
of the work the change implies there (changelog.md -> Propagates
to). `Pending` is the one open state; `Done` and `Rejected` are closed, and
`Rejected` is closed permanently. `search` excludes changelog files, because
their content is history rather than current truth, which is right for concept
search and would leave the work-list with no surface at all.
"""
from __future__ import annotations
from importlib import import_module
import re
from pathlib import Path
_m_propagation_state = import_module('modules-plugable.knowledge.documentation.changelog.primitive.propagation_state')
PropagationState = _m_propagation_state.PropagationState
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
without_code = _m_markdown.without_code
_PROPAGATION_OPEN = re.compile('(?m)^[ \\t]*[-*][ \\t]+\\S.*?:[ \\t]*' + PropagationState.PENDING.word + '(?![A-Za-z])')

def _is_changelog_ledger(path: Path) -> bool:
    return path.stem.endswith('.changelog')

def undischarged_propagations(paths: list[Path]) -> list[tuple[Path, int, str]]:
    """Every `Propagates to` entry left `Pending`, as (file, line, report).

    Changelog files only, since that is where the field is defined. Returns
    rather than raises: a `Pending` entry is correct content of the file that
    holds it, so this is a work-list and not a defect, and a caller that counts
    defects must not count these.
    """
    found: list[tuple[Path, int, str]] = []
    for path in paths:
        if path.suffix.lower() != '.md' or not _is_changelog_ledger(path):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        visible = without_code(text)
        for match in _PROPAGATION_OPEN.finditer(visible):
            line = visible[:match.start()].count('\n') + 1
            artifact = match.group(0).lstrip(' \t-*').rstrip()
            found.append((path, line, f'{path.name} {line}: {artifact} — not yet done'))
    return found
