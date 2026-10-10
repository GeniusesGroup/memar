#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the work-list of open propagations in `services/content_propagation.py`.

    python .agents/scripts/services/tests/content_propagation.py

The subject is the reading of a changelog's `Propagates to` field, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. Every ledger is written into
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again, and no test reads the repository's own ledgers.

What is pinned, and what each pin is for:

  PendingPropagation   A `Propagates to` entry in state `Pending` is
                      outstanding work the facet defined a searchable state
                      for, and this is the only surface that reports it:
                      `search` excludes changelog files by design, so the
                      work-list is otherwise invisible.
  SettledPropagation  `Done` and `Rejected` are closed states by the facet's
                      own definition, `Rejected` permanently, and neither is
                      outstanding work. Reporting them would train a reader to
                      ignore the section.
  PropagationIsAField The state is read from the entry's own field, so a
                      sentence that merely mentions `Pending` is not an open
                      obligation.
  LedgerNotSpec      `documentation-changelog.md` specifies the field and shows
                      its shape; `cognition.changelog.md` records entries in it.
                      Reading the first as the second reports the project's own
                      rules as its outstanding work.

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

import services.content_propagation as content_propagation


class LedgerFixture(unittest.TestCase):
    """A scratch tree to write ledgers into, cleaned up however the run ends."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path


class PendingPropagation(LedgerFixture):
    ENTRY = (
        "# Log\n\n## Changelog\n\n### A change\n"
        "- Propagates to:\n"
        "  - [modeling.md](./modeling.md): Pending - its local reasoning should\n"
        "    reference this document instead.\n"
    )

    def write_entry(self, text: str = ENTRY) -> Path:
        return self.write("docs/cognition.changelog.md", text)

    def found(self) -> list[tuple[Path, int, str]]:
        path = self.write_entry()
        return content_propagation.undischarged_propagations([path])

    def test_a_pending_entry_is_reported(self) -> None:
        found = self.found()
        self.assertEqual(len(found), 1, found)
        self.assertIn("modeling.md", found[0][2])
        self.assertEqual(found[0][1], 7)

    def test_the_report_names_the_entry_not_only_the_file(self) -> None:
        found = self.found()
        self.assertIn("Pending", found[0][2])
        self.assertIn("cognition.changelog.md", found[0][2])

    def test_a_wrapped_continuation_line_is_not_a_second_entry(self) -> None:
        found = self.found()
        self.assertEqual(len(found), 1, found)

    def test_a_file_without_the_field_reports_nothing(self) -> None:
        path = self.write("docs/cognition.md", "# Cognition\n- Propagates to nothing\n")
        self.assertEqual(content_propagation.undischarged_propagations([path]), [])

    def test_a_field_named_beside_the_artifact_is_not_an_entry(self) -> None:
        # The label appears in prose, not as the entry's own field.
        path = self.write("docs/cognition.changelog.md",
                          "# Log\nSee the Propagates to field for the states.\n")
        self.assertEqual(content_propagation.undischarged_propagations([path]), [])

    def test_a_non_changelog_file_is_not_scanned(self) -> None:
        path = self.write("docs/cognition.md", "# Cognition\n- other.md: Pending - owed\n")
        self.assertEqual(content_propagation.undischarged_propagations([path]), [])

    def test_the_facet_specification_is_not_read_as_a_ledger(self) -> None:
        # `documentation-changelog.md` is the document that specifies the field,
        # so it carries the heading, the example, and a sample line in the field's
        # own shape. It is a specification, and a check reading it as a ledger
        # would report the project's own rules as its outstanding work.
        path = self.write(
            "docs/documentation-changelog.md",
            "# Documentation Changelog\n\n## Changelog\n\n### Structure\n"
            "- Propagates to:\n  - {Other artifact}: Pending - {what needs to happen}\n",
        )
        self.assertEqual(content_propagation.undischarged_propagations([path]), [])

    def test_a_state_word_later_in_the_description_is_not_the_state(self) -> None:
        path = self.write(
            "docs/cognition.changelog.md",
            "# Log\n- Propagates to:\n"
            "  - modeling.md: Done - the entry it removed was Pending until this run.\n",
        )
        self.assertEqual(content_propagation.undischarged_propagations([path]), [])

    def test_a_pending_state_written_as_a_phrase_is_still_pending(self) -> None:
        # The facet's own sources write `Pending deletion` and `Pending at
        # absorb time`; both are open, and a check that missed them would
        # under-report against the material that exists.
        path = self.write(
            "docs/cognition.changelog.md",
            "# Log\n- Propagates to:\n"
            "  - protocol.per.md: Pending deletion - fully superseded by this document.\n",
        )
        self.assertEqual(len(content_propagation.undischarged_propagations([path])), 1)


class SettledPropagation(LedgerFixture):
    def settled(self, state: str) -> list[tuple[Path, int, str]]:
        path = self.write(
            "docs/cognition.changelog.md",
            f"# Log\n- Propagates to:\n  - modeling.md: {state} - why it was or was not done\n",
        )
        return content_propagation.undischarged_propagations([path])

    def test_done_is_not_outstanding(self) -> None:
        self.assertEqual(self.settled("Done"), [])

    def test_rejected_is_not_outstanding(self) -> None:
        # `Rejected` closes the search result permanently; reporting it would
        # put a decided matter back on the list every run.
        self.assertEqual(self.settled("Rejected"), [])

    def test_the_states_are_distinguished_in_the_matching_not_by_exclusion(self) -> None:
        path = self.write(
            "docs/cognition.changelog.md",
            "# Log\n- Propagates to:\n"
            "  - one.md: Pending - owed\n"
            "  - two.md: Done - landed\n"
            "  - three.md: Rejected - considered and deliberately not done\n"
            "  - four.md: Partial - some of it landed\n",
        )
        found = content_propagation.undischarged_propagations([path])
        self.assertEqual(len(found), 1, found)
        self.assertIn("one.md", found[0][2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
