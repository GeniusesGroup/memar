#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar prompts` in `services/prompts.py` and the services that declare its verbs.

    python .agents/scripts/services/tests/prompts.py

The subject is the prompts command — its help, its verbs, and which service
answers each — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
What each prompt's text is, is pinned by its own service's suite beside this
one; a behavior pinned in two files is one of them to forget.

The command is assembled by the launcher from the prompts services alone, so
another domain's services are not this suite's subject. Nothing here writes:
the services are replaced by mocks where a verb is dispatched, and the
subprocesses run ask for `--help` only.

What is pinned, and what each pin is for:

  HelpSaysWhatAPromptIs
                     `memar prompts --help` says what a prompt is: a fixed
                     text built from a session's id alone, handed to an
                     agent as it is printed, nothing added; and names none of
                     its sub-verbs' command lines. Each verb's help says what
                     it prints and for whom.
  EachServiceDeclaresItsVerb
                     Each verb is declared by the service that answers it,
                     under a long name that says what the prompt makes
                     happen, and the domain declares only the group.
  VerbsDispatch      Each verb reaches its one service with the arguments as
                     parsed.
  OldVerbsAreGone    `memar session` no longer offers `brief` or `answer`,
                     and no `--answer` flag is left anywhere: no legacy name.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import services.prompts as prompts
import services.prompts_answering as answering
import services.prompts_plan_brief as plan_brief
import services.prompts_questions_brief as questions_brief

LAUNCHER = SCRIPTS / "memar"

# The launcher is loaded under a name of its own, since its file has no
# extension for the import system to recognize.
_spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)

PROMPTS_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == "prompts"]
SESSION_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == "session"]
VERBS = ["answer-session-questions", "hand-session-plan-to-carry-out", "hand-session-questions-to-answer"]


def command(*arguments: str) -> int:
    """`memar prompts ARGUMENTS`, assembled from the prompts services alone."""
    with unittest.mock.patch.object(launcher, "services", return_value=PROMPTS_SERVICES):
        return launcher.main(["prompts", *arguments])


def run_help(*arguments: str, domain: str = "prompts") -> str:
    environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, str(LAUNCHER), domain, *arguments, "--help"], capture_output=True, env=environment
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.decode("utf-8").replace("\r\n", "\n")


def flat(text: str) -> str:
    return " ".join(text.split())


def verbs_of(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
    found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
    return dict(found[0].choices) if found else {}


class HelpSaysWhatAPromptIs(unittest.TestCase):
    def test_the_domain_help_says_what_a_prompt_is(self) -> None:
        text = flat(run_help())
        for phrase in (
            "memar prompts",
            "a fixed text",
            "from a session's id alone",
            "nothing added",
            *VERBS,
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_names_no_command_line_of_its_verbs(self) -> None:
        text = flat(run_help())
        for verb in VERBS:
            self.assertNotIn(f"memar prompts {verb}", text)

    def test_each_verbs_help_says_what_it_prints_and_for_whom(self) -> None:
        for verb, phrases in (
            ("hand-session-plan-to-carry-out", ("ID", "ready to paste", "`new --parent` prints", "to a sub-agent",
                                                "carry out", "`memar session start --session-id ID`")),
            ("hand-session-questions-to-answer", ("ID", "ready to paste", "to an agent that answers them", "Decisions needed",
                                                  "`memar prompts answer-session-questions --session-id ID`", "opens no session")),
            ("answer-session-questions", ("--session-id ID", "=== NAME ===", "For an agent", "writes nothing", "opens no session",
                                          "Decisions needed", "refuses an ID")),
        ):
            with self.subTest(verb=verb):
                text = flat(run_help(verb))
                self.assertIn(f"usage: memar prompts {verb}", text)
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_the_top_help_lists_prompts(self) -> None:
        environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run([sys.executable, str(LAUNCHER), "--help"], capture_output=True, env=environment)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertRegex(completed.stdout.decode("utf-8"), r"(?m)^ {4}prompts +\S")


class EachServiceDeclaresItsVerb(unittest.TestCase):
    class Recorded:
        """Where a service's verb goes, remembering the names it registers."""

        def __init__(self) -> None:
            self.names: list[str] = []
            self.group = argparse.ArgumentParser().add_subparsers()

        def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
            self.names.append(name)
            return self.group.add_parser(name, **kwargs)

    def test_each_verb_is_declared_by_the_service_that_answers_it(self) -> None:
        for module, declared in (
            (prompts, ["prompts"]),
            (plan_brief, ["hand-session-plan-to-carry-out"]),
            (questions_brief, ["hand-session-questions-to-answer"]),
            (answering, ["answer-session-questions"]),
        ):
            with self.subTest(verbs=declared):
                verbs = self.Recorded()
                run = module.describe(verbs)
                self.assertEqual(verbs.names, declared)
                # The domain only groups its verbs, so it owes nothing before them.
                if module is prompts:
                    self.assertIsNone(run)
                else:
                    self.assertTrue(callable(run))

    def test_the_command_offers_the_three_verbs(self) -> None:
        top, before = launcher.assemble(PROMPTS_SERVICES)
        self.assertEqual(before, [])
        self.assertEqual(sorted(verbs_of(verbs_of(top)["prompts"])), VERBS)


class VerbsDispatch(unittest.TestCase):
    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in (
            (["hand-session-plan-to-carry-out", "s-1"], plan_brief, "print_brief", ("s-1",)),
            (["hand-session-questions-to-answer", "s-1"], questions_brief, "print_questions_brief", ("s-1",)),
            (["answer-session-questions", "--session-id", "s-1"], answering, "print_answer",
             ("s-1", True, 1, None)),
            (["answer-session-questions", "--session-id", "s-1", "--without-skill", "--part", "2", "--most-characters", "9000"],
             answering, "print_answer", ("s-1", False, 2, 9000)),
        ):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service:
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_a_brief_with_the_old_answer_flag_is_refused(self) -> None:
        with unittest.mock.patch.object(plan_brief, "print_brief") as service, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command("hand-session-plan-to-carry-out", "s-1", "--answer")
        service.assert_not_called()


class OldVerbsAreGone(unittest.TestCase):
    def test_session_offers_neither_brief_nor_answer(self) -> None:
        top, _ = launcher.assemble(SESSION_SERVICES)
        offered = verbs_of(verbs_of(top)["session"])
        self.assertNotIn("brief", offered)
        self.assertNotIn("answer", offered)
        text = run_help(domain="session")
        for verb in ("brief", "answer"):
            self.assertNotRegex(text, rf"(?m)^ {{4}}{verb} ")

    def test_no_session_service_holds_the_old_names(self) -> None:
        for name in ("session_brief", "session_answer"):
            self.assertNotIn(name, launcher.services())


if __name__ == "__main__":
    unittest.main(verbosity=2)
