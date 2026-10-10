#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content changelog-append` in `services/content_changelog_append.py`.

    python .agents/scripts/services/tests/content_changelog_append.py

The subject is the append to a ledger, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: every ledger is written into
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  ChangelogAppendKeeps  The appended bytes are the ones the ledger already
  TheFilesConvention    holds: the practice tells every contributor to append
                        through this verb, and `check` reports mixed line
                        endings, so an append in the host's convention would
                        be the tool causing the defect it detects.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import services.content_changelog_append as content_changelog_append
import services.content_check as content_check


class ChangelogAppendKeepsTheFilesConvention(unittest.TestCase):
    """The appended bytes must be the ones the file already holds.

    The practice tells every contributor to append through this script, and
    `check` reports mixed line endings. An append that wrote the host's
    convention rather than the file's would therefore be the tool causing the
    very defect it is the authority for detecting.
    """

    ENTRY = "### A change\n- What changed: nothing an entry can say.\n"

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def problems(self, path: Path) -> list[str]:
        return content_check.check_file(path, {})

    def ledger(self, newline: str) -> Path:
        path = self.root / "docs" / "cognition.changelog.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            ("# Log\n\n## Changelog\n\n### Earlier\n- older.\n").encode("utf-8")
            .replace(b"\n", newline.encode("ascii"))
        )
        return path

    def test_a_crlf_ledger_gains_no_lf(self) -> None:
        path = self.ledger("\r\n")
        content_changelog_append.changelog_append(path, self.ENTRY)
        self.assertEqual(self.problems(path), [])

    def test_an_lf_ledger_gains_no_crlf(self) -> None:
        path = self.ledger("\n")
        content_changelog_append.changelog_append(path, self.ENTRY)
        self.assertEqual(self.problems(path), [])

    def test_a_crlf_entry_written_into_an_lf_ledger_is_normalized(self) -> None:
        path = self.ledger("\n")
        content_changelog_append.changelog_append(path, self.ENTRY.replace("\n", "\r\n"))
        self.assertEqual(self.problems(path), [])

    def test_the_entry_is_still_appended_after_the_earlier_one(self) -> None:
        path = self.ledger("\r\n")
        content_changelog_append.changelog_append(path, self.ENTRY)
        text = path.read_bytes().decode("utf-8")
        self.assertLess(text.index("### Earlier"), text.index("### A change"))
        self.assertIn("---", text)

    def test_the_appended_entry_is_not_written_over_an_existing_one(self) -> None:
        path = self.ledger("\r\n")
        content_changelog_append.changelog_append(path, self.ENTRY)
        first = path.read_bytes()
        content_changelog_append.changelog_append(path, self.ENTRY)
        self.assertGreater(len(path.read_bytes()), len(first))


if __name__ == "__main__":
    unittest.main(verbosity=2)
