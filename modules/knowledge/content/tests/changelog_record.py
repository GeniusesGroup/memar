#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the reading of a changelog record in `modules/knowledge/content/services/changelog_record.py`,
and for the two verbs a human reviewer runs on it:
`modules/knowledge/content/services/list_ai_only_changelog_records.py` and
`modules/knowledge/content/services/add_human_approval_to_changelog_record.py`.

    python modules/knowledge/content/tests/changelog_record.py

The subject is one: a record's `Contributors` field read as changelog.md
defines it, and the human's approval added to it. The two verbs are tested here
beside the reading they share, per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md).

Nothing here writes outside its scratch folder: the ledger, its
CONTRIBUTORS.md, and the Memar root the lock lives under are all inside one.

What is pinned, and what each pin is for:

  ReadingTheRecords     Records are the `###` entries under `## Changelog`;
                        a heading inside a code fence is not one; each
                        contributor is the first link of a sub-bullet.
  WhoIsWho              A `##` section without `Full Legal Name` is a natural
                        person, one with it a legal entity, a `###` a brand or
                        tool; the Template is no one.
  ListingOneLedger      Only records every contributor of which is a brand or
                        tool are listed, with their number and line; a record
                        naming an unknown contributor is counted, not listed.
  OfferingTheNextLedger Without a file, the first ledger in path order that
                        holds such a record is offered; `--after` moves past one.
  AddingTheApproval     The approval is one sub-bullet appended to exactly the
                        chosen record's Contributors; every other byte stays;
                        the file's line endings are kept; a reviewer who is not
                        a natural person, a record that is not AI-only, and a
                        number out of range are refused with nothing written.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import modules.knowledge.content.services.add_human_approval_to_changelog_record as approve
import modules.knowledge.content.services.changelog_record as record
import modules.knowledge.content.services.list_ai_only_changelog_records as listing

CONTRIBUTORS = """# Contributors

## Template
- Full Legal Name: Legal entity name (legal persons only).

### {Brand}
- **Bio**: One line.

## Omid Hekayati
- **Bio**: Architect.

## Anthropic
- Full Legal Name: Anthropic, PBC

### Claude
- **Bio**: A model.

### Claude Code
- **Bio**: A tool.

## Zhipu
- Full Legal Name: Zhipu AI

### Super Z
- **Bio**: A model.
"""

LEDGER = """# Thing Changelog
Intro.

## Changelog

### First, by a person and a model
- Time: 2026-01-01T00:00:00Z
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Super Z](../CONTRIBUTORS.md#super-z) - rewrote

#### What changed
- One.

---

### Second, by a model alone
- Time: 2026-01-02T00:00:00Z
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (claude-x via [Claude Code](../CONTRIBUTORS.md#claude-code)) - drafted

#### What changed
```
### Not a record, inside a fence
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
```

---

### Third, by an unknown name
- Contributors:
  - [Ghost](../CONTRIBUTORS.md#ghost) - wrote

---

### Fourth, by two models
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) - argued
  - [Claude](../CONTRIBUTORS.md#claude) - applied

#### What changed
- Four.
"""


