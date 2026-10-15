#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar session start`, in `services/session_start.py`.

    python .agents/scripts/services/tests/session_start.py

The subject is the one multi-part text a sub-agent reads first, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, holding a small
skill and small documents of its own, so no pin here depends on what the real
documents say. One class reads the real skill, to pin that the passages
`start` takes from it are found in the file as written.

What is pinned, and what each pin is for:

  PartsInOrder     The text is parts, each opened by a mark line, in one order:
                   the session, the model it needs, the plan, the folder, the
                   skill, the documents, the help, the ending.
  SessionPart      The session's id, path, plan and report are printed, and
                   starting is `new --session-id`: the role folders and the
                   report are there afterwards.
  ModelPart        A kind that is judgment names the strongest model and what
                   to do on a weaker one; a mechanical kind a cheaper one; a
                   plan with no kind, or one the plan's author mistyped, says
                   the Request decides, and names the kinds.
  PlanAndFolder    The plan is printed whole, and the folder's listing names
                   what is in it, folders marked.
  Documents        The skill's Cognition Abstract is always printed; the
                   other passages the skill requires of judgment only for
                   those kinds; each document the plan's Steps name is read
                   at the section it names, or at its Abstract when it names
                   none; one that is not there is said, not skipped.
  Help             The help of each command the plan names is printed, once,
                   with the help of `session` and `content write` which every
                   session needs; a command that does not exist is said.
  Ending           What a sub-agent does last is printed.
  Refusal          A session with no folder or no plan is refused, naming how
                   a session is opened.
  RealSkill        The passages `start` takes from the real skill are found.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
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

import machine.fs_memar as memar_fs
import services.session_temp as session_temp
import services.session_start as session_start
from services.session_plan import PLAN_NAME, plan_skeleton
from services.session_report import REPORT_NAME

SID = "20261011-T000000Z-7"
SKILL = """# Skill
- Thinking runs in every step. Read [Cognition](/docs/cognition.md)'s [Abstract](/docs/cognition.md#abstract) first. Before a step that reasons, read also [Standards](/docs/cognition.md#standards-here), and [Norms](/docs/cognition.md#norms-here).
- Ideation, design, and critique read theirs: [Modeling](/docs/modeling.md#abstract)'s Abstract; [Practice](/docs/practice.md#first-part) from First Part through Last Part; [Khayyam](/docs/khayyam.md#minimal-rule) alone.
- Anything else is not read.
"""
DOCS = {
    "cognition.md": "# Cognition\n\n## Abstract\nCOGNITION-ABSTRACT\n\n## Standards Here\nSTANDARDS-TEXT\n\n## Norms Here\nNORMS-TEXT\n",
    "modeling.md": "# Modeling\n\n## Abstract\nMODELING-ABSTRACT\n\n## Body\nMODELING-BODY\n",
    "practice.md": "# Practice\n\n## First Part\nFIRST-TEXT\n\n## Middle Part\nMIDDLE-TEXT\n\n## Last Part\nLAST-TEXT\n\n## After\nAFTER-TEXT\n",
    "khayyam.md": "# Khayyam\n\n## Minimal Rule\nMINIMAL-TEXT\n\n## Other\nOTHER-TEXT\n",
    "steps.md": "# Steps\n\n## Abstract\nSTEPS-ABSTRACT\n\n## Detail\nSTEPS-DETAIL\n",
}
MARK = "=== "


