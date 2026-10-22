#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar ai get-task-init-context`, in `modules-plugable/ai/services/get_task_init_context.py`.

    python modules/management/task/tests/start.py

The subject is the one multi-part text a sub-agent reads first, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, holding a small
skill and small documents of its own, and copies of the real documents the
kinds' normative references name and of the lists themselves, so which
sections a kind prints is pinned against the lists as they are while what they
say is not pinned at all.

What is pinned, and what each pin is for:

  PartsInOrder     The text is parts, each opened by a mark line, in one order:
                   the session, the model it needs, the plan, the folder, the
                   skill, the documents, the commands, the help, the ending; with
                   `--without-skill` the skill is left out.
  SessionPart      The session's id, path, plan and report are printed, and
                   starting is `new --task-id`: the role folders and the
                   report are there afterwards.
  ModelPart        A kind that is judgment names the strongest model and what
                   to do on a weaker one; a mechanical kind a cheaper one; a
                   plan with no kind, or one the plan's author mistyped, says
                   the Request decides, and names the kinds.
  PlanAndFolder    The plan is printed whole, and the folder's listing names
                   what is in it, folders marked.
  Documents        The sections the plan's Kind's normative references name
                   are printed, as `modules/knowledge/content/services/task_context.py` composes them
                   from Memar's lists, under their first line, and recorded in
                   the session's `temp/context_read.txt`: the every-act sections
                   alone for a plan with no kind; the lists of the project the
                   plan names are read in the folders its preference names, and
                   one that does not exist is said on the first line; a design prints no Khayyam passage
                   unless its Steps name one. Then each document the plan's
                   Steps name, at the section it names or at its Abstract,
                   unless the kind's passages already hold it; one that is
                   not there is said, not skipped.
  Commands         The part names `memar commands` in one sentence and copies
                   nothing: the card is that command's own output, and a
                   service printing it would hold a second copy that drifts.
  Help             The help of each command the plan names is printed, once,
                   with the help of `session` and `content write` which every
                   session needs; a command that does not exist is said.
  Ending           What a sub-agent does last is printed.
  InParts          A text past the bound prints in ordered parts, as
                   `machine/console_parts.py` cuts them: each part under the
                   bound, every part run in order joins to the whole text, and
                   each closing line names `start` again with the same flags
                   and the next part. A passage is a mark's part, or one block
                   under it. Every part names one hash of the whole text. With
                   no flag the bound is the `most-characters` preference of
                   the project the plan names, which no closing line repeats;
                   the flag outranks it; a value that is not a number is
                   refused, naming the file.
  Refusal          A session with no folder or no plan is refused, naming how
                   a session is opened.
  StartHelp        The help says what it prints, names the kinds from the
                   registry, and offers `--without-skill`, `--part` and
                   `--most-characters`.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
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
SCRIPTS = TESTS.parents[2] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from machine.console_parts import CLOSING_MARK, MOST_CHARACTERS
import modules.management.task.services.temp as session_temp
session_start = import_module('modules-plugable.ai.services.get_task_init_context')
import modules.knowledge.label.services.plan_labels as session_plan_labels
commands = import_module('modules-plugable.computer.ui.cli.command.command')
from modules.knowledge.documentation.primitive.label import Label, Labels, new_id
from modules.knowledge.documentation.plan.labels import task_kind
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, plan_skeleton
from modules.knowledge.documentation.report.services.report import REPORT_NAME
from modules.knowledge.content.services.get_section import by_anchor, section_hash
from modules.knowledge.content.services.normative_references import EVERY_ACT, LIST_NAME, PREFERENCE, lists, memar_place
from modules.process.project.services.preferences import preferences_path, preferences_text
from modules.knowledge.content.services.task_context import read_record
from modules.knowledge.documentation.plan.labels.task_kind import TaskKind
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
    """The label of a task kind a plan carries; a word that is none gets an identifier nothing defines."""
    known = {d.label.word: d.label for d in task_kind.LABEL_KIND.closed}
    return known.get(word) or Label(word, new_id())

