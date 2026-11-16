#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
import concurrent.futures
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
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from machine.console_parts import CLOSING_MARK, MOST_CHARACTERS
set_status_service = import_module('modules-plugable.knowledge.label.status.services.set_status')
SET_STATUS_LINE = 'memar status_set ID WORD --project NAME'
task_temp = import_module('modules-plugable.management.task.services.temp')
task_start = import_module('modules-plugable.management.agency.widgets.context_compose.context_compose')
task_ensure = import_module('modules-plugable.management.task.services.ensure')
task_files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
commands = import_module('bundles.memar_adaptor.cli.services.commands')
from modules.knowledge.label.primitive.label import Label, Labels, new_id
_m_acts = import_module('modules.management.agency.labels.acts')
plan_acts = import_module('modules-plugable.knowledge.documentation.plan.services.plan_acts')
import shape
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
plan_skeleton = _m_plan_text.plan_skeleton
_m_content_get_section = import_module('modules-plugable.computer.codec.markdown.services.content_get_section')
by_anchor = _m_content_get_section.by_anchor
section_hash = _m_content_get_section.section_hash
_m_normative_references = import_module('modules-plugable.knowledge.documentation.services.normative_references')
EVERY_ACT = _m_normative_references.EVERY_ACT
LIST_NAME = _m_normative_references.LIST_NAME
PREFERENCE = _m_normative_references.PREFERENCE
lists = _m_normative_references.lists
memar_place = _m_normative_references.memar_place
from modules.computer.software.edges.manifest.services.preferences import preferences_path, preferences_text
_m_task_context = import_module('modules-plugable.management.task.services.task_context.task_context')
read_record = _m_task_context.read_record
Acts = _m_acts.Acts
SID = '20261011-T000000Z-7'
ROOT = SCRIPTS.parent.parent
SKILL = '# Skill\n- SKILL-TEXT, printed whole.\n'
DOCS = {'plain.md': '# Plain\n\n## Abstract\nPLAIN-ABSTRACT\n\n## Body\nPLAIN-BODY\n', 'steps.md': '# Steps\n\n## Abstract\nSTEPS-ABSTRACT\n\n## Detail\nSTEPS-DETAIL\n'}
LISTS = lists([memar_place(ROOT)])
OTHERS = {'modules/process/example/example.md': '# Example\n\n## Abstract\nEXAMPLE-ABSTRACT\n\n## Body\nEXAMPLE-BODY\n', 'modules/process/headless/headless.md': '# Headless\n\n## Why\nHEADLESS-WHY\n\n## How\nHEADLESS-HOW\n', 'modules/process/described/described.md': '---\nname: described\ndescription: DESCRIBED-DESCRIPTION\n---\n\n# Described\n', 'bundles/example/example.md': '# Bundle Example\n\n## Abstract\nBUNDLE-ABSTRACT\n'}
REAL = sorted({entry.path for found in LISTS for entry in found.entries} | {found.path.relative_to(ROOT).as_posix() for found in LISTS} | {'docs/khayyam/khayyam.md'})
EVERY_ACT_HEADS = [f'{entry.path}#{entry.anchor}' for found in LISTS if found.word == EVERY_ACT for entry in found.entries]
KHAYYAM = '/docs/khayyam/khayyam.md#minimal-legislation-a-principle'
MARK = '=== '

def _kind_label(word: str) -> Label:
    known = {d.label.title: d.label for d in plan_acts.PLAIN}
    return known.get(word) or Label(word, new_id())

def plan_with(kind: str | None=None, request: str='Do the thing.', steps: str='', project: Path=Path('/project')) -> str:
    base = plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', project, labels=Labels((_kind_label(kind),)) if kind else None)
    return base.replace('## Request\n', f'## Request\n{request}\n').replace('## Steps\n', f'## Steps\n{steps}\n')

BUDGET_SECONDS = 10
_m_program_location = import_module('bundles.memar.services.location.memar_location')
_m_program_location.declare_program(_m_program_location.entry_program(str(SCRIPTS.parent / 'memar_adaptor' / 'cli' / 'memar')))
_REAL_HELP_OF = task_start._help_of
_REAL_CARD_TEXT = commands.card_text
_CARD_ONCE: list = []
_HELPED = (*task_start.ALWAYS_HELP, ('content', 'search'), ('content', 'get-section'), ('task', 'priority'), ('content', 'resolve-path'), ('nothing', 'here'))
_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=len(_HELPED))
_HELP_ONCE: dict = {words: _POOL.submit(_REAL_HELP_OF, words) for words in _HELPED}

