#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the section a heading's anchor names, in `services/content_section.py`.

    python .agents/scripts/services/tests/content_section.py

The subject is `by_anchor`, which reads a section by the fragment a link uses
rather than by the heading's text, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
Nothing here touches the filesystem.

What is pinned, and what each pin is for:

  ByAnchor   A heading is found by its slug, the heading line is part of what
             is returned, and the section runs to the next heading at its
             level or above; a `#` inside a fenced block is no heading; an
             anchor no heading answers to is None.
  Through    With a last heading, the text runs on to the end of that
             section, so neighbouring sections are one read; a last heading
             that is not after the first is None.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
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

from services.content_section import by_anchor

TEXT = """# Title

## Alpha Part
alpha text
### Inner (Detail)
inner text

## Beta Part
```
## not a heading
```
beta text

## Gamma Part
gamma text
"""


class ByAnchor(unittest.TestCase):
    def test_a_section_is_found_by_its_slug_with_its_heading_line_and_runs_to_the_next_at_its_level(self) -> None:
        found = by_anchor(TEXT, "alpha-part")
        self.assertTrue(found.startswith("## Alpha Part"))
        self.assertIn("inner text", found)
        self.assertNotIn("beta text", found)

    def test_a_deeper_heading_is_found_and_ends_at_the_next_heading_above_it(self) -> None:
        found = by_anchor(TEXT, "inner-detail")
        self.assertEqual(found, "### Inner (Detail)\ninner text")

    def test_a_hash_inside_a_fenced_block_is_no_heading(self) -> None:
        found = by_anchor(TEXT, "beta-part")
        self.assertIn("## not a heading", found)
        self.assertIn("beta text", found)
        self.assertIsNone(by_anchor(TEXT, "not-a-heading"))

    def test_an_anchor_no_heading_answers_to_is_none(self) -> None:
        self.assertIsNone(by_anchor(TEXT, "nowhere"))

    def test_an_anchor_may_carry_its_hash(self) -> None:
        self.assertEqual(by_anchor(TEXT, "#gamma-part"), by_anchor(TEXT, "gamma-part"))


class Through(unittest.TestCase):
    def test_the_text_runs_on_to_the_end_of_the_last_section(self) -> None:
        found = by_anchor(TEXT, "alpha-part", "Beta Part")
        self.assertIn("alpha text", found)
        self.assertIn("beta text", found)
        self.assertNotIn("gamma text", found)

    def test_a_last_heading_that_is_not_after_the_first_is_none(self) -> None:
        self.assertIsNone(by_anchor(TEXT, "gamma-part", "Alpha Part"))
        self.assertIsNone(by_anchor(TEXT, "alpha-part", "No Such Heading"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