def plan_with(kind: str | None=None, request: str='Do the thing.', steps: str='', project: Path=Path('/project')) -> str:
    base = plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', project, labels=Labels((_kind_label(kind),)) if kind else None)
    return base.replace('## Request\n', f'## Request\n{request}\n').replace('## Steps\n', f'## Steps\n{steps}\n')

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        skill = self.fake_root / '.agents' / 'skills' / 'memar' / 'SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text(SKILL, encoding='utf-8', newline='\n')
        for name, text in DOCS.items():
            (self.fake_root / 'docs').mkdir(exist_ok=True)
            (self.fake_root / 'docs' / name).write_text(text, encoding='utf-8', newline='\n')
        for path in REAL:
            (self.fake_root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, self.fake_root / path)
        for name, text in OTHERS.items():
            path = self.fake_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')

    def session(self, plan: str) -> str:
        folder = memar_fs.task_dir(SID, create=True)
        (folder / PLAN_NAME).write_text(plan, encoding='utf-8', newline='\n')
        return SID

    def text(self, plan: str | None=None, with_skill: bool=True) -> str:
        if plan is not None:
            self.session(plan)
        return session_start.start_text(SID, with_skill=with_skill)

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

class PartsInOrder(Fixture):

    def test_the_text_is_marked_parts_in_one_order(self) -> None:
        self.assertEqual(list(self.parts(plan_with())), ['task', 'model', PLAN_NAME, 'folder', 'skill', 'documents', 'commands', 'help', 'ending'])

    def test_without_the_skill_the_skill_is_left_out(self) -> None:
        parts = self.parts(plan_with(), with_skill=False)
        self.assertEqual(list(parts), ['task', 'model', PLAN_NAME, 'folder', 'documents', 'commands', 'help', 'ending'])
        self.assertNotIn('SKILL-TEXT', ''.join(parts.values()))

    def test_nothing_comes_before_the_first_mark(self) -> None:
        self.assertTrue(self.text(plan_with()).startswith(MARK))

class SessionPart(Fixture):

    def test_the_id_and_the_paths_are_printed(self) -> None:
        part = self.parts(plan_with())['task']
        folder = memar_fs.task_dir(SID)
        for line in (f'task_id: {SID}', f'path: {folder}', f'plan: {folder / PLAN_NAME}', f'report: {folder / REPORT_NAME}'):
            self.assertIn(line, part)

    def test_starting_leaves_the_report_and_the_role_folders_there(self) -> None:
        self.text(plan_with())
        folder = memar_fs.task_dir(SID)
        self.assertTrue((folder / REPORT_NAME).is_file())
        self.assertTrue((folder / 'docs').is_dir())

class ModelPart(Fixture):

    def test_a_kind_that_is_judgment_names_the_strongest_model_and_the_block(self) -> None:
        for kind in (word for word in session_plan_labels.STRONG_KINDS if word in session_plan_labels.TASK_KINDS):
            with self.subTest(kind=kind):
                part = self.parts(plan_with(kind))['model']
                self.assertIn(f'kind: {kind}', part)
                self.assertIn('strongest model', part)
                self.assertIn('end Blocked', part)

    def test_a_refused_stronger_model_does_not_block_the_task(self) -> None:
        part = self.parts(plan_with('design'))['model']
        self.assertIn('strongest usable one is the right one', part)
        self.assertIn('goes on', part)

    def test_a_mechanical_kind_names_a_cheaper_model(self) -> None:
        part = self.parts(plan_with('mechanical'))['model']
        self.assertIn('kind: mechanical', part)
        self.assertIn('cheaper model', part)
        self.assertNotIn('strongest', part)

    def test_a_plan_with_no_kind_leaves_it_to_the_request(self) -> None:
        part = self.parts(plan_with())['model']
        self.assertIn('the plan states no kind', part)
        self.assertIn('ideates, designs, or critiques', part)

    def test_a_label_that_is_no_task_kind_is_not_taken_for_a_cheaper_one(self) -> None:
        part = self.parts(plan_with('modelling'))['model']
        self.assertIn('the plan states no kind', part)
        self.assertNotIn('This task is mechanical', part)

