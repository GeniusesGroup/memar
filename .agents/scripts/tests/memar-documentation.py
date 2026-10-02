#!/usr/bin/env python3
"""Tests for `check`'s judgement of the links a document makes.

    python .agents/scripts/tests/memar-documentation.py

The subject is the `check` subcommand of `memar-documentation.py`, named for the
file that holds it per [Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. Every document is written into a scratch
folder inside this one and removed again, and no test reads the repository's own
`docs/`: a test that asserts against the tree stops being a test of the rule and
becomes a report on whatever the tree currently holds.

What is pinned, and what each pin is for:

  ReachableLink       A relative link whose target is beside the document is
                      not a problem. The whole point of the check is to report
                      what a reader cannot follow, so a check that reported
                      sound links would be worse than none.
  MovedDocument       The reason the check exists. A document moved one folder
                      deep leaves its links naming files that are no longer
                      there, and the link itself is unchanged text — nothing
                      about reading the document tells you it broke.
  NamedHeading        A link to another document names a heading, and the
                      heading is checked in the document the link names rather
                      than in the one holding the link. Half a link resolving
                      is a reader landing somewhere real and wrong.
  SharedCacheAnswers  Every link to one document gets the same answer, and the
                      document is read once to give it: a cache keyed by
                      anything other than the file would let one document's
                      headings answer for another's.
  UnreadableTarget    A target this run cannot read is not reported as a
                      document with no such heading. Silence is the honest
                      answer there, and a wrong report is worse than none.
  CodeIsNotALink      A link written inside backticks or a fenced block is text
                      about links. The same text as a real link must be judged
                      differently only by where it is, never by what it says.
  ExternalIsNotJudged A URI with a scheme, and a site-root path, are not files
                      this run can resolve and are left alone.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

_spec = importlib.util.spec_from_file_location(
    "memar_documentation", SCRIPTS / "memar-documentation.py"
)
memar_documentation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memar_documentation)


class LinkFixture(unittest.TestCase):
    """A scratch tree to write documents into, cleaned up however the run ends."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def problems(self, path: Path) -> list[str]:
        return memar_documentation.check_file(path, self.cache)

    def only_link_problems(self, path: Path) -> list[str]:
        return [p for p in self.problems(path)
                if "does not exist" in p or "names no heading" in p]