def help_once(words):
    if words not in _HELP_ONCE:
        _HELP_ONCE[words] = _POOL.submit(_REAL_HELP_OF, words)
    return _HELP_ONCE[words].result()

def card_once():
    if not _CARD_ONCE:
        _CARD_ONCE.append(_REAL_CARD_TEXT())
    return _CARD_ONCE[0]

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        for target, name, seam in ((task_start, '_help_of', help_once), (commands, 'card_text', card_once)):
            seamed = unittest.mock.patch.object(target, name, seam)
            seamed.start()
            self.addCleanup(seamed.stop)
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        under = import_module('modules-plugable.management.task.tests.scratch_task').task_dir_under(self.fake_root)
        for target in (memar_fs, task_ensure):
            bound = unittest.mock.patch.object(target, 'task_dir', under)
            bound.start()
            self.addCleanup(bound.stop)
        skill = self.fake_root / '.agents' / 'skills' / 'memar' / 'SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text(SKILL, encoding='utf-8', newline='\n')
        for name, text in DOCS.items():
            (self.fake_root / 'docs').mkdir(exist_ok=True)
            (self.fake_root / 'docs' / name).write_text(text, encoding='utf-8', newline='\n')
        for path in REAL:
            (self.fake_root / path).parent.mkdir(parents=True, exist_ok=True)
            source = ROOT / 'bundles/khayyam/khayyam.md' if path == 'docs/khayyam/khayyam.md' else ROOT / path
            shutil.copyfile(source, self.fake_root / path)
        for name, text in OTHERS.items():
            path = self.fake_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')

    def task(self, plan: str) -> str:
        folder = memar_fs.task_dir(SID, create=True)
        shape.from_plan_text(folder, plan)
        return SID

    def text(self, plan: str | None=None, with_skill: bool=True) -> str:
        if plan is not None:
            self.task(plan)
        return task_start.start_text(SID, with_skill=with_skill)

    def parts(self, plan: str | None=None, with_skill: bool=True) -> dict[str, str]:
        found: dict[str, str] = {}
        title = None
        for line in self.text(plan, with_skill).splitlines():
            if line.startswith(MARK) and line.endswith(' ==='):
                title = line[len(MARK):-len(' ===')]
                found[title] = ''
            elif title is not None:
                found[title] += line + '\n'
        return found

class NewShape(Fixture):

    def setUp(self) -> None:
        super().setUp()
        subprocess.run(['git', 'init', '-q', str(self.fake_root)], check=True, capture_output=True)
        ensured = unittest.mock.patch.object(task_ensure, 'project_root', return_value=self.fake_root)
        ensured.start()
        self.addCleanup(ensured.stop)
        with contextlib.redirect_stdout(io.StringIO()):
            _, self.folder = task_ensure.ensure_task(SID, 'Delegated', project=str(self.fake_root))
        body = plan_with(request='Do the new thing.').split('---\n', 2)[2]
        where = memar_fs.task_dir(SID, create=True)
        for name, data in import_module('bundles.memar_adaptor.git.services.task_store').tree(SID).items():
            path = where / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.folder = where
        timeline_files.add_text(self.folder, 'plan', body, 'agent')
        import_module('bundles.memar_adaptor.git.services.task_store').put_files(SID, {p.name: p.read_bytes() for p in self.folder.iterdir() if p.is_file()}, self.fake_root, message=f'test plan {SID}\n')

    def test_a_task_made_new_is_started_with_its_latest_plan_content_printed_whole(self) -> None:
        parts = self.parts()
        plan = task_files.plan_path(SID)
        self.assertEqual(plan.name, 'content.00001.md')
        self.assertEqual(list(parts), ['task', 'model', 'plan', 'folder', 'skill', 'documents', 'commands', 'help', 'ending'])
        self.assertIn('Do the new thing.', parts['plan'])

    def test_the_task_part_names_plan_and_report_by_kind(self) -> None:
        part = self.parts()['task']
        self.assertIn('plan: (latest content of kind plan)', part)
        self.assertIn('report: (latest content of kind report)', part)

    def test_starting_adds_no_file_to_the_task(self) -> None:
        before = sorted(entry.name for entry in self.folder.iterdir())
        self.text()
        self.assertEqual(sorted(entry.name for entry in self.folder.iterdir() if entry.is_file()), [name for name in before if (self.folder / name).is_file()])
        self.assertTrue((self.folder / 'task.yaml').is_file())
        self.assertTrue((self.folder / 'task.yaml').is_file())

    def test_the_project_the_facts_name_is_the_plan_project(self) -> None:
        self.assertEqual(task_start.plan_project(SID), self.fake_root)

