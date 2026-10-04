#!/usr/bin/env python3
"""Tests for `check`'s judgement of the links a document makes and of the
obligations a document set has recorded but not yet discharged.

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
  RejectedInABody    Whether a body holds a rejected-alternative record is not
  IsNotJudged        decidable from the text, and is deliberately not checked.
                      The specification of the field and a record in the field
                      differ only in what the text is for. The class is pinned
                      in `RejectedInABodyIsNotJudged` so the question is not
                      reopened blind.
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


class PendingPropagation(LinkFixture):
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
        return memar_documentation.undischarged_propagations([path])

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
        self.assertEqual(memar_documentation.undischarged_propagations([path]), [])

    def test_a_field_named_beside_the_artifact_is_not_an_entry(self) -> None:
        # The label appears in prose, not as the entry's own field.
        path = self.write("docs/cognition.changelog.md",
                          "# Log\nSee the Propagates to field for the states.\n")
        self.assertEqual(memar_documentation.undischarged_propagations([path]), [])

    def test_a_non_changelog_file_is_not_scanned(self) -> None:
        path = self.write("docs/cognition.md", "# Cognition\n- other.md: Pending - owed\n")
        self.assertEqual(memar_documentation.undischarged_propagations([path]), [])

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
        self.assertEqual(memar_documentation.undischarged_propagations([path]), [])

    def test_a_state_word_later_in_the_description_is_not_the_state(self) -> None:
        path = self.write(
            "docs/cognition.changelog.md",
            "# Log\n- Propagates to:\n"
            "  - modeling.md: Done - the entry it removed was Pending until this run.\n",
        )
        self.assertEqual(memar_documentation.undischarged_propagations([path]), [])

    def test_a_pending_state_written_as_a_phrase_is_still_pending(self) -> None:
        # The facet's own sources write `Pending deletion` and `Pending at
        # absorb time`; both are open, and a check that missed them would
        # under-report against the material that exists.
        path = self.write(
            "docs/cognition.changelog.md",
            "# Log\n- Propagates to:\n"
            "  - protocol.per.md: Pending deletion - fully superseded by this document.\n",
        )
        self.assertEqual(len(memar_documentation.undischarged_propagations([path])), 1)


class SettledPropagation(LinkFixture):
    def settled(self, state: str) -> list[tuple[Path, int, str]]:
        path = self.write(
            "docs/cognition.changelog.md",
            f"# Log\n- Propagates to:\n  - modeling.md: {state} - why it was or was not done\n",
        )
        return memar_documentation.undischarged_propagations([path])

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
        found = memar_documentation.undischarged_propagations([path])
        self.assertEqual(len(found), 1, found)
        self.assertIn("one.md", found[0][2])


class RejectedInABodyIsNotJudged(LinkFixture):
    """The negative result, pinned so a later session does not retry it blind.

    Whether a body holds a rejected-alternative record is not decidable from
    the text: the document that *specifies* the field carries a section by the
    field's name in its own body. So no such check exists, and these two tests
    say which way each candidate shape is expected to fall if one is ever
    written — the specification's own heading, and a body naming the field's
    home — rather than leaving the question open again.
    """

    def test_the_facet_specification_carries_the_heading_and_is_clean(self) -> None:
        # This is the shape that ruled the check out: a real section of a real
        # document, correctly placed, and indistinguishable by pattern from the
        # violation the check was meant to catch.
        path = self.write(
            "docs/documentation-changelog.md",
            "# Documentation Changelog\n## Optional Sections\n"
            "#### Considered and not done\n- alternatives examined and rejected\n",
        )
        self.assertEqual(self.problems(path), [])

    def test_a_body_naming_the_fields_home_is_clean(self) -> None:
        path = self.write(
            "docs/cognition.md",
            "# Cognition\n## Rules\nA rejected alternative belongs in the changelog "
            "entry's `Considered and not done` section.\n",
        )
        self.assertEqual(self.problems(path), [])


class ChangelogAppendKeepsTheFilesConvention(LinkFixture):
    """The appended bytes must be the ones the file already holds.

    The practice tells every contributor to append through this script, and
    `check` reports mixed line endings. An append that wrote the host's
    convention rather than the file's would therefore be the tool causing the
    very defect it is the authority for detecting.
    """

    ENTRY = "### A change\n- What changed: nothing an entry can say.\n"

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
        memar_documentation.changelog_append(path, self.ENTRY)
        self.assertEqual(self.problems(path), [])

    def test_an_lf_ledger_gains_no_crlf(self) -> None:
        path = self.ledger("\n")
        memar_documentation.changelog_append(path, self.ENTRY)
        self.assertEqual(self.problems(path), [])

    def test_a_crlf_entry_written_into_an_lf_ledger_is_normalized(self) -> None:
        path = self.ledger("\n")
        memar_documentation.changelog_append(path, self.ENTRY.replace("\n", "\r\n"))
        self.assertEqual(self.problems(path), [])

    def test_the_entry_is_still_appended_after_the_earlier_one(self) -> None:
        path = self.ledger("\r\n")
        memar_documentation.changelog_append(path, self.ENTRY)
        text = path.read_bytes().decode("utf-8")
        self.assertLess(text.index("### Earlier"), text.index("### A change"))
        self.assertIn("---", text)

    def test_the_appended_entry_is_not_written_over_an_existing_one(self) -> None:
        path = self.ledger("\r\n")
        memar_documentation.changelog_append(path, self.ENTRY)
        first = path.read_bytes()
        memar_documentation.changelog_append(path, self.ENTRY)
        self.assertGreater(len(path.read_bytes()), len(first))


class WalkLooksOnlyAtWhatTheProjectOwns(LinkFixture):
    """A folder run skips what a copy of this project never carries.

    An installed dependency tree is not this repository's work, and a report that
    raises the same problems inside it on every run is a report about the tool
    rather than about the tree — after long enough it is a report nobody reads.
    The patterns come from `copy_excluded`, which already holds that answer for
    the two things that copy part of a checkout elsewhere; a second list here
    would be a second answer to one question.

    Naming a file explicitly still checks it. A walk is how the tool chooses for
    itself; a named path is a decision somebody already made.
    """

    def install(self, relative: str, text: str = "x") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def test_a_dependency_tree_is_not_walked(self) -> None:
        self.install("node_modules/dep/package.json", '{"name": "dep"}\n')
        self.install("notes.md", "# Notes\n")
        walked = [p.relative_to(self.root).as_posix()
                  for p in memar_documentation.checkable_files(self.root)]
        self.assertIn("notes.md", walked)
        self.assertFalse([p for p in walked if p.startswith("node_modules/")], walked)

    def test_a_generated_folder_is_not_walked(self) -> None:
        for name in ("__pycache__", ".DS_Store"):
            with self.subTest(name=name):
                self.install(f"{name}/thing.py", "x = 1\n")
                walked = [p.relative_to(self.root).as_posix()
                          for p in memar_documentation.checkable_files(self.root)]
                self.assertFalse([p for p in walked if p.startswith(name)], walked)

    def test_a_file_inside_an_owned_folder_is_still_walked(self) -> None:
        self.install("src/deep/module.py", "x = 1\n")
        walked = [p.relative_to(self.root).as_posix()
                  for p in memar_documentation.checkable_files(self.root)]
        self.assertIn("src/deep/module.py", walked)

    def test_a_named_file_is_checked_whatever_folder_it_is_in(self) -> None:
        # The distinction the whole rule turns on: a walk chooses, a name does not.
        path = self.install("node_modules/dep/broken.md", "# T\n\n\nbody\n")
        self.assertTrue(self.problems(path))

    def test_the_patterns_are_the_ones_the_folder_already_states(self) -> None:
        # A copy of the list here would be a second answer to one question.
        from copy_excluded import NEVER_COPIED_PATTERNS

        self.assertEqual(
            set(memar_documentation.NEVER_COPIED_PATTERNS),
            set(NEVER_COPIED_PATTERNS),
        )
        for pattern in ("__pycache__", "*.pyc", ".DS_Store", "node_modules"):
            self.assertIn(pattern, NEVER_COPIED_PATTERNS)


if __name__ == "__main__":
    unittest.main()
