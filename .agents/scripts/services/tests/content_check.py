#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content check` in `services/content_check.py`: its judgement of links, its walk, and its rule sets.

    python .agents/scripts/services/tests/content_check.py

The subject is the checker, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. Every document is written into
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again, and no test reads the repository's own
`docs/`: a test that asserts against the tree stops being a test of the rule and
becomes a report on whatever the tree currently holds.

What is pinned, and what each pin is for:

  LinkStandIn         A folder README that git records as a symlink and a
                      checkout without symlink support writes as a text file
                      holding only its target, with no final newline, is not
                      judged as text; any other file, or a README naming
                      nothing beside it, still is.
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
  ExternalIsNotJudged A URI with a scheme, and a protocol-relative `//host`,
                      are not files this run can resolve and are left alone.
  RootRelativeIsJudged A link from the checkout's root (`/docs/...`) is
                      judged, file and anchor, against the root the run is
                      given, as `memar content path` resolves it.
  RejectedInABody    Whether a body holds a rejected-alternative record is not
  IsNotJudged        decidable from the text, and is deliberately not checked.
                       The specification of the field and a record in the field
                       differ only in what the text is for. The class is pinned
                       in `RejectedInABodyIsNotJudged` so the question is not
                       reopened blind.
  WalkLooksOnlyAt     A folder run skips what a copy of this project never
  WhatTheProjectOwns  carries, by the decision already written for the two
                      things that copy a checkout; a named file is still
                      checked.
  MemarRulesAutoDetect  Without a flag the folder decides: inside a Memar
                       repository the Markdown conventions apply, outside only
                       encoding and newlines do; an explicit flag wins.
  HandoffEntriesAreWarnedAbout  An Open Questions entry missing State, Options,
                      Anchor or Blocks is a warning printed apart from the
                      problems and never changing the exit; inside a Memar
                      repository and in `*.handoff.md` only.
  CitationDirection   A relative link from the base to the modules is a
                      warning, per Documentation -> Citation Direction: a
                      debt, never a problem and never a changed exit; a
                      link within a layer or down to the base, a path in a
                      code span, a README pointing into its own folder, and
                      files outside the layers are not warned about.

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

import services.content_check as content_check