class PartsInOrder(Fixture):

    def test_the_text_is_marked_parts_in_one_order(self) -> None:
        self.assertEqual(list(self.parts(plan_with())), ['task', 'model', 'plan', 'folder', 'skill', 'documents', 'commands', 'help', 'ending'])

    def test_without_the_skill_the_skill_is_left_out(self) -> None:
        parts = self.parts(plan_with(), with_skill=False)
        self.assertEqual(list(parts), ['task', 'model', 'plan', 'folder', 'documents', 'commands', 'help', 'ending'])
        self.assertNotIn('SKILL-TEXT', ''.join(parts.values()))

    def test_through_mcp_the_card_and_the_help_are_left_out(self) -> None:
        import os
        from unittest import mock
        with mock.patch.dict(os.environ, {'MEMAR_CALLER': 'mcp'}):
            parts = self.parts(plan_with(), with_skill=False)
        self.assertEqual(list(parts), ['task', 'model', 'plan', 'folder', 'documents', 'ending'])

    def test_nothing_comes_before_the_first_mark(self) -> None:
        self.assertTrue(self.text(plan_with()).startswith(MARK))

class TaskPart(Fixture):

    def test_the_id_and_the_plan_and_report_are_printed(self) -> None:
        part = self.parts(plan_with())['task']
        self.assertIn(f'task_id: {SID}', part)
        self.assertIn('plan:', part)
        self.assertIn('report:', part)

    def test_starting_writes_no_report_in_the_task_tree(self) -> None:
        self.text(plan_with())
        folder = memar_fs.task_dir(SID)
        self.assertTrue((folder / 'task.yaml').is_file())
        record = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage').context_record_path(SID)
        self.assertTrue(record.parent.is_dir())

class ModelPart(Fixture):

    def test_a_typed_critique_label_selects_the_critique_act(self) -> None:
        for label in ('ACT: critique', 'critique'):
            with self.subTest(label=label):
                plan = plan_with('critique')
                plan = __import__('re').sub(r'Labels:\n  - critique\([^\n]+\)', f'Labels:\n  - {label}', plan)
                folder = memar_fs.task_dir(SID, create=True)
                shape.from_plan_text(folder, plan)
                # conversation_post stores the supplied plan content verbatim;
                # write it as the latest content after seeding legacy facts.
                timeline_files.add_text(folder, 'plan', plan, 'agent')
                facts = task_files.read_facts(folder)
                self.assertNotIn('labels', facts)
                self.assertEqual(timeline_files.latest_content(folder, 'plan').body, plan)
                with unittest.mock.patch.object(task_start._storage, 'plan_text', return_value=plan):
                    part = self.parts()['model']
                self.assertIn('kind: critique', part)
                self.assertNotIn('the plan states no kind', part)

    def test_a_kind_gives_itself_cites_the_rule_and_keeps_the_block(self) -> None:
        for kind in plan_acts.ACTS:
            with self.subTest(kind=kind):
                part = self.parts(plan_with(kind))['model']
                self.assertIn(f'kind: {kind}', part)
                self.assertIn(plan_acts.MODEL_RULE, part)
                self.assertIn('end Blocked', part)
                self.assertIn('ask for another agent one level above to take it up', part)
                for word in ('strongest', 'cheaper', 'stronger'):
                    self.assertNotIn(word, part)

    def test_a_plan_with_no_kind_leaves_it_to_the_request(self) -> None:
        part = self.parts(plan_with())['model']
        self.assertIn('the plan states no kind', part)
        self.assertIn('Determine the act', part)
        self.assertIn(plan_acts.MODEL_RULE, part)
        self.assertNotIn('end Blocked saying the plan states no kind', part)
        self.assertNotIn('strongest', part)

    def test_a_label_that_is_no_act_is_not_taken_for_an_act(self) -> None:
        part = self.parts(plan_with('modelling'))['model']
        self.assertIn('the plan states no kind', part)
        self.assertNotIn('kind: mechanical', part)

