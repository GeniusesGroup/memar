#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content list-undischarged-propagations` in `modules-plugable/knowledge/documentation/services/content_list_undischarged_propagations.py`.

    python modules-plugable/knowledge/documentation/tests/content_obligations.py

The subject is the work-list as a query, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: every ledger is written into
one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  ObligationsAreQueryable  The Pending work-list prints as path:line hits, the
                           whole set by default and a named subset when files
                           are given. Which states are open is pinned by
                           `content_propagation.py`'s suite.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_obligations = import_module('modules-plugable.knowledge.documentation.services.content_list_undischarged_propagations')

class ObligationsAreQueryable(unittest.TestCase):
    """`obligations` prints the Pending work-list as path:line hits.

    The states are already pinned under PendingPropagation and
    SettledPropagation; what is pinned here is only the query shape: one hit
    per line with the repository-relative path first, the whole set by
    default, and a named subset when files are given.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def test_pending_entries_print_as_path_line_hits(self) -> None:
        self.write('docs/cognition.changelog.md', '# Log\n- Propagates to:\n  - modeling.md: Pending - owed\n')
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_obligations.cmd_obligations(Namespace(files=[]), self.root)
        self.assertIn(f"{Path('docs/cognition.changelog.md')}:3: modeling.md: Pending — not yet done", printed.getvalue())

    def test_settled_entries_print_nothing_outstanding(self) -> None:
        self.write('docs/cognition.changelog.md', '# Log\n- Propagates to:\n  - modeling.md: Done - landed\n')
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_obligations.cmd_obligations(Namespace(files=[]), self.root)
        self.assertIn('(no undischarged obligations)', printed.getvalue())

    def test_named_files_narrow_the_read(self) -> None:
        self.write('docs/a.changelog.md', '# Log\n- Propagates to:\n  - x.md: Pending - owed\n')
        self.write('docs/b.changelog.md', '# Log\n- Propagates to:\n  - y.md: Pending - owed\n')
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_obligations.cmd_obligations(Namespace(files=['docs/a.changelog.md']), self.root)
        out = printed.getvalue()
        self.assertIn('x.md: Pending', out)
        self.assertNotIn('y.md', out)
if __name__ == '__main__':
    unittest.main(verbosity=2)
