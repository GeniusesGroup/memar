#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar task` in `modules/management/task/task.py` and the services that declare its verbs.

    python modules/management/task/tests/session.py

The subject is the session command — its help, its arguments, and which
service answers each verb — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
What each service does is pinned by its own suite beside this one; a behavior
pinned in two files is one of them to forget.

Nothing here writes outside its scratch folder. The Memar root the services
resolve is patched onto one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py`
names, and removed again. The command is assembled by the launcher from the
session services alone, so another domain's services are not this suite's
subject. The subprocesses run ask for `--help` only, which resolves no root and
writes nothing.

What is pinned, and what each pin is for:

  HelpSaysWhatToRun  Each help states its own work only (owner, 2026-10-14).
                     `memar task --help` states the domain's: what a task
                     and a session are, that the folder's top holds only
                     plan.md and report.md (and Memar's claim) and the rest
                     goes in the session's own folders by kind, temp/ for what
                     no record needs, the Status words and that
                     a session ends when its report and plan state the same
                     one, who writes into another session's folder, that each
                     location keeps its own log; nothing of a move its own
                     run would make before a verb; and none of a sub-verb's command
                     lines, files, or recipes. No sub-verb sends its reader
                     back there for its own work. `new` says what it writes
                     (the plan's outline, the report's skeleton, the short
                     hand-back), where the folder lies, how a task is handed
                     to a sub-agent, queued, or continued; `claims` carries
                     the whole recipe for an agent told only to "do some of
                     the queued tasks" — the project always named, one fresh
                     sub-agent per batch of one topic, each report read, one
                     `digest --conversation` at the end; `digest` the owner's
                     review and what a hand-back is; `close` when it may be
                     run; and each verb's own help what it accepts. No
                     external runner is named, and `memar --help`'s line for
                     `session` names queued tasks, so an agent starting from
                     the top reaches `claims`.
  EachServiceDeclaresItsVerb
                     Each verb is declared by the service that answers it, and
                     the services the others share declare none.
  VerbsDispatch      Each verb reaches its one service with the arguments as
                     parsed; the verb that added tasks to a plan is gone.
  NothingBeforeAnyVerb
                     `memar task` only groups its verbs: nothing runs
                     before a verb's own service, and a folder an earlier
                     Memar left directly in temp/ is not read: not listed, not moved.
  CommandEndToEnd    What a caller types — `new`, then `list` — opens a folder,
                     prints its id and path, and finds it again, through the
                     real services; and `memar task <verb> --help` answers
                     through the launcher for every verb.
  StaleCopiesAreNotNew
                     `new` does not ask whether the skill copies are stale:
                     that is `memar update`'s question.
  NoOneTimeMigration No file of the scripts folder names a one-time
                     migration script or what only such a script owns, and
                     none is one of them: such a script lives in the session
                     that does the change (the session's `services/` folder). Only
                     this suite's own list names them.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
from importlib import import_module
import argparse
import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.management.task.task as session
session_archive = import_module('modules-plugable.computer.git.services.archive_task_records')
import modules.management.task.services.claim as session_claim
from modules.management.task.primitive.claim import Claim
import modules.management.task.services.claims as session_claims
session_close = import_module('modules-plugable.computer.git.services.trash_task_folder')
import modules.management.task.services.get_decisions_digest as session_digest
import modules.management.task.services.list as session_find
import modules.management.task.services.folder as session_folder
session_gc = import_module('modules-plugable.computer.git.services.sweep_idle_task_folders')
import modules.management.task.primitive.task_id as task_id
import modules.process.project.services.task_location as session_location
session_log = import_module('modules-plugable.computer.git.services.log')
import modules.management.task.services.ensure as session_ensure
import modules.management.task.services.new as session_new
import modules.knowledge.documentation.plan.services.plan as session_plan
import modules.management.task.services.priority as session_priority
session_start = import_module('modules-plugable.ai.services.get_task_init_context')
import modules.knowledge.label.services.add as session_label
import modules.knowledge.label.services.list as session_labels
import modules.knowledge.documentation.report.services.report as session_report
session_show = import_module('modules-plugable.computer.git.services.show_task_records')
LAUNCHER = SCRIPTS / 'memar'
_spec = importlib.util.spec_from_loader('memar_launcher', SourceFileLoader('memar_launcher', str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)
SESSION_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == 'task']
TITLE = 'Test the session command'

def command(*arguments: str) -> int:
    """`memar task ARGUMENTS`, assembled from the session services alone."""
    with unittest.mock.patch.object(launcher, 'services', return_value=SESSION_SERVICES):
        return launcher.main(['task', *arguments])

def run_help(*arguments: str) -> str:
    environment = dict(os.environ, COLUMNS='80', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    completed = subprocess.run([sys.executable, str(LAUNCHER), 'task', *arguments, '--help'], capture_output=True, env=environment)
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.decode('utf-8').replace('\r\n', '\n')

def flat(text: str) -> str:
    return ' '.join(text.split())

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        project = unittest.mock.patch.object(session_ensure, 'project_root', return_value=self.fake_root)
        project.start()
        self.addCleanup(project.stop)

    def run_main(self, *arguments: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = command(*arguments)
        self.assertEqual(code, 0)
        return out.getvalue()

class HelpSaysWhatToRun(unittest.TestCase):
    MECHANISM = ('shared-tree collisions', 'advisory locks', 'intent notes', 'OS-temp', 'fails closed', 'scripts/services/')

    def test_the_domain_help_says_what_a_task_and_a_session_are(self) -> None:
        text = flat(run_help())
        for phrase in ('A task is one thing the person asked for', 'A session is the record of one task', 'One session is one task', 'gets a session of its own', "Work inside the session's folder, not in the checkout", 'read what `new` says first'):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_the_top_holds_only_the_plan_and_the_report_and_where_the_rest_goes(self) -> None:
        text = flat(run_help())
        for phrase in ("The folder's top holds only plan.md and report.md", 'the `claim` file Memar writes there', 'Put nothing else at the top', 'a note (.md) in docs/, a script (.py, .mjs, .js, .ps1, .sh) in services/', 'a test in tests/', 'besides its folders, docs/, services/, tests/, temp/,', 'a file of another kind, or what the record does not need, in temp/'):
            self.assertIn(phrase, text)

    def test_the_domain_help_gives_the_status_words_and_how_a_session_ends(self) -> None:
        text = run_help()
        for phrase in ('Queued     Waiting to be taken up', 'Active     Being worked on', 'Status: Complete   the check passed', 'Status: Blocked    it waits on an answer or an approval', 'Status: Active     its budget ended'):
            self.assertIn(phrase, text)
        text = flat(text)
        for phrase in ('Queued, Active, Blocked, or Complete', 'finished or not', 'its report.md states a Status and its plan.md states the same', 'Complete once its check has passed'):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_who_writes_into_another_sessions_folder_and_where_each_log_is(self) -> None:
        text = flat(run_help())
        for phrase in ('Write only inside your own folder', "Two writes reach another session's folder, both from the session it came from", "writes the report.md of a sub-agent that could only return text, and sets that plan.md's Status", 'keeps its own log of what was done to its folders, sessions.log at its top'):
            self.assertIn(phrase, text)

    def test_the_domain_help_points_to_archive_for_where_the_records_are(self) -> None:
        text = flat(run_help())
        for phrase in ("its records stay, kept by `archive` on its project's records branch and never pushed", '`close` and the sweep act only on a session already archived', 'neither acts on a session whose Status is Queued', '`archive --help` says what is kept and where'):
            self.assertIn(phrase, text)
        self.assertNotIn("Committing a task's changes commits the records", text)

    def test_the_domain_help_says_nothing_of_a_move_before_every_verb(self) -> None:
        text = flat(run_help())
        for phrase in ('Before any verb below runs', 'moved into .agents/tasks/', 'asking for help moves nothing'):
            self.assertNotIn(phrase, text)

    def test_the_domain_help_states_no_sub_verbs_work(self) -> None:
        text = flat(run_help())
        for phrase in ('memar task ensure', 'memar task claims', 'memar task get-decisions-digest', 'Title: TITLE', '## Request', '## What ran', 'do some of the queued tasks', "review today's sessions", 'Once a day', 'To only add work'):
            self.assertNotIn(phrase, text)

    def test_no_sub_verb_sends_its_reader_to_the_domain_help_for_its_own_work(self) -> None:
        for verb in ('ensure', 'list', 'claim', 'claims', 'priority', 'get-decisions-digest', 'depends-on'):
            with self.subTest(verb=verb):
                text = flat(run_help(verb)).lower()
                self.assertNotIn('when to use', text)
                self.assertNotIn('what to do with each is said', text)
                self.assertNotIn("what a report's decisions are is said", text)

    def test_new_says_what_it_writes_and_leaves_the_rest_to_the_file(self) -> None:
        text = flat(run_help('ensure'))
        for phrase in ('never overwriting one that is there', 'Request (what was asked', 'Why (the reason', 'Steps (each local or delegated, each naming the governing documents it reads', 'Next (what the next session does first)', 'decide where it runs by two questions', "The owner's words never pick", 'A new chat never reaches a stronger model', 'at most 10 lines under `## Decisions needed`', 'use it as printed', '`memar content write`'):
            self.assertIn(phrase, text)
        for phrase in ('Title: TITLE', 'written in PascalCase', 'Once a day', 'drive or filesystem root is refused'):
            self.assertNotIn(phrase, text)

    def test_new_says_how_a_task_is_handed_over_queued_and_continued(self) -> None:
        text = flat(run_help('ensure'))
        for phrase in ('open its session with --parent', 'write the whole task into its plan.md — Request, the check that says it is done, the shape of its report, and Why', 'hand the sub-agent only the brief `new` prints, which `memar ai get-task-plan-carry-out-brief ID` prints again', '--label KIND=WORD', 'To only add work', '--queued', "never do a queued session's work in your own context", 'To continue a task another session left', '`memar task list`', 'start from its Next'):
            self.assertIn(phrase, text)

    def test_new_does_not_repeat_what_the_domain_states(self) -> None:
        text = run_help('ensure')
        for phrase in ('Status: Blocked    it waits', 'Queued     Waiting to be taken up', 'Put nothing else at the top'):
            self.assertNotIn(phrase, text)

    def test_claims_carries_the_recipe_for_an_agent_told_only_to_do_queued_tasks(self) -> None:
        text = flat(run_help('claims'))
        for phrase in ('do some of the queued tasks', '--project NAME or --project-path PATH is required: one run serves one project', '"Do 5 tasks of X" means `claims 5 --project X`', 'there is no default project and no way to take from all', 'ask the owner rather than guess', '`memar task list --status queued`', 'N is yours to choose', 'the highest priority first, the oldest opened first among equals', 'Hand the batch of one topic to one fresh sub-agent', 'each session keeping its own plan.md and report.md', 'never one sub-agent for sessions of different topics', 'never in your own context', 'read its report.md: its Status and its Decisions needed', 'a Status that disagrees with its plan', 'failed hand-back', "run `memar task get-decisions-digest --conversation ID`, ID your own session's", 'give the owner that one digest', 'Memar starts no agent'):
            self.assertIn(phrase, text)

    def test_the_review_and_the_hand_back_are_digests(self) -> None:
        text = flat(run_help('get-decisions-digest'))
        for phrase in ("review today's sessions with me and close the ones I confirm", '`memar git trash-task-folder --task-id ID`', 'at most 10 lines', 'each the question, its options, and the one it recommends', 'a complete session is in only when it has entries or a failed hand-back', 'blocking first', 'A pointer to a handoff or line that holds no open question is a failed hand-back'):
            self.assertIn(phrase, text)

    @unittest.skip('close moved to memar git; see git/tests/trash_task_folder.py')
    @unittest.skip('verb moved off memar task')
    def test_close_says_when_it_may_be_run(self) -> None:
        text = flat(run_help('close'))
        for phrase in ('recycle bin', 'the person who started the session has already said the work is finished', 'never ask them to, and never close a session you did not open', 'You do not have to close a session'):
            self.assertIn(phrase, text)

    def test_no_external_runner_is_left_in_the_help(self) -> None:
        texts = [run_help(), *(run_help(verb) for verb in ('ensure', 'claim', 'claims', 'get-decisions-digest', 'priority'))]
        for text in texts:
            for word in ('launch', 'runner', '`run`', 'session run'):
                self.assertNotIn(word, text)

    def test_the_top_help_leads_to_queued_tasks(self) -> None:
        self.assertIn('queued tasks', session.SUMMARY)

    def test_each_verbs_help_says_what_it_accepts(self) -> None:
        for verb, phrases in (('ensure', ('--task-id', '--title TITLE', '--parent ID', '--project NAME', '--project-path PATH', 'for one task', 'Nothing else goes in the hand-over')), ('list', ('whose id, title, or project holds TEXT', 'one word or a short phrase, not a question', '--status {queued,active,blocked,complete}', '--conversation ID', '--idle-days DAYS', '--project NAME', '--project-path PATH', "List Memar's own session folders", 'the calling folder is never read', 'earlier shape')), ('ensure', ('--queued', 'an existing active one no one has claimed is queued', '--priority N', '1 to 10', 'higher goes sooner')), ('claim', ('ID', 'another agent holds, is refused', 'taken over', 'Nothing keeps a claim fresh', f'{Claim.stale_hours()} hours')), ('claims', ('N', 'highest priority first', 'oldest', 'brief', 'Fewer queued than N is not an error', 'no default', "never mixes two projects'", 'one fresh sub-agent per batch of one topic', '--label Topic=T', '--fill')), ('priority', ('ID', 'N', '1 to 10', '5 when', 'higher goes sooner', 'Anyone, a person or an agent, may change it')), ('get-decisions-digest', ('--conversation ID', 'Decisions needed', 'priority', 'failed hand-back', 'marked `failed hand-back` with why', 'Queued sessions are left out', 'With --day: the review', 'The review closes nothing itself')), ('depends-on', ('ID', '--add', '--drop'))):
            with self.subTest(verb=verb):
                text = flat(run_help(verb))
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_the_help_does_not_carry_the_implementation(self) -> None:
        text = run_help()
        for phrase in self.MECHANISM:
            self.assertNotIn(phrase, text)

    def test_the_why_is_in_the_files_the_implementer_reads(self) -> None:
        for name in ('session_new', 'session_find'):
            self.assertIn(name, session.__doc__)
        for module, phrases in ((session_new, ('shared-tree collisions', 'advisory locks', 'intent notes', 'One session is one task')), (session_plan, ('disputed', 'handoff', 'Only that shape is read')), (session_find, ('listed together',))):
            for phrase in phrases:
                self.assertIn(phrase, flat(module.__doc__), module.__name__)