class ReachableLink(LinkFixture):
    def test_sibling_link_is_not_reported(self) -> None:
        self.write("other.md", "# Other\n")
        path = self.write("base.md", "# Base\nSee [Other](./other.md).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_parent_and_grandparent_links_are_not_reported(self) -> None:
        self.write("deep/target.md", "# Target\n")
        path = self.write("deep/inner/base.md",
                          "# Base\n[Up](../target.md) and [Out](../../deep/target.md).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_directory_target_is_not_reported(self) -> None:
        self.write("modules/math/one.kh", "")
        path = self.write("base.md", "# Base\n[Modules](./modules/math/).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_non_markdown_target_needs_no_anchor(self) -> None:
        self.write("code.kh", "tp X\n")
        path = self.write("base.md", "# Base\n[Code](./code.kh#anything).\n")
        self.assertEqual(self.only_link_problems(path), [])


class MovedDocument(LinkFixture):
    def test_target_one_folder_short_is_reported(self) -> None:
        # The link says `target.md` sits beside this document; it does not, and
        # the document it names was moved a folder deeper.
        self.write("area/deeper/target.md", "# Target\n")
        path = self.write("area/base.md", "# Base\nSee [Target](./target.md).\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("./target.md does not exist", found[0])
        self.assertIn("line 2", found[0])

    def test_a_link_to_a_real_sibling_is_not_reported(self) -> None:
        # The other half of the same case: repointing the link is what fixes it,
        # so the check must accept the repaired form rather than the shape.
        self.write("area/deeper/target.md", "# Target\n")
        path = self.write("area/base.md",
                          "# Base\nSee [Target](./deeper/target.md).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_contributors_link_out_of_a_subfolder_is_reported(self) -> None:
        # The shape that actually shipped broken: one hop short of the root,
        # which resolves to a file that was never there.
        self.write("CONTRIBUTORS.md", "# Contributors\n")
        path = self.write("docs/protocols/net/http.changelog.md",
                          "# Log\n- [Owner](../../CONTRIBUTORS.md#owner)\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("../../CONTRIBUTORS.md does not exist", found[0])

    def test_the_same_link_from_the_right_depth_is_not_reported(self) -> None:
        self.write("CONTRIBUTORS.md", "# Contributors\n### Owner\n")
        path = self.write("docs/protocols/net/http.changelog.md",
                          "# Log\n- [Owner](../../../CONTRIBUTORS.md#owner)\n")
        self.assertEqual(self.only_link_problems(path), [])


class NamedHeading(LinkFixture):
    def test_anchor_is_checked_in_the_named_document(self) -> None:
        self.write("target.md", "# Target\n## The Part\n")
        path = self.write("base.md", "# Base\n[Part](./target.md#the-part).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_anchor_absent_from_the_named_document_is_reported(self) -> None:
        self.write("target.md", "# Target\n## The Part\n")
        path = self.write("base.md", "# Base\n[Gone](./target.md#the-gone).\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("names no heading in ./target.md", found[0])

    def test_anchor_present_only_in_the_holding_document_is_reported(self) -> None:
        # The failure a path-only check would miss: both files resolve, and the
        # heading the link wants is one the reader's own document happens to have.
        self.write("target.md", "# Target\n")
        path = self.write("base.md", "# Base\n## Elsewhere\n[X](./target.md#elsewhere).\n")
        self.assertEqual(len(self.only_link_problems(path)), 1)

    def test_existence_is_reported_before_the_anchor(self) -> None:
        path = self.write("base.md", "# Base\n[X](./gone.md#somewhere).\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("does not exist", found[0])


class SharedCacheAnswers(LinkFixture):
    def test_one_read_serves_every_link_to_that_document(self) -> None:
        target = self.write("target.md", "# Target\n## The Part\n")
        readers = [
            self.write(f"base{index}.md",
                       f"# Base\n[A](./target.md#the-part)\n[B](./target.md#the-part)\n")
            for index in range(3)
        ]
        for path in readers:
            self.assertEqual(self.only_link_problems(path), [])
        self.assertEqual(sum(1 for key in self.cache if key == str(target)), 1)

    def test_cache_is_keyed_by_the_file_not_by_the_link(self) -> None:
        # Two documents, two identical-looking links, two different answers.
        self.write("one.md", "# One\n## Shared\n")
        self.write("two.md", "# Two\n")
        good = self.write("a.md", "# A\n[X](./one.md#shared).\n")
        bad = self.write("b.md", "# B\n[X](./two.md#shared).\n")
        self.assertEqual(self.only_link_problems(good), [])
        self.assertEqual(len(self.only_link_problems(bad)), 1)

    def test_a_second_run_reaches_the_same_answer(self) -> None:
        self.write("target.md", "# Target\n")
        path = self.write("base.md", "# Base\n[X](./target.md#gone).\n")
        first = self.only_link_problems(path)
        self.assertEqual(len(first), 1, first)
        # Reusing the cache must not turn a found problem into a silent one.
        self.assertEqual(first, self.only_link_problems(path))


class UnreadableTarget(LinkFixture):
    def test_invalid_utf8_target_is_not_reported_as_a_missing_heading(self) -> None:
        target = self.root / "target.md"
        target.write_bytes(b"# Target\n## \xff\xfe not utf-8\n")
        path = self.write("base.md", "# Base\n[X](./target.md#anything).\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_missing_target_is_still_reported_when_the_read_would_fail(self) -> None:
        path = self.write("base.md", "# Base\n[X](./target.md#anything).\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("does not exist", found[0])


class CodeIsNotALink(LinkFixture):
    def test_link_shown_inside_a_code_span_is_not_a_link(self) -> None:
        path = self.write("base.md",
                          "# Base\nWrite `[X](./gone.md)` and it resolves.\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_link_shown_inside_a_fence_is_not_a_link(self) -> None:
        path = self.write("base.md",
                          "# Base\n```\n[X](./gone.md#gone)\n```\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_real_link_beside_a_shown_one_is_still_judged(self) -> None:
        path = self.write("base.md",
                          "# Base\n`[X](./gone.md)` but [Y](./gone.md) is real.\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("./gone.md does not exist", found[0])


class ExternalIsNotJudged(LinkFixture):
    def test_links_with_a_scheme_are_left_alone(self) -> None:
        path = self.write("base.md",
                          "# Base\n[A](https://example.invalid/x) "
                          "[B](mailto:a@example.invalid) "
                          "[C](//cdn.example.invalid/x)\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_site_root_path_is_left_alone(self) -> None:
        path = self.write("base.md", "# Base\n[A](/docs/cognition.md)\n")
        self.assertEqual(self.only_link_problems(path), [])


class InPageAnchorStillJudged(LinkFixture):
    def test_in_page_anchor_is_reported_by_the_original_pass(self) -> None:
        path = self.write("base.md", "# Base\n## Real\n[X](#real)\n[Y](#gone)\n")
        found = [p for p in self.problems(path) if "in-page anchor" in p]
        self.assertEqual(len(found), 1, found)
        self.assertIn("#gone", found[0])

    def test_both_passes_run_on_one_document(self) -> None:
        self.write("target.md", "# Target\n")
        path = self.write("base.md",
                          "# Base\n## Real\n[X](#nowhere) and [Y](./target.md#gone)\n")
        found = self.problems(path)
        self.assertEqual(len(found), 2, found)
        self.assertTrue(any("in-page anchor" in p for p in found))
        self.assertTrue(any("names no heading" in p for p in found))


if __name__ == "__main__":
    unittest.main()
