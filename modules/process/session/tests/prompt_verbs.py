#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the session verbs that print a prompt: which service declares each and what each reaches.

    python modules/process/session/tests/prompt_verbs.py

What each prompt's text is, is pinned by its own service's suite beside this
one; a behavior pinned in two files is one of them to forget. Nothing here
writes: the services are replaced by mocks where a verb is dispatched, and the
subprocesses run ask for `--help` only.

What is pinned:

  Declares   Each verb is declared by the service that answers it, under a long
             name that says what the prompt makes happen, and is a verb of `session`.
  Dispatch   Each verb reaches its one service with the arguments as parsed.
  Help       Each verb's help says what it prints and for whom.
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
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

import modules.process.session.services.answering as answering
import modules.process.session.services.new_chats as new_chats
import modules.process.session.services.plan_brief as plan_brief
import modules.process.session.services.questions_brief as questions_brief

LAUNCHER = SCRIPTS / "memar"
_spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)

SESSION_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == "session"]
VERBS = ["answer-session-questions", "ask-for-new-chats", "hand-session-plan-to-carry-out", "hand-session-questions-to-answer"]


def command(*arguments: str) -> int:
    with unittest.mock.patch.object(launcher, "services", return_value=SESSION_SERVICES):
        return launcher.main(["session", *arguments])


def run_help(*arguments: str) -> str:
    environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run([sys.executable, str(LAUNCHER), "session", *arguments, "--help"], capture_output=True, env=environment)
    assert completed.returncode == 0, completed.stderr
    return " ".join(completed.stdout.decode("utf-8").split())


class Declares(unittest.TestCase):
    class Recorded:
        def __init__(self) -> None:
            self.names: list[str] = []
            self.group = argparse.ArgumentParser().add_subparsers()

        def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
            self.names.append(name)
            return self.group.add_parser(name, **kwargs)

    def test_each_verb_is_declared_by_the_service_that_answers_it(self) -> None:
        for module, declared in (
            (plan_brief, ["hand-session-plan-to-carry-out"]),
            (questions_brief, ["hand-session-questions-to-answer"]),
            (answering, ["answer-session-questions"]),
            (new_chats, ["ask-for-new-chats"]),
        ):
            with self.subTest(verbs=declared):
                verbs = self.Recorded()
                self.assertTrue(callable(module.describe(verbs)))
                self.assertEqual(verbs.names, declared)

    def test_the_verbs_are_verbs_of_session(self) -> None:
        top, _ = launcher.assemble(SESSION_SERVICES)
        group = next(action for action in top._actions if isinstance(action, argparse._SubParsersAction))
        inner = next(action for action in group.choices["session"]._actions if isinstance(action, argparse._SubParsersAction))
        self.assertTrue(set(VERBS) <= set(inner.choices))
        self.assertNotIn("prompts", group.choices)


class Dispatch(unittest.TestCase):
    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in (
            (["hand-session-plan-to-carry-out", "s-1"], plan_brief, "print_brief", ("s-1",)),
            (["hand-session-questions-to-answer", "s-1"], questions_brief, "print_questions_brief", ("s-1",)),
            (["answer-session-questions", "--session-id", "s-1"], answering, "print_answer", ("s-1", True, 1, None)),
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


class Help(unittest.TestCase):
    def test_each_verbs_help_says_what_it_prints_and_for_whom(self) -> None:
        for verb, phrases in (
            ("hand-session-plan-to-carry-out", ("ID", "ready to paste", "`new --parent` prints", "to a sub-agent", "carry out",
                                                "`memar session start --session-id ID`")),
            ("hand-session-questions-to-answer", ("ID", "ready to paste", "to an agent that answers them", "Decisions needed",
                                                  "`memar session answer-session-questions --session-id ID`", "opens no session")),
            ("answer-session-questions", ("--session-id ID", "=== NAME ===", "For an agent", "writes nothing", "opens no session",
                                          "Decisions needed", "refuses an ID")),
        ):
            with self.subTest(verb=verb):
                text = run_help(verb)
                self.assertIn(f"usage: memar session {verb}", text)
                for phrase in phrases:
                    self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
