#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that no script or service file grows past the size mark without being named.

    python .agents/scripts/tests/script_size.py

The rule is in [Scripts](../../README.md) -> A growing file is a sign of a problem.
The mark is MARK_LINES lines, chosen after measuring the files under `services/`,
`host/` and `machine/`, and the Python under `modules/`, `modules-plugable/`,
and `bundles/memar/`: nearly all are under 420 lines, and the files above 450
are the few that hold more than one concern. Tests are not measured; a suite
grows with what it pins.

What is pinned:

  NoNewFileOverTheMark  A source file over the mark that OVER_THE_MARK does not
                        name fails: the growth is the signal, and the answer is to
                        split it by concern, not to raise the mark.
  NoStaleEntry          A file named in OVER_THE_MARK that is back under the mark
                        fails, so the list only shrinks.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
TOP = SCRIPTS.parent.parent
sys.dont_write_bytecode = True

MARK_LINES = 450

# Files over the mark, each with what it should split into. None is over it now; the list only shrinks.
OVER_THE_MARK: dict[str, str] = {}


def measured() -> dict[str, int]:
    sizes = {}
    for shelf in ("host", "machine"):
        for path in sorted((SCRIPTS / shelf).glob("*.py")):
            sizes[f"{shelf}/{path.name}"] = len(path.read_text(encoding="utf-8").splitlines())
    for top in ("modules", "modules-plugable", "bundles/memar"):
        for path in sorted((TOP / top).rglob("*.py")):
            relative = path.relative_to(TOP)
            if "tests" not in relative.parts and "__pycache__" not in relative.parts:
                sizes[relative.as_posix()] = len(path.read_text(encoding="utf-8").splitlines())
    return sizes


class ScriptSize(unittest.TestCase):
    def test_no_new_file_over_the_mark(self) -> None:
        over = [name for name, lines in measured().items() if lines > MARK_LINES and name not in OVER_THE_MARK]
        self.assertEqual(over, [], f"over {MARK_LINES} lines: split each by concern rather than raise the mark")

    def test_no_stale_entry(self) -> None:
        sizes = measured()
        stale = [name for name in OVER_THE_MARK if sizes.get(name, 0) <= MARK_LINES]
        self.assertEqual(stale, [], "back under the mark: remove from OVER_THE_MARK")


if __name__ == "__main__":
    unittest.main()