class Scratch(unittest.TestCase):
    """A checkout with `docs/`, a CONTRIBUTORS.md at its top, and ledgers under `docs/`."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "docs").mkdir()
        (self.root / "CONTRIBUTORS.md").write_text(CONTRIBUTORS, encoding="utf-8", newline="\n")
        self.ledger = self.write("docs/thing.changelog.md", LEDGER)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.root)
        patched.start()
        self.addCleanup(patched.stop)

    def write(self, name: str, text: str, newline: str = "\n") -> Path:
        path = self.root / name
        path.write_text(text, encoding="utf-8", newline=newline)
        return path

    def run_quietly(self, function, args) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            function(args)
        return out.getvalue()


class ReadingTheRecords(Scratch):
    def test_records_are_the_entries_under_the_changelog_heading(self) -> None:
        records = record.changelog_records(LEDGER)
        self.assertEqual(
            [item.title for item in records],
            ["First, by a person and a model", "Second, by a model alone", "Third, by an unknown name", "Fourth, by two models"],
        )
        self.assertEqual([item.number for item in records], [1, 2, 3, 4])

    def test_each_contributor_is_the_first_link_of_a_sub_bullet(self) -> None:
        second = record.changelog_records(LEDGER)[1]
        self.assertEqual([(c.name, c.anchor) for c in second.contributors], [("Claude", "claude")])
        self.assertEqual(second.contributors[0].target, "../CONTRIBUTORS.md")


class WhoIsWho(Scratch):
    def test_a_section_is_typed_by_its_level_and_its_legal_name(self) -> None:
        sections = record.contributor_sections(self.root / "CONTRIBUTORS.md")
        self.assertEqual(sections["omid-hekayati"].kind, record.NATURAL_PERSON)
        self.assertEqual(sections["anthropic"].kind, record.LEGAL_ENTITY)
        self.assertEqual(sections["claude"].kind, record.BRAND_OR_TOOL)
        self.assertEqual(sections["claude-code"].kind, record.BRAND_OR_TOOL)
        self.assertNotIn("template", sections)
        self.assertNotIn("brand", sections)


class ListingOneLedger(Scratch):
    def test_only_records_with_only_brand_or_tool_contributors_are_listed(self) -> None:
        found = record.ai_only_records(self.ledger)
        self.assertEqual([item.number for item in found.listed], [2, 4])
        self.assertEqual(found.total, 4)
        self.assertEqual([item.number for item in found.unknown], [3])

    def test_the_listing_names_number_line_and_title(self) -> None:
        text = self.run_quietly(listing.run, Namespace(file=str(self.ledger), after=None))
        self.assertIn("2 of 4 records have only AI contributors", text)
        self.assertIn(":17: 2 Second, by a model alone", text)
        self.assertIn(": 4 Fourth, by two models", text)
        self.assertNotIn("First", text)
        self.assertNotIn("Not a record", text)
        self.assertIn("1 record names a contributor CONTRIBUTORS.md does not hold: 3", text)


class OfferingTheNextLedger(Scratch):
    def setUp(self) -> None:
        super().setUp()
        self.clean = self.write("docs/a.changelog.md", "# A Changelog\n\n## Changelog\n\n### Only a person\n- Contributors:\n  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - wrote\n")
        self.later = self.write("docs/z.changelog.md", LEDGER)

    def test_the_first_ledger_holding_one_is_offered(self) -> None:
        text = self.run_quietly(listing.run, Namespace(file=None, after=None))
        self.assertIn("thing.changelog.md: 2 of 4", text)
        self.assertNotIn("a.changelog.md", text)
        self.assertIn("1 more ledger after it holds such records", text)

    def test_after_moves_past_a_ledger(self) -> None:
        text = self.run_quietly(listing.run, Namespace(file=None, after=str(self.ledger)))
        self.assertIn("z.changelog.md: 2 of 4", text)

    def test_none_left_says_so(self) -> None:
        text = self.run_quietly(listing.run, Namespace(file=None, after=str(self.later)))
        self.assertIn("no ledger", text)


class AddingTheApproval(Scratch):
    def args(self, **overrides) -> Namespace:
        values = dict(file=str(self.ledger), record=2, reviewer="omid-hekayati")
        values.update(overrides)
        return Namespace(**values)

    def test_the_approval_is_one_line_in_exactly_the_chosen_record(self) -> None:
        self.run_quietly(approve.run, self.args())
        line = "  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - approved\n"
        after = self.ledger.read_text(encoding="utf-8")
        anchor = "(claude-x via [Claude Code](../CONTRIBUTORS.md#claude-code)) - drafted\n"
        self.assertEqual(after, LEDGER.replace(anchor, anchor + line, 1))
        self.assertEqual([item.number for item in record.ai_only_records(self.ledger).listed], [4])

    def test_the_last_record_takes_it_too(self) -> None:
        self.run_quietly(approve.run, self.args(record=4))
        after = self.ledger.read_text(encoding="utf-8")
        self.assertIn("  - [Claude](../CONTRIBUTORS.md#claude) - applied\n  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - approved\n\n#### What changed\n- Four.\n", after)

    def test_the_line_endings_of_the_file_are_kept(self) -> None:
        self.write("docs/thing.changelog.md", LEDGER, newline="\r\n")
        self.run_quietly(approve.run, self.args())
        raw = self.ledger.read_bytes()
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        self.assertIn(b"- approved\r\n", raw)

    def refused(self, **overrides) -> None:
        before = self.ledger.read_bytes()
        with self.assertRaises(SystemExit):
            self.run_quietly(approve.run, self.args(**overrides))
        self.assertEqual(self.ledger.read_bytes(), before)
        self.assertEqual(list((self.root / "temp").rglob("*.lock")) if (self.root / "temp").exists() else [], [])

    def test_a_model_is_not_a_reviewer(self) -> None:
        self.refused(reviewer="claude")

    def test_a_legal_entity_is_not_a_reviewer(self) -> None:
        self.refused(reviewer="anthropic")

    def test_an_unknown_reviewer_is_refused(self) -> None:
        self.refused(reviewer="ghost")

    def test_a_record_a_person_contributed_to_is_refused(self) -> None:
        self.refused(record=1)

    def test_a_record_naming_an_unknown_contributor_is_refused(self) -> None:
        self.refused(record=3)

    def test_a_number_out_of_range_is_refused(self) -> None:
        self.refused(record=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