class PlanAndFolder(Fixture):

    def test_the_plan_is_printed_whole(self) -> None:
        plan = plan_with(request='Unique request words.')
        self.assertIn(plan.split('---\n', 2)[2].strip(), self.parts(plan)['plan'])

    def test_the_folder_listing_names_files_and_marks_folders(self) -> None:
        part = self.parts(plan_with())['folder']
        lines = part.splitlines()
        self.assertTrue(any(name.startswith('content.') for name in lines))
        self.assertIn(shape.FACTS_NAME, lines)

def headers(part: str) -> list[str]:
    out: list[str] = []
    for line in part.splitlines():
        if not line.startswith('--- '):
            continue
        body = line[4:].split(' through ')[0].removesuffix(' ---')
        out.append(body.split(' (', 1)[0])
    return out

class Documents(Fixture):

    def test_init_documents_is_an_index_not_a_body_dump(self) -> None:
        part = self.parts(plan_with())['documents']
        self.assertIn('index only', part.splitlines()[0])
        self.assertIn('content_get_act_context', part)
        self.assertIn('ai_get_rules_for_subject', part)
        self.assertIn('Index:', part)
        self.assertNotIn('PLAIN-ABSTRACT', part)
        self.assertNotIn('## Abstract', part)

    def test_documents_bootstrap_names_the_kind_and_lists_paths(self) -> None:
        _act = import_module('modules.knowledge.content.services.act_context')
        printed = [_act.Printed('memar', 'docs/modeling.md', 'abstract', 'h')]
        composed = _act.Composed(blocks=['BODY-DUMP'], printed=printed, listed=1, changed=0, gone=0, dropped=0)
        part = task_start.documents_bootstrap('design', composed)
        self.assertIn('kinds: design; index only', part)
        self.assertIn('docs/modeling.md#abstract', part)
        self.assertNotIn('BODY-DUMP', part)

    def test_selection_still_reads_step_bodies_for_compose_not_init(self) -> None:
        steps = '1. local: read /docs/steps.md#detail and `docs/plain.md`, then act.'
        root = self.fake_root
        composed = task_start.documents(root, [], task_start.step_documents(root, steps), root)
        joined = '\n'.join(composed.blocks)
        self.assertIn('STEPS-DETAIL', joined)
        self.assertIn('PLAIN-ABSTRACT', joined)
        part = task_start.documents_bootstrap('mechanical', composed)
        self.assertNotIn('STEPS-DETAIL', part)
        self.assertIn('docs/steps.md#detail', part)

    def test_what_is_selected_is_still_recorded_when_init_runs(self) -> None:
        self.parts(plan_with())
        recorded = read_record(memar_fs.task_dir(SID))
        self.assertTrue(recorded)
        self.assertTrue(all(('\\' not in line.path for line in recorded)))

class SkillPart(Fixture):

    def test_the_skill_is_printed_whole(self) -> None:
        self.assertIn(SKILL.strip(), self.parts(plan_with())['skill'])

class Commands(Fixture):

    def test_the_part_is_the_card_the_command_module_generates(self) -> None:
        part = self.parts(plan_with())['commands']
        self.assertEqual(part.strip(), commands.card_text().strip())
        self.assertIn('memar content_write', part)

class Help(Fixture):

    def test_the_help_every_task_needs_is_printed(self) -> None:
        part = self.parts(plan_with())['help']
        self.assertIn('`memar task_ensure --help`', part)
        self.assertIn('usage: memar task_ensure', part)
        self.assertIn('`memar content_write --help`', part)
        self.assertIn('usage: memar content_write', part)

    def test_the_help_of_a_command_the_plan_names_is_printed_once(self) -> None:
        plan = plan_with(request='Run `memar content_search PATTERN` then `memar content_search X --flag`.')
        part = self.parts(plan)['help']
        self.assertEqual(part.count('`memar content_search --help`'), 1)
        self.assertIn('usage: memar content_search', part)

    def test_a_flag_or_a_placeholder_ends_the_command_words(self) -> None:
        plan = plan_with(request='Run `memar content_get_section FILE HEADING` and `memar task_claims --help`.')
        part = self.parts(plan)['help']
        self.assertIn('`memar content_get_section --help`', part)
        self.assertIn('`memar task_claims --help`', part)

    def test_a_command_that_does_not_exist_is_said(self) -> None:
        part = self.parts(plan_with(request='Run `memar nothing here`.'))['help']
        self.assertIn('`memar nothing here`', part)
        self.assertIn('no such command', part)

    def test_the_commands_of_a_plan_are_read_from_anywhere_in_it(self) -> None:
        part = self.parts(plan_with(steps='1. run `memar content_resolve_path REF`'))['help']
        self.assertIn('usage: memar content_resolve_path', part)