class PlanAndFolder(Fixture):

    def test_the_plan_is_printed_whole(self) -> None:
        plan = plan_with(request='Unique request words.')
        self.assertIn(plan.strip(), self.parts(plan)[PLAN_NAME])

    def test_the_folder_listing_names_files_and_marks_folders(self) -> None:
        part = self.parts(plan_with())['folder']
        lines = part.splitlines()
        self.assertIn(PLAN_NAME, lines)
        self.assertIn(REPORT_NAME, lines)
        self.assertIn('docs/', lines)

def headers(part: str) -> list[str]:
    """The passage headers of a documents part, as `path#anchor`, without a range's end."""
    return [line[4:].split(' through ')[0].removesuffix(' ---') for line in part.splitlines() if line.startswith('--- ')]

class Documents(Fixture):

    def test_each_kind_prints_its_passages_and_no_other(self) -> None:
        for kind in (kind for kind in TaskKind if kind.carried):
            with self.subTest(kind=kind.word):
                plan = plan_with(kind.word)
                found = [line for line in headers(self.parts(plan)['documents']) if '(description)' not in line]
                printed = self.compose_heads(kind)
                self.assertEqual(found, printed)

    def compose_heads(self, kind: TaskKind) -> list[str]:
        from modules.knowledge.content.services.task_context import context_text
        return [line for line in headers(context_text([memar_place(self.fake_root)], [kind])) if '(description)' not in line]

    def test_a_plan_with_no_kind_or_a_mistyped_one_prints_the_every_act_sections(self) -> None:
        for plan in (plan_with(), plan_with('modelling')):
            with self.subTest(plan=plan[:40]):
                found = headers(self.parts(plan)['documents'])
                self.assertEqual(sorted(found), sorted(EVERY_ACT_HEADS))

    def test_the_documents_part_opens_with_its_first_line(self) -> None:
        part = self.parts(plan_with('design'))['documents']
        self.assertTrue(part.splitlines()[0].startswith('kinds: design; '), part.splitlines()[:2])

    def test_the_lists_of_the_project_the_plan_names_are_read(self) -> None:
        project = self.fake_root / 'orchard'
        (project / 'docs').mkdir(parents=True)
        (project / 'docs' / 'own.md').write_text('# Own\n\n## Mine\nMINE-TEXT\n', encoding='utf-8', newline='\n')
        (project / 'rules').mkdir()
        mark = section_hash(by_anchor('# Own\n\n## Mine\nMINE-TEXT\n', 'mine'))
        (project / 'rules' / LIST_NAME.format(word=TaskKind.DESIGN.word)).write_text(f'# Orchard\nWhy.\n\n- [Own → Mine](../docs/own.md#mine) — OWN-WHY `reviewed {mark}`\n', encoding='utf-8', newline='\n')
        preferences = preferences_path(project)
        preferences.write_text(preferences_text({PREFERENCE: 'rules, rules/gone'}), encoding='utf-8', newline='\n')
        part = self.parts(plan_with('design', project=project))['documents']
        self.assertIn('--- orchard: docs/own.md#mine ---\nWhy: OWN-WHY\n## Mine\nMINE-TEXT', part)
        self.assertIn(", 1 from this project's", part.splitlines()[0])
        self.assertIn('rules/gone', part.splitlines()[0])

    def test_what_the_documents_part_printed_is_recorded_in_the_session(self) -> None:
        self.parts(plan_with('design'))
        recorded = read_record(memar_fs.task_dir(SID))
        self.assertIn(('memar', 'docs/modeling.md', 'abstract'), {line[:3] for line in recorded})
        self.assertTrue(all(('\\' not in line.path for line in recorded)))

    def test_a_design_prints_no_khayyam_passage_unless_its_steps_name_one(self) -> None:
        design = self.parts(plan_with('design'))['documents']
        self.assertIn('docs/modeling.md#abstract', headers(design))
        self.assertNotIn('khayyam', design.lower())
        named = self.parts(plan_with('design', steps=f'1. read {KHAYYAM}. Local.'))['documents']
        self.assertIn(KHAYYAM.lstrip('/'), headers(named))

    def test_a_practice_has_its_description_once(self) -> None:
        part = self.parts(plan_with('implement'))['documents']
        self.assertEqual(part.count('--- modules/process/test/test.practice.md (description) ---'), 1)

    def test_a_step_document_the_kind_already_prints_is_not_printed_again(self) -> None:
        steps = '1. read /docs/modeling.md#abstract and docs/modeling.practice.md#the-modeling-workflow. Local.'
        found = headers(self.parts(plan_with('design', steps=steps))['documents'])
        self.assertEqual(found.count('docs/modeling.md#abstract'), 1)
        self.assertEqual(found.count('docs/modeling.practice.md#the-modeling-workflow'), 1)

    def test_a_document_the_steps_name_is_read_at_its_section_or_its_abstract(self) -> None:
        steps = '1. local: read /docs/steps.md#detail and `docs/plain.md`, then act.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('STEPS-DETAIL', part)
        self.assertNotIn('STEPS-ABSTRACT', part)
        self.assertIn('PLAIN-ABSTRACT', part)
        self.assertNotIn('PLAIN-BODY', part)
        self.assertLess(part.index('docs/cognition.md#abstract'), part.index('STEPS-DETAIL'))

    def test_a_document_named_twice_is_printed_once(self) -> None:
        steps = 'read /docs/steps.md#detail, again /docs/steps.md#detail'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertEqual(part.count('STEPS-DETAIL'), 1)

    def test_documents_named_outside_the_steps_are_not_read(self) -> None:
        plan = plan_with('mechanical', request='See /docs/steps.md#detail.')
        self.assertNotIn('STEPS-DETAIL', self.parts(plan)['documents'])

    def test_a_document_that_is_not_there_is_said_and_the_rest_still_printed(self) -> None:
        steps = 'read /docs/missing.md#x and /docs/steps.md#detail'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('docs/missing.md', part)
        self.assertIn('is not there', part)
        self.assertIn('STEPS-DETAIL', part)

    def test_a_section_that_is_not_there_is_said(self) -> None:
        steps = 'read /docs/steps.md#nowhere'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('no section answers to #nowhere', part)

    def test_a_step_document_under_modules_is_read_from_that_top_folder(self) -> None:
        steps = '1. read `modules/process/example/example.md`. Local.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('--- modules/process/example/example.md (Abstract) ---', part)
        self.assertIn('EXAMPLE-ABSTRACT', part)
        self.assertNotIn('EXAMPLE-BODY', part)

    def test_a_step_document_under_bundles_is_read_from_that_top_folder(self) -> None:
        steps = '1. read /bundles/example/example.md. Local.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('BUNDLE-ABSTRACT', part)

    def test_a_step_document_with_no_abstract_is_read_at_its_first_section(self) -> None:
        steps = '1. read `modules/process/headless/headless.md`. Local.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('--- modules/process/headless/headless.md (first section) ---', part)
        self.assertIn('HEADLESS-WHY', part)
        self.assertNotIn('HEADLESS-HOW', part)
        self.assertNotIn('no section answers', part)

    def test_a_step_document_with_no_abstract_and_no_section_prints_its_description(self) -> None:
        steps = '1. read `modules/process/described/described.md`. Local.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertIn('DESCRIBED-DESCRIPTION', part)
        self.assertNotIn('no section answers', part)

    def test_a_bare_file_name_and_a_url_are_no_step_documents(self) -> None:
        steps = '1. read example.md and https://example.com/modules/process/example/example.md. Local.'
        part = self.parts(plan_with('mechanical', steps=steps))['documents']
        self.assertNotIn('EXAMPLE-ABSTRACT', part)

