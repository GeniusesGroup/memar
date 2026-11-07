#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
TIER = 'system'
BUDGET_SECONDS = 150
from machine.plugable_import import load as plugable_load
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
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
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task = import_module('modules-plugable.management.task.task')
set_status_service = import_module('modules-plugable.knowledge.label.status.services.set_status')
SET_STATUS_LINE = f'memar service {set_status_service.SERVICE_SET} --thing ID --word WORD'
task_archive = import_module('bundles.memar_git.services.archive_task_records')
task_claim = import_module('modules-plugable.management.task.services.claim')
_m_claim = import_module('modules-plugable.management.task.primitive.claim')
Claim = _m_claim.Claim
task_claims = import_module('modules-plugable.management.task.services.claims')
task_close = import_module('bundles.memar_git.services.trash_task_folder')
task_digest = plugable_load('ai.services.task_get_decisions_digest')
task_find = import_module('modules-plugable.management.task.services.list')
task_folder = import_module('modules-plugable.management.task.services.folder')
task_gc = import_module('bundles.memar_git.services.sweep_idle_task_folders')
task_id = import_module('modules-plugable.management.task.primitive.task_id')
task_location = import_module('modules-plugable.management.task.services.task_location')
task_log = import_module('bundles.memar_git.services.log')
task_ensure = import_module('modules-plugable.management.task.services.ensure')
task_new = import_module('modules-plugable.management.task.services.new')
task_plan = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
task_start = import_module('modules-plugable.ai.services.get_task_init_context')
task_report = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
task_show = import_module('bundles.memar_git.services.show_task_records')
LAUNCHER = SCRIPTS / 'memar'
_spec = importlib.util.spec_from_loader('memar_launcher', SourceFileLoader('memar_launcher', str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)
TASK_SERVICES = launcher.services_of('task')
TITLE = 'Test the task command'

def command(*arguments: str) -> int:
    with unittest.mock.patch.object(launcher, 'services', return_value=TASK_SERVICES):
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
        project = unittest.mock.patch.object(task_ensure, 'project_root', return_value=self.fake_root)
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

    def test_the_domain_help_says_what_a_task_is(self) -> None:
        text = flat(run_help())
        for phrase in ('A task is one thing the person asked for', "Its record lives on the project's records branch", 'One task is one id', 'gets a task of its own', 'Scratch while working goes in the task\'s temp/', 'read what `ensure` says first'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_the_domain_help_says_where_scratch_and_claims_go(self) -> None:
        text = flat(run_help())
        for phrase in ("Scratch while working goes in the task's temp/", "A claim while an agent holds the task is Memar's (`claim`)", 'Role folders the work may use: services/, tests/, temp/'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_the_domain_help_gives_the_status_words_and_how_a_task_ends(self) -> None:
        text = run_help()
        for phrase in ('Queued     Waiting to be taken up', 'Active     Being worked on', 'Complete   the check passed', 'Blocked    it waits on an answer or an approval', 'Active     its budget ended'):
            self.assertIn(phrase, text)
        text = flat(text)
        for phrase in ('Queued, Active, Blocked, or Complete', SET_STATUS_LINE, 'the report does not repeat the Status', 'Complete once its check has passed'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_the_domain_help_says_who_posts_a_sub_agents_report(self) -> None:
        text = flat(run_help())
        for phrase in ('posts the report of a sub-agent that could only return text, and sets that task\'s Status', 'Read plan and report with `memar git show-task-records`'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_the_domain_help_points_to_archive_for_where_the_records_are(self) -> None:
        text = flat(run_help())
        for phrase in ("its records stay on its project's records branch and are never pushed", '`close` and the sweep act only on a task already archived', 'neither acts on a task whose Status is Queued'):
            self.assertIn(phrase, text)
        self.assertNotIn("Committing a task's changes commits the records", text)

    def test_the_domain_help_says_nothing_of_a_move_before_every_verb(self) -> None:
        text = flat(run_help())
        for phrase in ('Before any verb below runs', 'moved into .agents/tasks/', 'asking for help moves nothing'):
            self.assertNotIn(phrase, text)

    def test_the_domain_help_states_no_sub_verbs_work(self) -> None:
        text = flat(run_help())
        for phrase in ('memar task ensure', 'memar task claims', 'memar task get-decisions-digest', 'Title: TITLE', '## Request', '## What ran', 'do some of the queued tasks', "review today's tasks", 'Once a day', 'To only add work'):
            self.assertNotIn(phrase, text)

    def test_no_sub_verb_sends_its_reader_to_the_domain_help_for_its_own_work(self) -> None:
        for verb in ('ensure', 'list', 'claim', 'claims', 'get-decisions-digest', 'depends-on'):
            with self.subTest(verb=verb):
                text = flat(run_help(verb)).lower()
                self.assertNotIn('when to use', text)
                self.assertNotIn('what to do with each is said', text)
                self.assertNotIn("what a report's decisions are is said", text)

    def test_new_says_what_it_writes_and_leaves_the_rest_to_the_file(self) -> None:
        text = flat(run_help('ensure'))
        for phrase in ('a text is added and never written over', 'memar conversation post --timeline ID --kind plan|report', 'Request (what was asked', 'Why (the reason', 'Steps (each local or delegated, each naming the governing documents it reads', 'Next (what the next task does first)', 'decide where it runs by two questions', "The owner's words never pick", 'model-follows-need.md', 'at most 10 lines under `## Decisions needed`', SET_STATUS_LINE, 'No filesystem path is printed'):
            self.assertIn(phrase, text)
        for phrase in ('Title: TITLE', 'written in PascalCase', 'Once a day', 'drive or filesystem root is refused', 'task.yaml'):
            self.assertNotIn(phrase, text)

    def test_new_says_how_a_task_is_handed_over_queued_and_continued(self) -> None:
        text = flat(run_help('ensure'))
        for phrase in ('open its task with --parent', 'post the whole task as its plan content — Request, the check that says it is done, the shape of its report, and Why', 'hand the sub-agent only the brief `ensure` prints, which `memar ai get-task-plan-carry-out-brief ID` prints again', '--label ACT', 'To only add work', '--queued', "never do a queued task's work in your own context", 'To continue a task another task left', '`memar task ids`', 'start from its Next'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_new_sends_later_work_on_a_result_back_to_its_task(self) -> None:
        text = flat(run_help('ensure'))
        for phrase in ("A task is one thing asked with one check", "a full context, a plan a sub-agent can read or the end of a session is not a new thing asked", 'a new plan content on the same task', 'a ruling of the owner since is a content of kind `decision`', 'later-work-returns-to-its-task.md', 'a new task is for work new in itself', 'A sub-agent or a new chat that continues a task is handed that task', 'and no task is opened for it', 'To hand a thing new in itself to a sub-agent', 'independent, opened with no --parent', 'never as your child session, so that none of its messages come back to you', 'opened-chat-is-left-alone.md', 'a later act is a content posted with that word as its --kind'):
            self.assertIn(phrase, text)

    def test_new_does_not_repeat_what_the_domain_states(self) -> None:
        text = run_help('ensure')
        for phrase in ('Status: Blocked    it waits', 'Queued     Waiting to be taken up', 'Put nothing else at the top'):
            self.assertNotIn(phrase, text)

    def test_claims_carries_the_recipe_for_an_agent_told_only_to_do_queued_tasks(self) -> None:
        text = flat(run_help('claims'))
        for phrase in ('do some of the queued tasks', '--project NAME or --project-path PATH is required: one run serves one project', '"Do 5 tasks of X" means `claims 5 --project X`', 'there is no default project and no way to take from all', 'ask the owner rather than guess', '`memar task list --status queued`', 'N is yours to choose', 'the highest priority first, the oldest opened first among equals', 'Hand the batch of one topic to one fresh sub-agent', 'each task keeping its own plan and report contents (by kind)', 'never one sub-agent for tasks of different topics', 'never in your own context', 'read its report with `memar git show-task-records`', 'memar conversation post --kind report', SET_STATUS_LINE, 'a Status that disagrees with its plan', 'failed hand-back', "run `memar task get-decisions-digest --conversation ID`, ID your own task's", 'give the owner that one digest', 'Memar starts no agent'):
            self.assertIn(phrase, text)
        for name in ('task.yaml',):
            self.assertNotIn(name, text)

    def test_the_review_and_the_hand_back_are_digests(self) -> None:
        text = flat(run_help('get-decisions-digest'))
        for phrase in ("review today's tasks with me and close the ones I confirm", '`memar git trash-task-folder --task-id ID`', 'at most 10 lines', 'each the question, its options, and the one it recommends', 'a complete task is in only when it has entries or a failed hand-back', 'blocking first', 'one naming a question that is not open is a failed hand-back'):
            self.assertIn(phrase, text)

    @unittest.skip('close moved to memar git; see git/tests/trash_task_folder.py')
    @unittest.skip('verb moved off memar task')
    def test_close_says_when_it_may_be_run(self) -> None:
        text = flat(run_help('close'))
        for phrase in ('recycle bin', 'the person who started the task has already said the work is finished', 'never ask them to, and never close a task you did not open', 'You do not have to close a task'):
            self.assertIn(phrase, text)

    def test_no_external_runner_is_left_in_the_help(self) -> None:
        texts = [run_help(), *(run_help(verb) for verb in ('ensure', 'claim', 'claims', 'get-decisions-digest'))]
        for text in texts:
            for word in ('launch', 'runner', '`run`', 'task run'):
                self.assertNotIn(word, text)

    def test_the_top_help_leads_to_queued_tasks(self) -> None:
        self.assertIn('queued tasks', task.SUMMARY)

    def test_each_verbs_help_says_what_it_accepts(self) -> None:
        for verb, phrases in (('ensure', ('--task-id', '--title TITLE', '--parent ID', '--project NAME', '--project-path PATH', 'No filesystem path is printed', 'Nothing else goes in the hand-over')), ('list', ('whose id, title, or project holds TEXT', 'one word or a short phrase, not a question', '--status {queued,active,blocked,complete}', '--conversation ID', '--idle-days DAYS', '--project NAME', '--project-path PATH', "List Memar's own task folders", 'the calling folder is never read', 'earlier shape')), ('ensure', ('--queued', 'an existing active one no one has claimed is queued', '--priority N', '1 to 10', 'higher goes sooner')), ('claim', ('ID', 'another agent holds, is refused', 'taken over', 'Nothing keeps a claim fresh', f'{Claim.stale_hours()} hours')), ('claims', ('N', 'highest priority first', 'oldest', 'brief', 'Fewer queued than N is not an error', 'no default', "never mixes two projects'", 'one fresh sub-agent per batch of one topic', '--label Topic=T', '--fill')), ('get-decisions-digest', ('--conversation ID', 'Decisions needed', 'priority', 'failed hand-back', 'marked `failed hand-back` with why', 'Queued tasks are left out', 'With --day: the review', 'The review closes nothing itself')), ('depends-on', ('ID', '--add', '--drop'))):
            with self.subTest(verb=verb):
                text = flat(run_help(verb))
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_the_help_does_not_carry_the_implementation(self) -> None:
        text = run_help()
        for phrase in self.MECHANISM:
            self.assertNotIn(phrase, text)

    def test_the_why_is_in_the_files_the_implementer_reads(self) -> None:
        for name in ('task_new', 'task_find'):
            self.assertIn(name, task.__doc__)
        for module, phrases in ((task_new, ('shared-tree collisions', 'advisory locks', 'intent notes', 'One task is one folder')), (task_plan, ('disputed', 'handoff', 'Only that shape is read')), (task_find, ('listed together',))):
            for phrase in phrases:
                self.assertIn(phrase, flat(module.__doc__), module.__name__)

class NoOneTimeMigration(unittest.TestCase):
    MIGRATION_SCRIPTS = ('task-convert', 'task-strays', 'task-rename', 'CONVERT_SCRIPT', 'task_migrate', 'tasks.migrated', 'take_up')

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

        def __init__(self) -> None:
            self.names: list[str] = []
            self.group = argparse.ArgumentParser().add_subparsers()

        def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
            self.names.append(name)
            return self.group.add_parser(name, **kwargs)

    def test_each_verb_is_declared_by_the_service_that_answers_it(self) -> None:
        for module, declared in ((task, ['task']), (task_new, ['ensure']), (task_find, ['list']), (task_claim, ['claim']), (task_claims, ['claims']), (task_digest, ['get-decisions-digest'])):
            with self.subTest(verbs=declared):
                verbs = self.Recorded()
                run = module.describe(verbs)
                self.assertEqual(verbs.names, declared)
                if module is task:
                    self.assertIsNone(run)
                else:
                    self.assertTrue(callable(run))

    def test_the_shared_services_declare_no_verb(self) -> None:
        for module in (task_plan, task_report, task_folder, task_location, task_log, task_id):
            with self.subTest(module=module.__name__):
                self.assertFalse(hasattr(module, launcher.DESCRIBE))

    def test_the_command_offers_its_verbs(self) -> None:

        def verbs_of(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
            found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            return dict(found[0].choices) if found else {}
        top, before = launcher.assemble(TASK_SERVICES)
        self.assertEqual(before, [])
        self.assertEqual(sorted(verbs_of(verbs_of(top)['task'])), sorted(['claim', 'claims', 'depends-on', 'get-decisions-digest', 'ids', 'list', 'ensure']))

class VerbsDispatch(Fixture):

    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in ((['ensure', '--title', 'T'], task_new, 'open_task', (None, 'T', None)), (['ensure', '--task-id', 's-1', '--parent', 's-0'], task_new, 'open_task', ('s-1', None, 's-0')), (['ensure', '--title', 'T', '--queued'], task_new, 'open_task', (None, 'T', None, True, None)), (['ensure', '--title', 'T', '--queued', '--priority', '8'], task_new, 'open_task', (None, 'T', None, True, 8)), (['claim', 's-1'], task_claim, 'claim', ('s-1',)), (['claims', '5'], task_claims, 'claims', (5, None)), (['claims', '2', '--project-path', '<F>'], task_claims, 'claims', (2, '<F>')), (['ensure', '--title', 'T', '--label', 'Topic=docs', '--label', 'TaskKind=design'], task_new, 'open_task', (None, 'T', None, False, None, ['Topic=docs', 'TaskKind=design'])), (['claims', '5', '--project', 'p', '--label', 'Topic=docs'], task_claims, 'claims', (5, '<F>', 'docs', False)), (['claims', '5', '--project', 'p', '--fill'], task_claims, 'claims', (5, '<F>', None, True)), (['get-decisions-digest'], task_digest, 'get_decisions_digest', (None, None, None)), (['get-decisions-digest', '--conversation', 's-0'], task_digest, 'get_decisions_digest', ('s-0', None, None))):
            folder = self.fake_root / 'p'
            folder.mkdir(exist_ok=True)
            argv = [str(folder) if word == '<F>' else word for word in argv]
            expected = tuple((folder.resolve() if value == '<F>' else value for value in expected))
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service, unittest.mock.patch('modules.computer.software.services.project_find.resolve_project', return_value=folder.resolve()):
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_new_passes_its_project_as_a_folder_and_without_one_passes_none(self) -> None:
        folder = self.fake_root / 'docs'
        folder.mkdir()
        with unittest.mock.patch.object(task_new, 'open_task') as service:
            self.assertEqual(command('ensure', '--title', 'T', '--project-path', str(folder)), 0)
        service.assert_called_once_with(None, 'T', None, project=folder.resolve())
        with unittest.mock.patch.object(task_new, 'open_task') as service, unittest.mock.patch('modules.computer.software.services.project_find.resolve_project', return_value=folder.resolve()):
            self.assertEqual(command('ensure', '--title', 'T', '--project', 'docs'), 0)
        service.assert_called_once_with(None, 'T', None, project=folder.resolve())
        with unittest.mock.patch.object(task_new, 'open_task') as service, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command('ensure', '--title', 'T', '--project')
        service.assert_not_called()

    def test_every_verb_that_takes_a_project_takes_one_flag_per_kind_and_never_both(self) -> None:
        for argv, module, name in ((['ensure', '--title', 'T'], task_new, 'open_task'), (['claims', '5'], task_claims, 'claims'), (['get-decisions-digest'], task_digest, 'get_decisions_digest')):
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
        for argv, module, name in ((['claims', '5', '--project'], task_claims, 'claims'), (['get-decisions-digest', '--day', 'today', '--project'], task_digest, 'get_decisions_digest')):
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
        import shape
        shape.from_plan_text(left, task_plan.plan_skeleton('20261009T120000Z-1-0', 'Left behind', '2026-10-09T12:00:00Z', Path('/w')))
        when = time.time() - idle_days * 24 * 60 * 60
        for path in (left / shape.FACTS_NAME, left):
            os.utime(path, (when, when))
        return left

    def test_a_folder_left_in_temp_is_not_listed_nor_moved(self) -> None:
        for sid, idle in (('20261009T120000Z-42-0', 2), ('20261009T120000Z-43-0', 0)):
            left = self.left_in_temp(sid, idle_days=idle)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), unittest.mock.patch.object(import_module('modules-plugable.management.task.services.ids_source'), 'records_rows', return_value=[]):
                listed = self.run_main('ids', '--label', 'active')
            self.assertNotIn(sid, listed)
            self.assertEqual(err.getvalue(), '')
            self.assertTrue(left.is_dir())
            self.assertFalse(memar_fs.task_dir(sid).exists())

class CommandEndToEnd(Fixture):

    def test_new_prints_the_id_and_path_and_ids_finds_it(self) -> None:
        text = self.run_main('ensure', '--task-id', '20261003T000000Z-1-0', '--title', TITLE, '--project-path', str(self.fake_root))
        path = memar_fs.task_dir('20261003T000000Z-1-0')
        self.assertIn('task_id: 20261003T000000Z-1-0', text)
        self.assertIn(f'path: {path}', text)
        self.assertTrue((path / 'task.yaml').is_file())
        with unittest.mock.patch.object(import_module('modules-plugable.management.task.services.ids_source'), 'records_rows', return_value=[]):
            listed = self.run_main('ids', '--label', 'active')
        self.assertEqual(listed.strip(), 'next:')

    def test_the_launcher_reaches_each_verbs_help(self) -> None:
        self.assertIn('one folder for the task you are about to do', run_help())
        for verb, phrase in (('ensure', '--parent ID'), ('list', '--conversation ID'), ('claim', 'ID'), ('claims', 'N'), ('get-decisions-digest', '--conversation ID'), ('depends-on', 'ID')):
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