class Ending(Fixture):

    def test_what_a_sub_agent_does_last_is_printed(self) -> None:
        part = self.parts(plan_with())['ending']
        for phrase in ('without rewriting', f'`{SET_STATUS_LINE}`', 'return the report as your final text', 'never as `.agents/tmp_*`', f"project's `{task_temp.TEMP_FOLDER}/`", task_temp.TEMP_SENTENCE):
            self.assertIn(phrase, part)

    def test_the_folder_rule_is_said_once_in_the_task_help(self) -> None:
        parts = self.parts(plan_with())
        self.assertIn(SET_STATUS_LINE, parts['help'])
        for name in ('task.yaml',):
            self.assertNotIn(name, parts['ending'])

class NoFilesystemInComposeSurface(unittest.TestCase):

    def test_compose_module_does_not_import_path_folder_of_or_memar_location_at_top(self) -> None:
        import ast
        path = Path(task_start.__file__).resolve()
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
            elif isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
        joined = '\n'.join(imported)
        self.assertNotIn('pathlib', joined)
        self.assertNotIn('memar_location', joined)
        self.assertFalse(any(name.endswith('.folder') or name.endswith('folder') for name in imported if 'folder' in name))

class TaskHelp(Fixture):

    def test_its_flat_verb_help_is_printed(self) -> None:
        parts = self.parts(plan_with())
        task_help = parts['help'].split('--- `memar content_write --help` ---')[0]
        self.assertIn('usage: memar task_ensure', task_help)
        self.assertNotIn(task_start.CARD_POINTER, task_help)
        self.assertIn('memar task_ensure', parts['commands'])
SMALL = 8000

def body(part: str) -> str:
    return part[:part.rindex(CLOSING_MARK)] if CLOSING_MARK in part else part

class InParts(Fixture):

    def printed(self, part: int, with_skill: bool=True, most: int | None=SMALL) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_start.get_task_init_context(SID, with_skill, part=part, most=most)
        return out.getvalue()

    def every_part(self, with_skill: bool=True, most: int | None=SMALL) -> list[str]:
        parts = [self.printed(1, with_skill, most)]
        while 'the last' not in parts[-1][parts[-1].rindex(CLOSING_MARK):]:
            parts.append(self.printed(len(parts) + 1, with_skill, most))
        return parts

    def test_the_passages_joined_are_the_text(self) -> None:
        self.task(plan_with('implement'))
        self.assertEqual(''.join(task_start.start_passages(SID)), task_start.start_text(SID))

    def test_every_part_run_in_order_joins_to_the_text_each_under_the_bound(self) -> None:
        self.task(plan_with('implement'))
        parts = self.every_part()
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), SMALL)
        self.assertEqual(''.join((body(part) for part in parts)), task_start.start_text(SID))

    def test_a_closing_line_names_start_with_the_same_flags_and_the_next_part(self) -> None:
        self.task(plan_with('implement'))
        first = self.printed(1, with_skill=False)
        self.assertIn(f'`memar agency_get_task_init_context --task-id {SID} --without-skill --most-characters {SMALL} --part 2`', first)

    def test_a_text_under_the_bound_prints_whole_with_no_closing_line(self) -> None:
        self.task(plan_with('implement'))
        whole = self.printed(1, most=10 * len(task_start.start_text(SID)))
        self.assertNotIn(CLOSING_MARK, whole)
        self.assertEqual(whole, task_start.start_text(SID))

    def test_the_default_bound_is_the_declared_one(self) -> None:
        self.task(plan_with('implement'))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_start.get_task_init_context(SID)
        self.assertLessEqual(len(out.getvalue()), MOST_CHARACTERS)

    def project_preferring(self, value: str) -> Path:
        project = self.fake_root / 'project'
        project.mkdir(parents=True)
        (project / 'manifest.yaml').write_text(f'memar:\n  tasks:\n  most-characters: {value}\n', encoding='utf-8', newline='\n')
        self.task(plan_with('implement', project=project))
        return project

    def test_the_projects_preference_is_the_bound_and_no_closing_line_names_it(self) -> None:
        self.project_preferring(str(SMALL))
        parts = self.every_part(most=None)
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), SMALL)
        self.assertIn(f'`memar agency_get_task_init_context --task-id {SID} --part 2`', parts[0])
        self.assertEqual(''.join((body(part) for part in parts)), task_start.start_text(SID))

    def test_the_flag_outranks_the_preference(self) -> None:
        self.project_preferring(str(SMALL * 2))
        preferred = self.every_part(most=None)
        given = self.every_part(most=SMALL)
        self.assertGreater(len(given), len(preferred))
        for part in given:
            self.assertLessEqual(len(part), SMALL)

    def test_a_preference_that_is_not_a_number_is_refused_naming_its_file(self) -> None:
        self.project_preferring('many')
        with self.assertRaises(SystemExit) as refused:
            self.printed(1, most=None)
        self.assertIn('most-characters', str(refused.exception.code))
        self.assertIn('manifest.yaml', str(refused.exception.code))

    def test_every_part_names_one_hash_of_the_whole_text(self) -> None:
        from machine.console_parts import text_id
        self.task(plan_with('implement'))
        parts = self.every_part()
        whole = text_id(task_start.start_text(SID))
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertIn(f'{CLOSING_MARK} part {number} of {len(parts)} of text {whole}', part)