class SkillPart(Fixture):

    def test_the_skill_is_printed_whole(self) -> None:
        self.assertIn(SKILL.strip(), self.parts(plan_with())['skill'])

class Commands(Fixture):

    def test_the_part_is_the_card_the_command_module_generates(self) -> None:
        part = self.parts(plan_with())['commands']
        self.assertEqual(part.strip(), commands.card_text().strip())
        self.assertIn('memar content write', part)

class Help(Fixture):

    def test_the_help_every_session_needs_is_printed(self) -> None:
        part = self.parts(plan_with())['help']
        self.assertIn('`memar task --help`', part)
        self.assertIn('usage: memar task', part)
        self.assertIn('`memar content write --help`', part)
        self.assertIn('usage: memar content write', part)

    def test_the_help_of_a_command_the_plan_names_is_printed_once(self) -> None:
        plan = plan_with(request='Run `memar content search PATTERN` then `memar content search X --flag`.')
        part = self.parts(plan)['help']
        self.assertEqual(part.count('`memar content search --help`'), 1)
        self.assertIn('usage: memar content search', part)

    def test_a_flag_or_a_placeholder_ends_the_command_words(self) -> None:
        plan = plan_with(request='Run `memar content get-section FILE HEADING` and `memar task priority --help`.')
        part = self.parts(plan)['help']
        self.assertIn('`memar content get-section --help`', part)
        self.assertIn('`memar task priority --help`', part)

    def test_a_command_that_does_not_exist_is_said(self) -> None:
        part = self.parts(plan_with(request='Run `memar nothing here`.'))['help']
        self.assertIn('`memar nothing here`', part)
        self.assertIn('no such command', part)

    def test_the_commands_of_a_plan_are_read_from_anywhere_in_it(self) -> None:
        part = self.parts(plan_with(steps='1. run `memar content resolve-path REF`'))['help']
        self.assertIn('usage: memar content resolve-path', part)

