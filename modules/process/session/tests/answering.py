#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar session answer-session-questions`, in `modules/process/session/services/answering.py`.

    python modules/process/session/tests/answering.py

The subject is the one multi-part text an agent handed a session's questions
reads first, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
How its parts are cut is `machine/console_parts.py`'s and pinned beside
`start`'s, in `modules/process/session/tests/start.py`; here only that it prints in
parts and names itself for the next one.

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, holding a small
skill and small documents of its own, and copies of Memar's every-act and
`answer` lists and of the real documents their entries name.

What is pinned, and what each pin is for:

  PartsInOrder     The text is parts, each opened by a mark line, in one order:
                   the session, the model it needs, the plan, the report, the
                   skill, the documents, the commands, the ending; with
                   `--without-skill` the skill is left out.
  ReadOnly         Printing it writes nothing anywhere: no report, no role
                   folder, no log line; it opens no session.
  ModelPart        Answering is judgment: the strongest model is named.
  PlanAndReport    The plan and the report, whose `Decisions needed` holds the
                   questions, are printed whole.
  Documents        The sections the every-act and `answer` lists name, then
                   each document a question names, at its section or its
                   Abstract; nothing is recorded, since answering writes nothing.
  Ending           The agent answers each question with its reasons, says which
                   it is unsure of, writes nothing, opens no session, and
                   returns the answers as its final text.
  InParts          A text past the bound prints in parts, each closing line
                   naming `memar session answer-session-questions` again with
                   the same flags and the next part.
  Refusal          A session with no folder, no plan, or no line under its
                   report's `Decisions needed` is refused, and nothing printed.
  AnswerHelp       The help says what it prints, for whom, and that it writes
                   nothing.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
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
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.console_parts import CLOSING_MARK
from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
from importlib import import_module
commands = import_module("modules-plugable.process.command.command")
import modules.process.session.services.answering as answering
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, plan_skeleton
from modules.knowledge.documentation.report.services.report import REPORT_NAME
from modules.knowledge.content.services.normative_references import EVERY_ACT, lists, memar_place
from modules.knowledge.content.services.task_context import context_text
from modules.knowledge.documentation.primitive.label import Label, Labels
from modules.knowledge.documentation.plan.primitive.task_kind import TaskKind

SID = "20261011-T000000Z-9"
ROOT = SCRIPTS.parent.parent
SKILL = "# Skill\n- SKILL-TEXT, printed whole.\n"
DOCS = {
    "plain.md": "# Plain\n\n## Abstract\nPLAIN-ABSTRACT\n\n## Body\nPLAIN-BODY\n",
    "steps.md": "# Steps\n\n## Abstract\nSTEPS-ABSTRACT\n\n## Detail\nSTEPS-DETAIL\n",
}
LISTS = [found for found in lists([memar_place(ROOT)]) if found.word in (EVERY_ACT, TaskKind.ANSWER.word)]
# The every-act and answer lists, and the real documents their entries name, copied into the scratch root.
REAL = sorted({entry.path for found in LISTS for entry in found.entries} | {found.path.relative_to(ROOT).as_posix() for found in LISTS})
MARK = "=== "
PLAN = plan_skeleton("20261011T000000Z-1-0", "Delegated", "2026-10-11T00:00:00Z", Path("/project"), labels=Labels((Label("TaskKind", "design"),))).replace(
    "## Request\n", "## Request\nPLAN-REQUEST\n"
)
REPORT = (
    "---\nTitle: R\nStatus: Blocked\n---\n# Report\n\n## Result\nREPORT-RESULT\n\n## Decisions needed\n"
    "- Q1: is /docs/steps.md#detail the home of the rule? Recommended: yes.\n"
    "- Q2: which name, per `docs/plain.md`? Recommended: answer.\n"
)
NO_QUESTIONS = "---\nTitle: R\nStatus: Complete\n---\n# Report\n\n## Decisions needed\n\n## Result\nDone.\n"


def headers(part: str) -> list[str]:
    """The passage headers of a documents part, as `path#anchor`, without a range's end."""
    return [line[4:].split(" through ")[0].removesuffix(" ---") for line in part.splitlines() if line.startswith("--- ")]


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
        (self.fake_root / "docs").mkdir(exist_ok=True)
        for name, text in DOCS.items():
            (self.fake_root / "docs" / name).write_text(text, encoding="utf-8", newline="\n")
        for path in REAL:
            (self.fake_root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, self.fake_root / path)

    def session(self, report: str | None = REPORT, plan: str = PLAN) -> Path:
        folder = memar_fs.session_dir(SID, create=True)
        (folder / PLAN_NAME).write_text(plan, encoding="utf-8", newline="\n")
        if report is not None:
            (folder / REPORT_NAME).write_text(report, encoding="utf-8", newline="\n")
        return folder

    def parts(self, with_skill: bool = True) -> dict[str, str]:
        found: dict[str, str] = {}
        title = None
        for line in answering.answer_text(SID, with_skill).splitlines():
            if line.startswith(MARK) and line.endswith(" ==="):
                title = line[len(MARK) : -len(" ===")]
                found[title] = ""
            elif title is not None:
                found[title] += line + "\n"
        return found


class PartsInOrder(Fixture):
    def test_the_text_is_marked_parts_in_one_order(self) -> None:
        self.session()
        self.assertEqual(
            list(self.parts()),
            ["session", "model", PLAN_NAME, REPORT_NAME, "skill", "documents", "commands", "ending"],
        )

    def test_without_the_skill_the_skill_is_left_out(self) -> None:
        self.session()
        parts = self.parts(with_skill=False)
        self.assertNotIn("skill", parts)
        self.assertNotIn("SKILL-TEXT", "".join(parts.values()))

    def test_nothing_comes_before_the_first_mark(self) -> None:
        self.session()
        self.assertTrue(answering.answer_text(SID).startswith(MARK))