def plan_with(kind: str | None = None, request: str = "Do the thing.", steps: str = "") -> str:
    base = plan_skeleton("Delegated", "2026-10-11T00:00:00Z", Path("/project"), kind=kind)
    return base.replace("## Request\n", f"## Request\n{request}\n").replace("## Steps\n", f"## Steps\n{steps}\n")


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        skill = self.fake_root / ".agents" / "skills" / "memar" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(SKILL, encoding="utf-8", newline="\n")
        for name, text in DOCS.items():
            (self.fake_root / "docs").mkdir(exist_ok=True)
            (self.fake_root / "docs" / name).write_text(text, encoding="utf-8", newline="\n")

    def session(self, plan: str) -> str:
        folder = memar_fs.session_dir(SID, create=True)
        (folder / PLAN_NAME).write_text(plan, encoding="utf-8", newline="\n")
        return SID

    def text(self, plan: str | None = None) -> str:
        if plan is not None:
            self.session(plan)
        return session_start.start_text(SID)

    def parts(self, plan: str | None = None) -> dict[str, str]:
        found: dict[str, str] = {}
        title = None
        for line in self.text(plan).splitlines():
            if line.startswith(MARK) and line.endswith(" ==="):
                title = line[len(MARK) : -len(" ===")]
                found[title] = ""
            elif title is not None:
                found[title] += line + "\n"
        return found


class PartsInOrder(Fixture):
    def test_the_text_is_marked_parts_in_one_order(self) -> None:
        self.assertEqual(
            list(self.parts(plan_with())),
            ["session", "model", PLAN_NAME, "folder", "skill", "documents", "help", "ending"],
        )

    def test_nothing_comes_before_the_first_mark(self) -> None:
        self.assertTrue(self.text(plan_with()).startswith(MARK))


class SessionPart(Fixture):
    def test_the_id_and_the_paths_are_printed(self) -> None:
        part = self.parts(plan_with())["session"]
        folder = memar_fs.session_dir(SID)
        for line in (f"session_id: {SID}", f"path: {folder}", f"plan: {folder / PLAN_NAME}", f"report: {folder / REPORT_NAME}"):
            self.assertIn(line, part)

    def test_starting_leaves_the_report_and_the_role_folders_there(self) -> None:
        self.text(plan_with())
        folder = memar_fs.session_dir(SID)
        self.assertTrue((folder / REPORT_NAME).is_file())
        self.assertTrue((folder / "docs").is_dir())


class ModelPart(Fixture):
    def test_a_kind_that_is_judgment_names_the_strongest_model_and_the_block(self) -> None:
        for kind in ("ideation", "plan", "modeling", "design", "critique"):
            with self.subTest(kind=kind):
                part = self.parts(plan_with(kind))["model"]
                self.assertIn(f"kind: {kind}", part)
                self.assertIn("strongest model", part)
                self.assertIn("end Blocked", part)

    def test_a_mechanical_kind_names_a_cheaper_model(self) -> None:
        part = self.parts(plan_with("mechanical"))["model"]
        self.assertIn("kind: mechanical", part)
        self.assertIn("cheaper model", part)
        self.assertNotIn("strongest", part)

    def test_a_plan_with_no_kind_leaves_it_to_the_request(self) -> None:
        part = self.parts(plan_with())["model"]
        self.assertIn("the plan states no kind", part)
        self.assertIn("ideates, designs, or critiques", part)

    def test_a_mistyped_kind_is_not_taken_for_a_cheaper_one(self) -> None:
        part = self.parts(plan_with().replace("Opened:", "Kind: modelling\nOpened:"))["model"]
        self.assertIn("'modelling' is not a kind", part)
        self.assertIn("ideation, plan, modeling, design, critique, mechanical", part)
        self.assertNotIn("cheaper model", part)


class PlanAndFolder(Fixture):
    def test_the_plan_is_printed_whole(self) -> None:
        plan = plan_with(request="Unique request words.")
        self.assertIn(plan.strip(), self.parts(plan)[PLAN_NAME])

    def test_the_folder_listing_names_files_and_marks_folders(self) -> None:
        part = self.parts(plan_with())["folder"]
        lines = part.splitlines()
        self.assertIn(PLAN_NAME, lines)
        self.assertIn(REPORT_NAME, lines)
        self.assertIn("docs/", lines)