class Ending(Fixture):

    def test_what_a_sub_agent_does_last_is_printed(self) -> None:
        part = self.parts(plan_with())['ending']
        for phrase in ('without rewriting', '`memar task --help`', 'return the report as your final text', '`memar content write --create FILE --content-file SCRATCHFILE`', session_temp.TEMP_SENTENCE):
            self.assertIn(phrase, part)

    def test_the_folder_rule_is_said_once_in_the_session_help(self) -> None:
        parts = self.parts(plan_with())
        self.assertIn('holds only plan.md and report.md', parts['help'])
        self.assertNotIn('plan.md and report.md', parts['ending'])

class SessionHelp(Fixture):

    def test_its_verbs_are_left_to_the_card(self) -> None:
        parts = self.parts(plan_with())
        session_help = parts['help'].split('--- `memar content write --help` ---')[0]
        self.assertIn(session_start.CARD_POINTER, session_help)
        self.assertNotIn('\nverbs:', session_help)
        self.assertIn('memar task ensure', parts['commands'])
SMALL = 8000

def body(part: str) -> str:
    """PART without its closing line."""
    return part[:part.rindex(CLOSING_MARK)] if CLOSING_MARK in part else part

class InParts(Fixture):

    def printed(self, part: int, with_skill: bool=True, most: int | None=SMALL) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_start.get_task_init_context(SID, with_skill, part=part, most=most)
        return out.getvalue()

    def every_part(self, with_skill: bool=True, most: int | None=SMALL) -> list[str]:
        parts = [self.printed(1, with_skill, most)]
        while 'the last' not in parts[-1][parts[-1].rindex(CLOSING_MARK):]:
            parts.append(self.printed(len(parts) + 1, with_skill, most))
        return parts

    def test_the_passages_joined_are_the_text(self) -> None:
        self.session(plan_with('implement'))
        self.assertEqual(''.join(session_start.start_passages(SID)), session_start.start_text(SID))

    def test_every_part_run_in_order_joins_to_the_text_each_under_the_bound(self) -> None:
        self.session(plan_with('implement'))
        parts = self.every_part()
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), SMALL)
        self.assertEqual(''.join((body(part) for part in parts)), session_start.start_text(SID))

    def test_a_closing_line_names_start_with_the_same_flags_and_the_next_part(self) -> None:
        self.session(plan_with('implement'))
        first = self.printed(1, with_skill=False)
        self.assertIn(f'`memar ai get-task-init-context --task-id {SID} --without-skill --most-characters {SMALL} --part 2`', first)

    def test_a_text_under_the_bound_prints_whole_with_no_closing_line(self) -> None:
        self.session(plan_with('implement'))
        whole = self.printed(1, most=10 * len(session_start.start_text(SID)))
        self.assertNotIn(CLOSING_MARK, whole)
        self.assertEqual(whole, session_start.start_text(SID))

    def test_the_default_bound_is_the_declared_one(self) -> None:
        self.session(plan_with('implement'))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_start.get_task_init_context(SID)
        self.assertLessEqual(len(out.getvalue()), MOST_CHARACTERS)

    def project_preferring(self, value: str) -> Path:
        """A project whose preferences file sets `most-characters` to VALUE, and a session of it."""
        project = self.fake_root / 'project'
        project.mkdir(parents=True)
        (project / 'manifest.yaml').write_text(f'memar:\n  sessions:\n  most-characters: {value}\n', encoding='utf-8', newline='\n')
        self.session(plan_with('implement', project=project))
        return project

    def test_the_projects_preference_is_the_bound_and_no_closing_line_names_it(self) -> None:
        self.project_preferring(str(SMALL))
        parts = self.every_part(most=None)
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), SMALL)
        self.assertIn(f'`memar ai get-task-init-context --task-id {SID} --part 2`', parts[0])
        self.assertEqual(''.join((body(part) for part in parts)), session_start.start_text(SID))

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
        self.session(plan_with('implement'))
        parts = self.every_part()
        whole = text_id(session_start.start_text(SID))
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertIn(f'{CLOSING_MARK} part {number} of {len(parts)} of text {whole}', part)