class NoOneTimeMigration(unittest.TestCase):
    MIGRATION_SCRIPTS = ('session-convert', 'session-strays', 'session-rename', 'CONVERT_SCRIPT', 'session_migrate', 'sessions.migrated', 'take_up')

    def test_no_file_of_the_scripts_folder_names_a_one_time_migration(self) -> None:
        this = Path(__file__).resolve()
        files = [path for path in SCRIPTS.rglob('*.py') if path.resolve() != this]
        files.append(LAUNCHER)
        for path in files:
            text = path.read_text(encoding='utf-8')
            for name in self.MIGRATION_SCRIPTS:
                with self.subTest(path=path.relative_to(SCRIPTS).as_posix(), name=name):
                    self.assertNotIn(name, text)
            with self.subTest(path=path.relative_to(SCRIPTS).as_posix()):
                self.assertFalse(path.name in {f'{name}.py' for name in self.MIGRATION_SCRIPTS})

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
        for module, declared in ((session, ['task']), (session_new, ['ensure']), (session_find, ['list']), (session_claim, ['claim']), (session_claims, ['claims']), (session_priority, ['priority']), (session_digest, ['get-decisions-digest'])):
            with self.subTest(verbs=declared):
                verbs = self.Recorded()
                run = module.describe(verbs)
                self.assertEqual(verbs.names, declared)
                if module is session:
                    self.assertIsNone(run)
                else:
                    self.assertTrue(callable(run))

    def test_the_shared_services_declare_no_verb(self) -> None:
        for module in (session_plan, session_report, session_folder, session_location, session_log, task_id):
            with self.subTest(module=module.__name__):
                self.assertFalse(hasattr(module, launcher.DESCRIBE))

    def test_the_command_offers_its_verbs(self) -> None:

        def verbs_of(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
            found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            return dict(found[0].choices) if found else {}
        top, before = launcher.assemble(SESSION_SERVICES)
        self.assertEqual(before, [])
        self.assertEqual(sorted(verbs_of(verbs_of(top)['task'])), sorted(['claim', 'claims', 'depends-on', 'get-decisions-digest', 'list', 'ensure', 'priority']))

class VerbsDispatch(Fixture):

    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in ((['ensure', '--title', 'T'], session_new, 'open_task', (None, 'T', None)), (['ensure', '--task-id', 's-1', '--parent', 's-0'], session_new, 'open_task', ('s-1', None, 's-0')), (['list'], session_find, 'list_tasks', (None, None, None, None, None)), (['list', 'word', '--status', 'blocked', '--idle-days', '3', '--conversation', 's-0'], session_find, 'list_tasks', ('word', 'blocked', 3.0, 's-0', None)), (['list', '--project-path', '<F>'], session_find, 'list_tasks', (None, None, None, None, '<F>')), (['list', '--project', 'p'], session_find, 'list_tasks', (None, None, None, None, '<F>')), (['ensure', '--title', 'T', '--queued'], session_new, 'open_task', (None, 'T', None, True, None)), (['ensure', '--title', 'T', '--queued', '--priority', '8'], session_new, 'open_task', (None, 'T', None, True, 8)), (['list', '--status', 'queued'], session_find, 'list_tasks', (None, 'queued', None, None, None)), (['claim', 's-1'], session_claim, 'claim', ('s-1',)), (['claims', '5'], session_claims, 'claims', (5, None)), (['claims', '2', '--project-path', '<F>'], session_claims, 'claims', (2, '<F>')), (['priority', 's-1', '8'], session_priority, 'set_session_priority', ('s-1', '8')), (['ensure', '--title', 'T', '--label', 'Topic=docs', '--label', 'TaskKind=design'], session_new, 'open_task', (None, 'T', None, False, None, ['Topic=docs', 'TaskKind=design'])), (['claims', '5', '--project', 'p', '--label', 'Topic=docs'], session_claims, 'claims', (5, '<F>', 'docs', False)), (['claims', '5', '--project', 'p', '--fill'], session_claims, 'claims', (5, '<F>', None, True)), (['get-decisions-digest'], session_digest, 'get_decisions_digest', (None, None, None)), (['get-decisions-digest', '--conversation', 's-0'], session_digest, 'get_decisions_digest', ('s-0', None, None))):
            folder = self.fake_root / 'p'
            folder.mkdir(exist_ok=True)
            argv = [str(folder) if word == '<F>' else word for word in argv]
            expected = tuple((folder.resolve() if value == '<F>' else value for value in expected))
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service, unittest.mock.patch('modules.process.project.services.find.resolve_project', return_value=folder.resolve()):
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_new_passes_its_project_as_a_folder_and_without_one_passes_none(self) -> None:
        folder = self.fake_root / 'docs'
        folder.mkdir()
        with unittest.mock.patch.object(session_new, 'open_task') as service:
            self.assertEqual(command('ensure', '--title', 'T', '--project-path', str(folder)), 0)
        service.assert_called_once_with(None, 'T', None, project=folder.resolve())
        with unittest.mock.patch.object(session_new, 'open_task') as service, unittest.mock.patch('modules.process.project.services.find.resolve_project', return_value=folder.resolve()):
            self.assertEqual(command('ensure', '--title', 'T', '--project', 'docs'), 0)
        service.assert_called_once_with(None, 'T', None, project=folder.resolve())
        with unittest.mock.patch.object(session_new, 'open_task') as service, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command('ensure', '--title', 'T', '--project')
        service.assert_not_called()

    def test_every_verb_that_takes_a_project_takes_one_flag_per_kind_and_never_both(self) -> None:
        for argv, module, name in ((['ensure', '--title', 'T'], session_new, 'open_task'), (['list'], session_find, 'list_tasks'), (['claims', '5'], session_claims, 'claims'), (['get-decisions-digest'], session_digest, 'get_decisions_digest')):
            with self.subTest(verb=argv[0]):
                folder = str(self.fake_root)
                with unittest.mock.patch.object(module, name) as service, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv, '--project', 'p', '--project-path', folder)
                    with self.assertRaises(SystemExit):
                        command(*argv, '--project', folder)
                    with self.assertRaises(SystemExit):
                        command(*argv, '--project-path', 'p-is-a-name')
                service.assert_not_called()

    def test_project_always_takes_a_value_and_no_service_runs_without_one(self) -> None:
        for argv, module, name in ((['list', 'word', '--project'], session_find, 'list_tasks'), (['list', 'word', '--project-path'], session_find, 'list_tasks'), (['claims', '5', '--project'], session_claims, 'claims'), (['get-decisions-digest', '--day', 'today', '--project'], session_digest, 'get_decisions_digest')):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv)
                service.assert_not_called()

    def test_the_task_verb_is_gone_and_an_unknown_status_refused(self) -> None:
        for argv in (['task', '--task-id', 's-1', '--title', 'T'], ['list', '--status', 'released'], ['close']):
            with self.subTest(argv=argv):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv)

