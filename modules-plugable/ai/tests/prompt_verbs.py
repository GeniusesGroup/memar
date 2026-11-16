#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the task verbs that print a prompt: which service declares each and what each reaches.

    python modules-plugable/ai/tests/prompt_verbs.py

What each prompt's text is, is pinned by its own service's suite beside this
one; a behavior pinned in two files is one of them to forget. Nothing here
writes: the services are replaced by mocks where a verb is dispatched, and the
subprocesses run ask for `--help` only.

What is pinned:

  Declares   Each verb is declared by the service that answers it, under a long
             name that says what the prompt makes happen.
  Dispatch   Each flat call reaches its one service with the arguments as parsed.
  Help       Each call's help says what it prints and for whom.
"""
from __future__ import annotations
from importlib import import_module
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
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
answering = import_module('modules-plugable.management.agency.widgets.answer_context.answer_context')
new_chats = import_module('modules-plugable.management.agency.widgets.new_chats_ask.new_chats_ask')
plan_brief = import_module('modules-plugable.management.agency.widgets.plan_carry_out_brief.plan_carry_out_brief')
questions_brief = import_module('modules-plugable.management.agency.widgets.questions_answer_brief.questions_answer_brief')
LAUNCHER = SCRIPTS.parent / 'memar_adaptor' / 'cli' / 'memar'
launcher = importlib.import_module('bundles.memar_adaptor.cli.router')
from bundles.memar_adaptor.cli.call_names import LegacyDetails
from modules.process.service.primitive.call_name import call_name
TASK_SERVICES = launcher.services_of('agency')
LEAF = {
    'get-task-answer-context': 'agency_get_task_answer_context',
    'get-new-chats-ask': 'agency_get_new_chats_ask',
    'get-task-plan-carry-out-brief': 'agency_get_task_plan_carry_out_brief',
    'get-task-questions-answer-brief': 'agency_get_task_questions_answer_brief',
}
VERBS = list(LEAF)

def command(*arguments: str) -> int:
    with unittest.mock.patch.object(launcher, 'services', return_value=TASK_SERVICES):
        return launcher.main(list(arguments))

def run_help(call: str) -> str:
    environment = dict(os.environ, COLUMNS='80', MEMAR_SERVER='0', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    completed = subprocess.run([sys.executable, str(LAUNCHER), call, '--help'], capture_output=True, env=environment)
    assert completed.returncode == 0, completed.stderr
    return ' '.join(completed.stdout.decode('utf-8').split())

class Declares(unittest.TestCase):

    class Recorded:

        def __init__(self) -> None:
            self.names: list[str] = []
            self.group = argparse.ArgumentParser().add_subparsers()

        def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
            self.names.append(name)
            return self.group.add_parser(name, **kwargs)

    def test_each_verb_is_declared_by_the_service_that_answers_it(self) -> None:
        for module, declared in ((plan_brief, ['get-task-plan-carry-out-brief']), (questions_brief, ['get-task-questions-answer-brief']), (answering, ['get-task-answer-context']), (new_chats, ['get-new-chats-ask'])):
            with self.subTest(verbs=declared):
                self.assertEqual(['-'.join(each.name.split()) for each in module.DECLARATIONS], declared)

    def test_the_verbs_are_flat_public_calls(self) -> None:
        top, _ = launcher.assemble(TASK_SERVICES)
        group = next((action for action in top._actions if isinstance(action, argparse._SubParsersAction)))
        self.assertTrue(set(LEAF.values()) <= set(group.choices))
        self.assertNotIn('ai', group.choices)
        self.assertNotIn('prompts', group.choices)

class Dispatch(unittest.TestCase):

    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in (
            (['agency_get_task_plan_carry_out_brief', 's-1'], plan_brief, 'get_task_plan_carry_out_brief', ('s-1',)),
            (['agency_get_task_questions_answer_brief', 's-1'], questions_brief, 'get_task_questions_answer_brief', ('s-1',)),
            (['agency_get_task_answer_context', '--task-id', 's-1'], answering, 'get_task_answer_context', ('s-1', True, 1, None)),
            (['agency_get_task_answer_context', '--task-id', 's-1', '--without-skill', '--part', '2', '--most-characters', '9000'], answering, 'get_task_answer_context', ('s-1', False, 2, 9000)),
        ):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service:
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_a_brief_with_the_old_answer_flag_is_refused(self) -> None:
        with unittest.mock.patch.object(plan_brief, 'get_task_plan_carry_out_brief') as service, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command('agency_get_task_plan_carry_out_brief', 's-1', '--answer')
        service.assert_not_called()

class Help(unittest.TestCase):

    def test_each_verbs_help_says_what_it_prints_and_for_whom(self) -> None:
        init = call_name(LegacyDetails('agency', 'get-task-init-context'))
        answer = call_name(LegacyDetails('agency', 'get-task-answer-context'))
        for verb, phrases in (
            ('agency_get_task_plan_carry_out_brief', ('ID', 'ready to paste', '`ensure --parent` prints', 'to a sub-agent', 'carry out', f'`memar {init} --task-id ID`')),
            ('agency_get_task_questions_answer_brief', ('ID', 'ready to paste', 'to an agent that answers them', 'Decisions needed', f'`memar {answer} --task-id ID`', 'opens no task')),
            ('agency_get_task_answer_context', ('--task-id ID', '=== NAME ===', 'For an agent', 'writes nothing', 'opens no task', 'Decisions needed', 'refuses an ID')),
        ):
            with self.subTest(verb=verb):
                text = run_help(verb)
                self.assertIn(f'usage: memar {verb}', text)
                for phrase in phrases:
                    self.assertIn(phrase, text)
if __name__ == '__main__':
    unittest.main(verbosity=2)