class Refusal(Fixture):

    def test_a_session_with_no_folder_is_refused_naming_how_one_is_opened(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            session_start.start_text(SID)
        self.assertIn(f'no task to start in {SID}', str(refused.exception.code))
        self.assertIn('`memar task ensure --title T --parent ID --project NAME`', str(refused.exception.code))

    def test_a_session_with_no_plan_is_refused(self) -> None:
        memar_fs.task_dir(SID, create=True)
        with self.assertRaises(SystemExit) as refused:
            session_start.start_text(SID)
        self.assertIn(f'no task to start in {SID}', str(refused.exception.code))

    def test_run_prints_the_text_and_a_refusal_prints_nothing(self) -> None:
        self.session(plan_with())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_start.get_task_init_context(SID)
        self.assertTrue(out.getvalue().startswith(MARK))
        with contextlib.redirect_stdout(io.StringIO()) as nothing, self.assertRaises(SystemExit):
            session_start.get_task_init_context('a/b')
        self.assertEqual(nothing.getvalue(), '')

class StartHelp(unittest.TestCase):

    def test_the_help_says_what_it_prints_names_the_kinds_and_offers_without_skill(self) -> None:
        environment = dict(os.environ, COLUMNS='100', PYTHONIOENCODING='utf-8', MEMAR_NO_AUTO_UPDATE='1')
        done = subprocess.run([sys.executable, str(SCRIPTS / 'memar'), 'ai', 'start', '--help'], capture_output=True, env=environment)
        self.assertEqual(done.returncode, 0, done.stderr)
        shown = ' '.join(done.stdout.decode('utf-8').split())
        for phrase in ('--without-skill', '--part', '--most-characters', 'memar content get-act-context', 'every agent', ', '.join(session_plan_labels.TASK_KINDS)):
            self.assertIn(phrase, shown)
if __name__ == '__main__':
    unittest.main(verbosity=2)