class NothingBeforeAnyVerb(Fixture):

    def left_in_temp(self, sid: str, idle_days: float) -> Path:
        left = memar_fs.scratch_root() / sid
        left.mkdir(parents=True)
        plan = left / session_plan.PLAN_NAME
        plan.write_text(session_plan.plan_skeleton('20261009T120000Z-1-0', 'Left behind', '2026-10-09T12:00:00Z', Path('/w')), encoding='utf-8', newline='\n')
        when = time.time() - idle_days * 24 * 60 * 60
        for path in (plan, left):
            os.utime(path, (when, when))
        return left

    def test_a_folder_left_in_temp_is_not_listed_nor_moved(self) -> None:
        for sid, idle in (('20261009T120000Z-42-0', 2), ('20261009T120000Z-43-0', 0)):
            left = self.left_in_temp(sid, idle_days=idle)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                listed = self.run_main('list')
            self.assertNotIn(sid, listed)
            self.assertEqual(err.getvalue(), '')
            self.assertTrue(left.is_dir())
            self.assertFalse(memar_fs.task_dir(sid).exists())

class CommandEndToEnd(Fixture):

    def test_new_prints_the_id_and_path_and_list_finds_it(self) -> None:
        text = self.run_main('ensure', '--task-id', '20261003T000000Z-1-0', '--title', TITLE, '--project-path', str(self.fake_root))
        path = memar_fs.task_dir('20261003T000000Z-1-0')
        self.assertIn('task_id: 20261003T000000Z-1-0', text)
        self.assertIn(f'path: {path}', text)
        self.assertTrue((path / session_plan.PLAN_NAME).is_file())
        listed = self.run_main('list', '--status', 'active')
        self.assertIn(f'20261003T000000Z-1-0  {TITLE}', listed)

    def test_the_launcher_reaches_each_verbs_help(self) -> None:
        self.assertIn('one folder for the task you are about to do', run_help())
        for verb, phrase in (('ensure', '--parent ID'), ('list', '--conversation ID'), ('claim', 'ID'), ('claims', 'N'), ('get-decisions-digest', '--conversation ID'), ('priority', 'ID'), ('depends-on', 'ID')):
            with self.subTest(verb=verb):
                self.assertIn(phrase, run_help(verb))

class StaleCopiesAreNotNew(Fixture):

    def test_new_runs_no_child_process_but_git(self) -> None:
        with unittest.mock.patch.object(subprocess, 'run', wraps=subprocess.run) as run:
            self.run_main('ensure', '--task-id', 's-quiet', '--title', TITLE, '--project-path', str(self.fake_root))
        for call in run.call_args_list:
            self.assertEqual(call.args[0][0], 'git')
if __name__ == '__main__':
    unittest.main(verbosity=2)