class Documents(Fixture):
    def test_the_cognition_abstract_is_always_printed_and_the_rest_only_for_judgment(self) -> None:
        mechanical = self.parts(plan_with("mechanical"))["documents"]
        self.assertIn("COGNITION-ABSTRACT", mechanical)
        for absent in ("STANDARDS-TEXT", "NORMS-TEXT", "MODELING-ABSTRACT", "FIRST-TEXT"):
            self.assertNotIn(absent, mechanical)
        judgment = self.parts(plan_with("design"))["documents"]
        for present in ("COGNITION-ABSTRACT", "STANDARDS-TEXT", "NORMS-TEXT", "MODELING-ABSTRACT", "MINIMAL-TEXT"):
            self.assertIn(present, judgment)
        self.assertNotIn("MODELING-BODY", judgment)
        self.assertNotIn("OTHER-TEXT", judgment)

    def test_a_range_runs_from_the_first_section_through_the_last(self) -> None:
        judgment = self.parts(plan_with("design"))["documents"]
        for present in ("FIRST-TEXT", "MIDDLE-TEXT", "LAST-TEXT"):
            self.assertIn(present, judgment)
        self.assertNotIn("AFTER-TEXT", judgment)

    def test_each_passage_is_headed_by_where_it_comes_from(self) -> None:
        judgment = self.parts(plan_with("design"))["documents"]
        self.assertIn("docs/cognition.md#abstract", judgment)
        self.assertIn("docs/practice.md#first-part", judgment)

    def test_a_document_the_steps_name_is_read_at_its_section_or_its_abstract(self) -> None:
        steps = "1. local: read /docs/steps.md#detail and `docs/modeling.md`, then act."
        part = self.parts(plan_with("mechanical", steps=steps))["documents"]
        self.assertIn("STEPS-DETAIL", part)
        self.assertNotIn("STEPS-ABSTRACT", part)
        self.assertIn("MODELING-ABSTRACT", part)
        self.assertNotIn("MODELING-BODY", part)

    def test_a_document_named_twice_is_printed_once(self) -> None:
        steps = "read /docs/steps.md#detail, again /docs/steps.md#detail"
        part = self.parts(plan_with("mechanical", steps=steps))["documents"]
        self.assertEqual(part.count("STEPS-DETAIL"), 1)

    def test_documents_named_outside_the_steps_are_not_read(self) -> None:
        plan = plan_with("mechanical", request="See /docs/steps.md#detail.")
        self.assertNotIn("STEPS-DETAIL", self.parts(plan)["documents"])

    def test_a_document_that_is_not_there_is_said_and_the_rest_still_printed(self) -> None:
        steps = "read /docs/missing.md#x and /docs/steps.md#detail"
        part = self.parts(plan_with("mechanical", steps=steps))["documents"]
        self.assertIn("docs/missing.md", part)
        self.assertIn("is not there", part)
        self.assertIn("STEPS-DETAIL", part)

    def test_a_section_that_is_not_there_is_said(self) -> None:
        steps = "read /docs/steps.md#nowhere"
        part = self.parts(plan_with("mechanical", steps=steps))["documents"]
        self.assertIn("no section answers to #nowhere", part)


class SkillPart(Fixture):
    def test_the_skill_is_printed_whole(self) -> None:
        self.assertIn(SKILL.strip(), self.parts(plan_with())["skill"])


class Help(Fixture):
    def test_the_help_every_session_needs_is_printed(self) -> None:
        part = self.parts(plan_with())["help"]
        self.assertIn("`memar session --help`", part)
        self.assertIn("usage: memar session", part)
        self.assertIn("`memar content write --help`", part)
        self.assertIn("usage: memar content write", part)

    def test_the_help_of_a_command_the_plan_names_is_printed_once(self) -> None:
        plan = plan_with(request="Run `memar content search PATTERN` then `memar content search X --flag`.")
        part = self.parts(plan)["help"]
        self.assertEqual(part.count("`memar content search --help`"), 1)
        self.assertIn("usage: memar content search", part)

    def test_a_flag_or_a_placeholder_ends_the_command_words(self) -> None:
        plan = plan_with(request="Run `memar content section FILE HEADING` and `memar session priority --help`.")
        part = self.parts(plan)["help"]
        self.assertIn("`memar content section --help`", part)
        self.assertIn("`memar session priority --help`", part)

    def test_a_command_that_does_not_exist_is_said(self) -> None:
        part = self.parts(plan_with(request="Run `memar nothing here`."))["help"]
        self.assertIn("`memar nothing here`", part)
        self.assertIn("no such command", part)

    def test_the_commands_of_a_plan_are_read_from_anywhere_in_it(self) -> None:
        part = self.parts(plan_with(steps="1. run `memar content path REF`"))["help"]
        self.assertIn("usage: memar content path", part)