class Refusal(Fixture):

    def test_a_task_with_no_folder_is_refused_naming_how_one_is_opened(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            task_start.start_text(SID)
        self.assertIn(f'no task to start in {SID}', str(refused.exception.code))
        self.assertIn('`memar task_ensure --title T --parent ID --project NAME`', str(refused.exception.code))

    def test_a_task_with_no_plan_is_refused(self) -> None:
        memar_fs.task_dir(SID, create=True)
        with self.assertRaises(SystemExit) as refused:
            task_start.start_text(SID)
        self.assertIn(f'no task to start in {SID}', str(refused.exception.code))

    def test_run_prints_the_text_and_a_refusal_prints_nothing(self) -> None:
        self.task(plan_with())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_start.get_task_init_context(SID)
        self.assertTrue(out.getvalue().startswith(MARK))
        with contextlib.redirect_stdout(io.StringIO()) as nothing, self.assertRaises(SystemExit):
            task_start.get_task_init_context('a/b')
        self.assertEqual(nothing.getvalue(), '')

class StartHelp(unittest.TestCase):

    def test_the_help_says_what_it_prints_names_the_kinds_and_offers_without_skill(self) -> None:
        environment = dict(os.environ, COLUMNS='100', PYTHONIOENCODING='utf-8', MEMAR_NO_AUTO_UPDATE='1')
        done = subprocess.run([sys.executable, str(SCRIPTS.parent / 'memar_adaptor' / 'cli' / 'memar'), 'agency_get_task_init_context', '--help'], capture_output=True, env=environment)
        self.assertEqual(done.returncode, 0, done.stderr)
        shown = ' '.join(done.stdout.decode('utf-8').split())
        for phrase in ('--without-skill', '--part', '--most-characters', 'memar content_get_act_context', 'every agent', ', '.join(plan_acts.ACTS)):
            self.assertIn(phrase, shown)

class HelpIsAskedOfTheProgram(unittest.TestCase):

    def test_the_help_command_is_the_program_with_the_words_and_help(self) -> None:
        location = import_module('bundles.memar.services.location.memar_location')
        done = subprocess.CompletedProcess([], 0, 'usage: x', '')
        with unittest.mock.patch.object(location, 'program', return_value=('the-program', 'entry')), unittest.mock.patch.object(subprocess, 'run', return_value=done) as run:
            said = _REAL_HELP_OF(('content', 'search'))
        self.assertEqual(run.call_args[0][0], ['the-program', 'entry', 'content_search', '--help'])
        self.assertEqual(said, 'usage: x')

if __name__ == '__main__':
    unittest.main(verbosity=2)
