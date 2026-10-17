#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the entry lint in `services/content_questions_lint.py`.

    python .agents/scripts/services/tests/content_questions_lint.py

The subject is the check that an Open Questions entry carries the fields
[Open Questions](../../../../modules/content/documentation/handoff/handoff.md#open-questions) names
for an entry written during a task: State, Options, Anchor and Blocks. A missing
one is a warning, never an error: the entries written before the rule stay valid.

What is pinned:

  FieldsAreRequired   An entry missing State, Options, Anchor or Blocks is
                      warned about, naming its line, heading and the missing
                      fields; a complete one is not; both bold and plain field
                      markers count; the older `Blocks continuation` counts as
                      Blocks.
  OnlyEntriesCount    Text outside `Open Questions`, fenced headings, and a file
                      with no such section give no warning.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import services.content_questions_lint as lint

COMPLETE = """# T handoff

## Open Questions
### Whole?
- **State**: x
- **Options**: a, b
- **Anchor**: f.md:1
- **Blocks**: nothing
- **Asked**: 2026-10-13, Claude
"""


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)

    def write(self, text: str) -> Path:
        path = Path(self.scratch.name) / "t.handoff.md"
        path.write_text(text, encoding="utf-8", newline="\n")
        return path


class FieldsAreRequired(Fixture):
    def test_a_complete_entry_is_clean(self) -> None:
        self.assertEqual(lint.entry_warnings(self.write(COMPLETE)), [])

    def test_a_missing_field_is_named_with_line_and_heading(self) -> None:
        text = COMPLETE.replace("- **Options**: a, b\n", "").replace("- **Anchor**: f.md:1\n", "")
        self.assertEqual(
            lint.entry_warnings(self.write(text)),
            ["line 4: entry 'Whole?' lacks Options, Anchor"],
        )

    def test_plain_markers_and_the_older_blocks_name_count(self) -> None:
        text = "## Open Questions\n### Q?\n- State: x\n- Options: a\n- Anchor: y\n- Blocks continuation: no\n"
        self.assertEqual(lint.entry_warnings(self.write(text)), [])

    def test_a_colon_inside_the_bold_counts(self) -> None:
        text = "## Open Questions\n### Q?\n- **State:** x\n- **Options:** a\n- **Anchor:** y\n- **Blocks:** no\n"
        self.assertEqual(lint.entry_warnings(self.write(text)), [])

    def test_a_bare_entry_lacks_all_four(self) -> None:
        text = "## Open Questions\n### Q?\nJust a paragraph.\n"
        self.assertEqual(
            lint.entry_warnings(self.write(text)),
            ["line 2: entry 'Q?' lacks State, Options, Anchor, Blocks"],
        )


class OnlyEntriesCount(Fixture):
    def test_text_outside_the_section_and_fenced_headings_give_nothing(self) -> None:
        text = ("# T\n\n### Not an entry\n\n## Open Questions\n```\n### fenced\n```\n"
                "### Whole?\n- State: x\n- Options: a\n- Anchor: y\n- Blocks: no\n\n## Notes\n### Other\n")
        self.assertEqual(lint.entry_warnings(self.write(text)), [])

    def test_a_file_with_no_section_gives_nothing(self) -> None:
        self.assertEqual(lint.entry_warnings(self.write("# T\n\nBody\n")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