class Ending(Fixture):
    def test_what_a_sub_agent_does_last_is_printed(self) -> None:
        part = self.parts(plan_with())["ending"]
        for phrase in (
            "plan.md and report.md",
            "without rewriting",
            "`memar session --help`",
            "return the report as your final text",
            "`memar content write --create FILE --content-file SCRATCHFILE`",
            session_temp.TEMP_SENTENCE,
        ):
            self.assertIn(phrase, part)


class Refusal(Fixture):
    def test_a_session_with_no_folder_is_refused_naming_how_one_is_opened(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            session_start.start_text(SID)
        self.assertIn(f"no task to start in {SID}", str(refused.exception.code))
        self.assertIn("`memar session new --title T --parent ID --project NAME`", str(refused.exception.code))

    def test_a_session_with_no_plan_is_refused(self) -> None:
        memar_fs.session_dir(SID, create=True)
        with self.assertRaises(SystemExit) as refused:
            session_start.start_text(SID)
        self.assertIn(f"no task to start in {SID}", str(refused.exception.code))

    def test_run_prints_the_text_and_a_refusal_prints_nothing(self) -> None:
        self.session(plan_with())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_start.print_start(SID)
        self.assertTrue(out.getvalue().startswith(MARK))
        with contextlib.redirect_stdout(io.StringIO()) as nothing, self.assertRaises(SystemExit):
            session_start.print_start("a/b")
        self.assertEqual(nothing.getvalue(), "")


class RealSkill(unittest.TestCase):
    """The passages `start` takes from the skill are found in the skill as written."""

    def reading(self) -> session_start.Reading:
        skill = SCRIPTS.parent.parent / ".agents" / "skills" / "memar" / "SKILL.md"
        return session_start.required_reading(skill.read_text(encoding="utf-8"))

    def test_the_cognition_abstract_is_the_one_always_read(self) -> None:
        always = self.reading().always
        self.assertEqual([(ref.path, ref.anchor) for ref in always], [("docs/cognition.md", "abstract")])

    def test_judgment_reads_the_cognition_sections_and_what_the_skill_names_for_ideation(self) -> None:
        judgment = {(ref.path, ref.anchor): ref for ref in self.reading().judgment}
        for key in (
            ("docs/cognition.md", "standards-of-cognitive-material"),
            ("docs/cognition.md", "what-implementation-asymmetry-obliges"),
            ("docs/modeling.md", "abstract"),
            ("docs/modeling.practice.md", "model-reading"),
            ("docs/protocol.md", "abstract"),
            ("docs/khayyam/khayyam.md", "abstract"),
            ("docs/khayyam/khayyam.md", "minimal-legislation-a-principle"),
        ):
            self.assertIn(key, judgment)
        self.assertEqual(judgment[("docs/modeling.practice.md", "model-reading")].through, "The Modeling Workflow")

    def test_every_passage_resolves_in_the_real_documents(self) -> None:
        from services.content_section import by_anchor

        root = SCRIPTS.parent.parent
        for ref in (*self.reading().always, *self.reading().judgment):
            with self.subTest(ref=ref):
                text = (root / ref.path).read_text(encoding="utf-8")
                self.assertIsNotNone(by_anchor(text, ref.anchor, ref.through))


if __name__ == "__main__":
    unittest.main(verbosity=2)