class LinkFixture(unittest.TestCase):
    """A scratch tree to write documents into, cleaned up however the run ends."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def problems(self, path: Path) -> list[str]:
        return content_check.check_file(path, self.cache, root=self.root)

    def only_link_problems(self, path: Path) -> list[str]:
        return [p for p in self.problems(path)
                if "does not exist" in p or "names no heading" in p]


class LinkStandIn(LinkFixture):
    """A README that git records as a symlink is a text file naming its target on a checkout without symlink support."""

    def test_a_readme_holding_only_its_siblings_name_is_clean(self) -> None:
        self.write("m/m.md", "# M\n")
        stand_in = self.root / "m" / "README.md"
        stand_in.write_bytes(b"m.md")
        self.assertEqual(self.problems(stand_in), [])

    def test_a_readme_naming_nothing_there_is_judged_as_text(self) -> None:
        self.write("m/m.md", "# M\n")
        stand_in = self.root / "m" / "README.md"
        stand_in.write_bytes(b"gone.md")
        self.assertIn("no newline at end of file", self.problems(stand_in))

    def test_another_file_with_the_same_content_is_judged_as_text(self) -> None:
        self.write("m/m.md", "# M\n")
        other = self.root / "m" / "notes.md"
        other.write_bytes(b"m.md")
        self.assertIn("no newline at end of file", self.problems(other))


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
        path = self.write("modules/net/chapar/chapar.changelog.md",
                          "# Log\n- [Owner](../../CONTRIBUTORS.md#owner)\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("../../CONTRIBUTORS.md does not exist", found[0])

    def test_the_same_link_from_the_right_depth_is_not_reported(self) -> None:
        self.write("CONTRIBUTORS.md", "# Contributors\n### Owner\n")
        path = self.write("modules/net/chapar/chapar.changelog.md",
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


class RootRelativeIsJudged(LinkFixture):
    """A link from the checkout's root (`/docs/...`) is judged against the root the run is given.

    This pin replaced `test_site_root_path_is_left_alone` (session
    20261016-T135246Z-23188): such a link was skipped as a server's site root,
    and the Memar skill writes every link in that form, so none of its links
    was checked. It resolves as `memar content path` resolves it, against the
    checkout, never against the linking document's folder.
    """

    def test_a_root_relative_link_to_a_heading_there_is_not_reported(self) -> None:
        self.write("docs/cognition.md", "# Cognition\n## Abstract\n")
        path = self.write("area/deep/base.md", "# Base\n[A](/docs/cognition.md#abstract)\n")
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_root_relative_link_to_a_missing_anchor_is_reported(self) -> None:
        self.write("docs/cognition.md", "# Cognition\n## Abstract\n")
        path = self.write("area/base.md", "# Base\n[A](/docs/cognition.md#gone)\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("/docs/cognition.md#gone names no heading", found[0])
        self.assertIn("line 2", found[0])

    def test_a_root_relative_link_to_a_missing_file_is_reported(self) -> None:
        path = self.write("area/base.md", "# Base\n[A](/docs/gone.md)\n")
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn("/docs/gone.md does not exist", found[0])

    def test_it_is_not_resolved_from_the_linking_folder(self) -> None:
        # `area/docs/x.md` sits beside the linker; the link names the root's.
        self.write("area/docs/x.md", "# X\n")
        path = self.write("area/base.md", "# Base\n[A](/docs/x.md)\n")
        self.assertEqual(len(self.only_link_problems(path)), 1)


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
            "modules/content/documentation/changelog/changelog.md",
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


class WalkLooksOnlyAtWhatTheProjectOwns(LinkFixture):
    """A folder run skips what a copy of this project never carries.

    An installed dependency tree is not this repository's work, and a report that
    raises the same problems inside it on every run is a report about the tool
    rather than about the tree — after long enough it is a report nobody reads.
    The patterns come from `machine/fs_copy_excluded`, which already holds that
    answer for the two things that copy part of a checkout elsewhere; a second
    list here would be a second answer to one question.

    Naming a file explicitly still checks it. A walk is how the tool chooses for
    itself; a named path is a decision somebody already made.
    """

    def install(self, relative: str, text: str = "x") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def walked(self) -> list[str]:
        return [p.relative_to(self.root).as_posix()
                for p in content_check.checkable_files(self.root)]

    def test_a_dependency_tree_is_not_walked(self) -> None:
        self.install("node_modules/dep/package.json", '{"name": "dep"}\n')
        self.install("notes.md", "# Notes\n")
        walked = self.walked()
        self.assertIn("notes.md", walked)
        self.assertFalse([p for p in walked if p.startswith("node_modules/")], walked)

    def test_a_generated_folder_is_not_walked(self) -> None:
        for name in ("__pycache__", ".DS_Store"):
            with self.subTest(name=name):
                self.install(f"{name}/thing.py", "x = 1\n")
                walked = self.walked()
                self.assertFalse([p for p in walked if p.startswith(name)], walked)

    def test_a_file_inside_an_owned_folder_is_still_walked(self) -> None:
        self.install("src/deep/module.py", "x = 1\n")
        self.assertIn("src/deep/module.py", self.walked())

    def test_a_named_file_is_checked_whatever_folder_it_is_in(self) -> None:
        # The distinction the whole rule turns on: a walk chooses, a name does not.
        path = self.install("node_modules/dep/broken.md", "# T\n\n\nbody\n")
        self.assertTrue(self.problems(path))

    def test_the_patterns_are_the_ones_the_folder_already_states(self) -> None:
        # A copy of the list here would be a second answer to one question, so
        # every pattern the folder states is one the walk leaves out.
        from machine.fs_copy_excluded import NEVER_COPIED_PATTERNS

        for pattern in ("__pycache__", "*.pyc", ".DS_Store", "node_modules"):
            self.assertIn(pattern, NEVER_COPIED_PATTERNS)
        for pattern in NEVER_COPIED_PATTERNS:
            folder = pattern.replace("*", "x")
            with self.subTest(pattern=pattern):
                self.install(f"{folder}/thing.py", "x = 1\n")
                walked = self.walked()
                self.assertFalse([p for p in walked if p.startswith(f"{folder}/")], walked)


class RepositoryFixture(LinkFixture):
    """A scratch tree that is a Memar repository, for the rules that ask for one."""

    def make_repo(self) -> Path:
        repo = self.root / "Memar"
        repo.mkdir(parents=True, exist_ok=True)
        (repo / "README.md").write_text("# Memar\n", encoding="utf-8", newline="\n")
        (repo / "docs").mkdir(parents=True, exist_ok=True)
        skill = repo / ".agents" / "skills" / "memar" / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("# Memar\n", encoding="utf-8", newline="\n")
        return repo

    def isolate(self) -> None:
        # A walk past the scratch can reach the real repository (the session
        # folder the variable may point at sits inside this checkout), so
        # isolated to the scratch, outside resolves None wherever it sits.
        import machine.fs_memar_repository as memar_repository

        saved = memar_repository.is_memar_repository
        root = self.root.resolve()

        def isolated(path: Path) -> bool:
            try:
                Path(path).resolve().relative_to(root)
            except ValueError:
                return False
            return saved(path)

        memar_repository.is_memar_repository = isolated
        self.addCleanup(setattr, memar_repository, "is_memar_repository", saved)


class MemarRulesAutoDetect(RepositoryFixture):
    def test_memar_conventions_apply_inside_and_not_outside(self) -> None:
        self.isolate()
        repo = self.make_repo()
        inside = repo / "docs" / "note.md"
        inside.parent.mkdir(parents=True, exist_ok=True)
        inside.write_text("# Base\n\nBody\n", encoding="utf-8", newline="\n")
        outside = self.root / "plain" / "note.md"
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_text("# Base\n\nBody\n", encoding="utf-8", newline="\n")
        from machine.fs_memar_repository import enclosing_repository

        self.assertIsNotNone(enclosing_repository(inside))
        self.assertIsNone(enclosing_repository(outside))
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))
        self.assertEqual(content_check.check_file(outside, {}, False, root=self.root), [])

    def test_an_explicit_flag_wins_over_the_folder(self) -> None:
        repo = self.make_repo()
        inside = repo / "docs" / "note.md"
        inside.parent.mkdir(parents=True, exist_ok=True)
        inside.write_text("# Base\n\nBody\n", encoding="utf-8", newline="\n")
        self.assertEqual(content_check.check_file(inside, {}, False, root=self.root), [])
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))

    def test_encoding_problems_report_whatever_the_folder_is(self) -> None:
        repo = self.make_repo()
        inside = repo / "note.md"
        inside.write_text("# T\n", encoding="utf-8", newline="\n")
        inside.write_bytes(inside.read_bytes().rstrip(b"\n"))
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))
        self.assertTrue(content_check.check_file(inside, {}, False, root=self.root))


class CitationDirection(RepositoryFixture):
    """A relative link up the layers is a warning: a debt, never a problem.

    The rule is Documentation -> Citation Direction: the base (docs/, its
    khayyam/ and comparisons/ included) and the modules
    (modules/, bundles/). A document may link within its own
    layer or down to the base; a base document names a module as a concept.
    Files outside the two layers are not judged, and a folder's README may
    link anywhere inside its own folder. A link up is never deleted to comply,
    so the check warns about it and does not count it as a problem.
    """

    def setUp(self) -> None:
        super().setUp()
        self.repo = self.make_repo()

    def put(self, relative: str, text: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def upward(self, path: Path) -> list[str]:
        return [w for w in content_check.upward_warnings(path, self.cache)
                if "points up" in w]

    def test_an_upward_link_is_a_warning_and_not_a_problem(self) -> None:
        import argparse
        import contextlib
        import io

        self.targets()
        path = self.put("docs/process.md",
                        "# T\nSee [X](../modules/process/error/error.md).\n")
        self.assertEqual(content_check.check_file(path, self.cache, True, root=self.repo), [])
        args = argparse.Namespace(files=[str(path)], verbose=False, memar_rules=True)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.repo)
            except SystemExit as stop:
                code = stop.code or 0
        self.assertEqual(code, 0)
        self.assertIn("warnings (not counted as problems)", out.getvalue())
        self.assertIn("points up", out.getvalue())
        self.assertIn("a debt", out.getvalue())
        self.assertIn("0 problems", out.getvalue())

    def targets(self) -> None:
        self.put("docs/system.md", "# System\n")
        self.put("modules/process/error/error.md", "# Error\n")
        self.put("docs/khayyam/khayyam.md", "# Khayyam\n")
        self.put("bundles/khayyam/khayyam.md", "# Toolchain\n")
        self.put("modules/process/error/README.md", "# Error\n")

    def test_each_upward_pair_is_reported(self) -> None:
        self.targets()
        cases = [
            ("docs/process.md", "../modules/process/error/error.md"),
            ("docs/process.md", "../bundles/khayyam/khayyam.md"),
            ("docs/process.md", "../modules/process/error/"),
            ("docs/process.md", "../modules/"),
            ("docs/khayyam/flow.md", "../../modules/process/error/error.md"),
            ("docs/khayyam/flow.md", "../../bundles/khayyam/khayyam.md"),
            ("docs/khayyam/flow.md", "../../modules/process/error/README.md"),
            ("docs/comparisons/other.md", "../../modules/process/error/error.md"),
            ("docs/process.changelog.md", "../modules/process/error/error.md#error"),
        ]
        for source, link in cases:
            with self.subTest(source=source, link=link):
                path = self.put(source, f"# T\nSee [X]({link}).\n")
                found = self.upward(path)
                self.assertEqual(len(found), 1, found)
                self.assertIn("line 2", found[0])
                self.assertIn(link.partition("#")[0], found[0])

    def test_same_layer_and_downward_links_are_not_reported(self) -> None:
        self.targets()
        cases = [
            ("docs/process.md", "./system.md"),
            ("docs/process.md", "./khayyam/khayyam.md"),
            ("docs/process.md", "./khayyam/"),
            ("docs/khayyam/flow.md", "../system.md"),
            ("modules/process/flow/flow.md", "../error/error.md"),
            ("modules/process/flow/flow.md", "../../../docs/system.md"),
            ("modules/process/flow/flow.md", "../../../docs/khayyam/khayyam.md"),
            ("modules/process/flow/flow.md", "../error/README.md"),
            ("modules/process/flow/flow.md", "../../../bundles"),
            ("bundles/khayyam/rules.md", "../../docs/khayyam/khayyam.md"),
            ("modules/process/error/error.md", "../../../modules/process/error/error.md"),
            ("modules/process/error/error.md", "../../../bundles/khayyam/khayyam.md"),
        ]
        for source, link in cases:
            with self.subTest(source=source, link=link):
                path = self.put(source, f"# T\nSee [X]({link}).\n")
                self.assertEqual(self.upward(path), [])

    def test_a_path_in_a_code_span_is_not_reported(self) -> None:
        self.targets()
        path = self.put("docs/process.md",
                        "# T\nRealized in `bundles/khayyam/khayyam.md`; "
                        "shown as `[X](../bundles/khayyam/khayyam.md)`.\n")
        self.assertEqual(self.upward(path), [])

    def test_a_readme_may_point_into_its_own_folder_only(self) -> None:
        self.targets()
        inside = self.put("docs/README.md",
                          "# Docs\n[System](./system.md) "
                          "[Language](./khayyam/khayyam.md)\n")
        self.assertEqual(self.upward(inside), [])
        out = self.put("docs/khayyam/README.md",
                       "# Khayyam\n[Error](../../modules/process/error/error.md)\n")
        self.assertEqual(len(self.upward(out)), 1)

    def test_files_outside_the_layers_are_not_judged(self) -> None:
        self.targets()
        self.put("CONTRIBUTORS.md", "# Contributors\n")
        root_readme = self.put("README.md",
                               "# Memar\n[Code](./bundles/khayyam/khayyam.md)\n")
        self.assertEqual(self.upward(root_readme), [])
        skill = self.put(".agents/skills/memar/notes.md",
                         "# N\n[E](../../../modules/process/error/error.md)\n")
        self.assertEqual(self.upward(skill), [])
        base = self.put("docs/process.md", "# T\n[C](../CONTRIBUTORS.md)\n")
        self.assertEqual(self.upward(base), [])

    def test_outside_a_memar_repository_nothing_is_layered(self) -> None:
        self.isolate()
        self.write("plain/docs/modules/error.md", "# Error\n")
        path = self.write("plain/docs/process.md", "# T\n[E](./modules/error.md)\n")
        self.assertEqual(self.upward(path), [])


class OwedMarkIsAHint(LinkFixture):
    """`Owed: <id>` in a document and `owed:<id>` in a pending Test's title find each other.

    Per Content Rule -> Owed or planned capability and Test Practice -> Pending:
    an identifier on one side only is reported, as a hint apart from the
    problems and never changing the exit; the check reads the identifiers and
    opens no path.
    """

    def run_check(self, memar_rules: bool = True) -> tuple[str, int]:
        import argparse
        import contextlib
        import io

        args = argparse.Namespace(files=[str(self.root)], verbose=False,
                                  memar_rules=memar_rules)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return out.getvalue(), code

    def test_an_id_on_both_sides_is_not_reported(self) -> None:
        self.write("a.md", "# A\nOwed: khayyam.js-backend-runs\n")
        self.write("t/a.test.ts",
                   "test('owed:khayyam.js-backend-runs runs', { todo: true }, () => {});\n")
        out, code = self.run_check()
        self.assertNotIn("khayyam.js-backend-runs", out)
        self.assertNotIn("owed marks", out)
        self.assertEqual(code, 0)

    def test_a_document_only_id_is_a_hint_not_a_problem(self) -> None:
        self.write("a.md", "# A\nOwed: only.in-doc\n")
        out, code = self.run_check()
        self.assertIn("owed marks", out)
        self.assertIn("only.in-doc", out)
        self.assertIn("no pending Test", out)
        self.assertIn("0 problems", out)
        self.assertEqual(code, 0)

    def test_a_test_only_id_is_a_hint_not_a_problem(self) -> None:
        self.write("a.md", "# A\nNothing owed.\n")
        self.write("t/test_a.py",
                   "class T:\n    def test_x(self):\n        'owed:only.in-test is pending'\n")
        out, code = self.run_check()
        self.assertIn("only.in-test", out)
        self.assertIn("no Owed line", out)
        self.assertIn("0 problems", out)
        self.assertEqual(code, 0)

    def test_an_id_quoted_inside_prose_is_ignored(self) -> None:
        self.write("a.md", "# A\nWrite `Owed: quoted.id` in the document, or say Owed: prose.id inline.\n"
                           "```\nOwed: fenced.id\n```\n")
        out, _ = self.run_check()
        self.assertNotIn("quoted.id", out)
        self.assertNotIn("prose.id", out)
        self.assertNotIn("fenced.id", out)

    def test_a_path_is_not_an_id(self) -> None:
        self.write("a.md", "# A\nOwed: docs/x.md\nOwed: Has Space\n")
        out, _ = self.run_check()
        self.assertNotIn("owed marks", out)

    def test_no_memar_rules_skips_the_hint(self) -> None:
        self.write("a.md", "# A\nOwed: only.in-doc\n")
        out, code = self.run_check(memar_rules=False)
        self.assertNotIn("owed marks", out)
        self.assertEqual(code, 0)


class HandoffEntriesAreWarnedAbout(LinkFixture):
    """An Open Questions entry missing State, Options, Anchor or Blocks is a warning, apart from the problems."""

    ENTRY = "## Open Questions\n### Q?\n- **State**: x\n"
    FULL = "## Open Questions\n### Q?\n- State: x\n- Options: a\n- Anchor: y\n- Blocks: no\n"

    def run_check(self, memar_rules: bool = True) -> tuple[str, int]:
        import argparse
        import contextlib
        import io

        args = argparse.Namespace(files=[str(self.root)], verbose=False, memar_rules=memar_rules)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return out.getvalue(), code

    def test_a_short_entry_warns_and_is_not_a_problem(self) -> None:
        self.write("a.handoff.md", "# A handoff\n\n" + self.ENTRY)
        out, code = self.run_check()
        self.assertIn("warnings (not counted as problems):", out)
        self.assertIn("a.handoff.md:4: entry 'Q?' lacks Options, Anchor, Blocks", out)
        self.assertIn("0 problems", out)
        self.assertIn("1 warning", out)
        self.assertEqual(code, 0)

    def test_check_file_itself_does_not_return_it(self) -> None:
        path = self.write("a.handoff.md", "# A handoff\n\n" + self.ENTRY)
        self.assertEqual(content_check.check_file(path, {}, True, root=self.root), [])

    def test_a_complete_entry_and_other_documents_do_not_warn(self) -> None:
        self.write("a.handoff.md", "# A handoff\n\n" + self.FULL)
        self.write("b.md", "# B\n\n" + self.ENTRY)
        out, _ = self.run_check()
        self.assertNotIn("warning", out)

    def test_outside_a_memar_repository_it_is_not_judged(self) -> None:
        self.write("a.handoff.md", "# A handoff\n\n" + self.ENTRY)
        out, _ = self.run_check(memar_rules=False)
        self.assertNotIn("lacks", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
