#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the checkout's corpus in `services/content_corpus.py`.

    python .agents/scripts/services/tests/content_corpus.py

The subject is which files of a checkout are its content and which its ledgers,
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: every checkout is laid out in
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again, and no test walks the repository's own tree.

What is pinned, and what each pin is for:

  CorpusIsTheCheckout  The boundary is the whole checkout — `docs/`, `modules/`,
                       `bundles/`, `.agents/` — because a tool named for content that could
                       not search code would be a tool for documents. Pinned
                       per folder, because a tool that quietly stopped at
                       `docs/` reported a narrower world under the wider name.
                       Generated and dependency folders stay out by the decision
                       already written for the two things that copy a checkout,
                       and the work-list reads every ledger of the checkout,
                       not only the ones under `docs/`.

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

import services.content_corpus as content_corpus


class CorpusIsTheCheckout(unittest.TestCase):
    """The corpus is the whole checkout, so the tool's name is not narrower than its reach.

    `docs/` is where the model is argued, not where the repository's content
    ends: the model definitions, the rule catalog, the protocol implementations
    and the sources all live under `modules/`, what runs or aggregates them
    under `bundles/`, and the configuration a session is driven by lives under
    `.agents/`. A tool named for content that could not reach them reported a
    narrower world under the wider name.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def a_checkout(self) -> Path:
        for folder in ("docs", "modules", "bundles", ".agents"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        (self.root / "README.md").write_text("# R\n", encoding="utf-8", newline="\n")
        return self.root

    def test_the_corpus_reaches_each_folder_the_content_lives_in(self) -> None:
        root = self.a_checkout()
        for folder in ("docs", "modules", "bundles", ".agents"):
            self.write(f"{folder}/note.md", "# Note\n")
        self.write("README.md", "# R\n")
        found = {path.relative_to(root).parts[0] for path in content_corpus.content_files(root)}
        self.assertEqual(found, {"docs", "modules", "bundles", ".agents", "README.md"})

    def test_a_folder_that_is_not_content_stays_out(self) -> None:
        # A dependency tree or a session's scratch is not this repository's
        # content even when it holds Markdown, and the decision is asked of the
        # module that already makes it for the two things that copy a checkout.
        # Named by path rather than by file name, because the vendored file is
        # also called README.md and the root one is also called README.md.
        root = self.a_checkout()
        self.write("docs/kept.md", "# Kept\n")
        self.write("node_modules/vendored/vendored.md", "# Vendored\n")
        self.write("temp/s-1/scratch.md", "# Scratch\n")
        self.write("temp/sessions/s-2/plan.md", "# Plan\n")
        found = {
            path.relative_to(root).as_posix() for path in content_corpus.content_files(root)
        }
        self.assertIn("docs/kept.md", found)
        self.assertNotIn("node_modules/vendored/vendored.md", found)
        self.assertNotIn("temp/s-1/scratch.md", found)
        self.assertNotIn("temp/sessions/s-2/plan.md", found)

    def test_a_folder_holding_none_of_the_content_folders_is_refused(self) -> None:
        empty = self.root / "not-a-checkout"
        empty.mkdir()
        with self.assertRaises(SystemExit) as raised:
            content_corpus.content_files(empty)
        self.assertIn("not a Memar checkout", str(raised.exception))

    def test_the_search_corpus_excludes_ledgers_and_ledgers_are_still_reachable(self) -> None:
        # `search` excludes changelogs by design so a reader is not sent into
        # history instead of into explanation — and the work-list still reads
        # every one of them, or a propagation owed under `modules/` would be
        # invisible.
        root = self.a_checkout()
        self.write("docs/one.changelog.md", "# One\n")
        self.write("modules/two.changelog.md", "# Two\n")
        searched = {path.name for path in content_corpus.content_files(root)}
        ledgers = {path.name for path in content_corpus.ledger_files(root)}
        self.assertNotIn("one.changelog.md", searched)
        self.assertEqual(ledgers, {"one.changelog.md", "two.changelog.md"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