class ReadOnly(Fixture):
    def test_printing_writes_nothing_and_opens_no_session(self) -> None:
        self.session()

        def everything() -> dict[str, bytes | None]:
            return {
                path.relative_to(self.fake_root).as_posix(): (path.read_bytes() if path.is_file() else None)
                for path in self.fake_root.rglob("*")
            }

        before = everything()
        with contextlib.redirect_stdout(io.StringIO()):
            answering.print_answer(SID)
        self.assertEqual(everything(), before)

    def test_the_session_part_says_it_is_read_and_not_taken_up(self) -> None:
        folder = self.session()
        part = self.parts()["session"]
        for line in (f"session_id: {SID}", f"plan: {folder / PLAN_NAME}", f"report: {folder / REPORT_NAME}"):
            self.assertIn(line, part)
        self.assertIn("not taken up", part)


class ModelPart(Fixture):
    def test_answering_is_judgment_and_names_the_strongest_model(self) -> None:
        self.session()
        part = self.parts()["model"]
        self.assertIn("kind: answer", part)
        self.assertIn("strongest model", part)


class PlanAndReport(Fixture):
    def test_the_plan_and_the_report_are_printed_whole(self) -> None:
        self.session()
        parts = self.parts()
        self.assertIn("PLAN-REQUEST", parts[PLAN_NAME])
        self.assertIn("REPORT-RESULT", parts[REPORT_NAME])
        self.assertIn("Q1:", parts[REPORT_NAME])
        self.assertIn("Q2:", parts[REPORT_NAME])


class Documents(Fixture):
    def test_the_answer_kind_passages_then_the_documents_the_questions_name(self) -> None:
        self.session()
        part = self.parts()["documents"]
        kind = [line for line in headers(context_text([memar_place(self.fake_root)], [TaskKind.ANSWER])) if "(description)" not in line]
        self.assertTrue(kind)
        found = [line for line in headers(part) if "(description)" not in line]
        self.assertEqual(found[: len(kind)], kind)
        self.assertIn("STEPS-DETAIL", part)
        self.assertNotIn("STEPS-ABSTRACT", part)
        self.assertIn("PLAIN-ABSTRACT", part)
        self.assertLess(part.index(kind[-1]), part.index("STEPS-DETAIL"))

    def test_a_document_the_plan_alone_names_is_not_printed(self) -> None:
        self.session(plan=PLAN.replace("PLAN-REQUEST", "PLAN-REQUEST, see /docs/plain.md#body"))
        self.assertNotIn("PLAIN-BODY", self.parts()["documents"])


class Commands(Fixture):
    def test_the_card_is_the_generated_one(self) -> None:
        self.session()
        self.assertEqual(self.parts()["commands"].strip(), commands.card_text().strip())


class Ending(Fixture):
    def test_what_the_answering_agent_does_is_printed(self) -> None:
        self.session()
        part = " ".join(self.parts()["ending"].split())
        for phrase in (
            "Decisions needed",
            "with its reasons",
            "unsure",
            "opens no session",
            "writes nothing",
            "final text",
            "`memar session start`",
        ):
            self.assertIn(phrase, part)


# A bound well under the text, so it prints in several parts.
SMALL = 6_000


class InParts(Fixture):
    def printed(self, part: int, with_skill: bool = True, most: int = SMALL) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            answering.print_answer(SID, with_skill, part=part, most=most)
        return out.getvalue()

    def test_a_closing_line_names_answer_with_the_same_flags_and_the_next_part(self) -> None:
        self.session()
        first = self.printed(1, with_skill=False)
        self.assertIn(CLOSING_MARK, first)
        self.assertLessEqual(len(first), SMALL)
        self.assertIn(
            f"`memar session answer-session-questions --session-id {SID} --without-skill --most-characters {SMALL} --part 2`", first
        )

    def test_the_passages_joined_are_the_text(self) -> None:
        self.session()
        self.assertEqual("".join(answering.answer_passages(SID)), answering.answer_text(SID))


class Refusal(Fixture):
    def test_a_session_with_no_folder_or_no_plan_is_refused(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            answering.answer_text(SID)
        self.assertIn(f"no questions to answer in {SID}", str(refused.exception.code))
        memar_fs.session_dir(SID, create=True)
        with self.assertRaises(SystemExit):
            answering.answer_text(SID)

    def test_a_session_with_no_question_under_decisions_needed_is_refused(self) -> None:
        for report in (None, NO_QUESTIONS):
            with self.subTest(report=report):
                self.session(report)
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as refused:
                    answering.print_answer(SID)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("Decisions needed", str(refused.exception.code))


class AnswerHelp(unittest.TestCase):
    def test_the_help_says_what_it_prints_and_that_it_writes_nothing(self) -> None:
        environment = dict(os.environ, COLUMNS="100", PYTHONIOENCODING="utf-8", MEMAR_NO_AUTO_UPDATE="1")
        done = subprocess.run(
            [sys.executable, str(SCRIPTS / "memar"), "session", "answer-session-questions", "--help"], capture_output=True, env=environment
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        shown = " ".join(done.stdout.decode("utf-8").split())
        for phrase in ("--without-skill", "--part", "--most-characters", "Decisions needed", "writes nothing", "hand-session-questions-to-answer ID", "For an agent"):
            self.assertIn(phrase, shown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
