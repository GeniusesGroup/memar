#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/install/services/development.py — the mark that says a checkout is where Memar is developed.

The mark is `memar.development` in the checkout's own git configuration, and
`mark_development` is the one write of it. It is the installer's, because a
developer sets it by installing (`memar install --developer`), and the update
reads it to leave such a checkout alone (`bundles/memar/services/update/services/checkout.py`):
the update depends on the install and not the other way round. A mark in git's
configuration of a clone travels with nothing, is never tracked, never shows in
`git status`, and survives a cleared `temp/`.
"""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
DEVELOPMENT_KEY = 'memar.development'

def _config(checkout: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    return subprocess.run(['git', '-C', str(checkout), 'config', *arguments], capture_output=True, text=True, encoding='utf-8', errors='replace', env=environment)

def is_marked_development(checkout: Path) -> bool:
    """Whether CHECKOUT's own git configuration marks it as a development checkout."""
    try:
        said = _config(checkout, '--get', '--bool', DEVELOPMENT_KEY)
    except OSError:
        return False
    return said.stdout.strip() == 'true'

def mark_development(checkout: Path) -> None:
    """Mark CHECKOUT as a development checkout, so no update ever moves it."""
    done = _config(checkout, '--bool', DEVELOPMENT_KEY, 'true')
    if done.returncode != 0:
        said = done.stderr.strip().splitlines()
        raise RuntimeError(said[-1] if said else f'git config exited {done.returncode}')
