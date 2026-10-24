#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for composing the context of a set of kinds, in `modules/knowledge/content/services/task_context.py`.

    python modules/knowledge/content/tests/task_context.py

The subject is the one composition `memar ai get-task-init-context` and
`memar content get-act-context` both print, from the lists of
[Normative References](../../rules/normative_references/normative_references.md),
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Two kinds of pin. The shape of the composition is pinned on small documents
and lists of the suite's own, in a scratch checkout, so no pin depends on what
the real documents or lists say; on the real tree only that each kind's
context is not empty and that the command prints the composition, read and
never written, so no pin holds a copy of a list.

What is pinned, and what each pin is for:

  Order            The every-act sections print first, then each kind's in the
                   order the kinds are given; within one list, documents by
                   path and sections in document order, whatever order the
                   list writes them in; each under a line naming it and,
                   below it, its entry's why. A document a plan names with no
                   anchor is read at its Abstract.
  FirstLine        The first line names the kinds and counts the sections the
                   lists gave; with no project named it says Memar's lists
                   alone.
  Once             A section two kinds name prints once, and so does one that
                   lies inside another printed section, whichever comes first.
  Description      A Practice's `description` prints once, above its first
                   section; a document with none has nothing printed for it.
  Marked           A section changed since its entry's mark prints as it reads
                   now, marked with the entry's list and line; an entry whose
                   anchor or document is gone prints its link, label and why,
                   marked; both are counted on the first line.
  Dropped          A drop prints where the passage would have stood, with its
                   list, line and reason, and is counted; an every-act section
                   is never dropped.
  Record           What a context printed is recorded, a line per section, with
                   forward slashes; with kinds already read, the sections the
                   record holds with the same hash are left out, a section
                   changed between two prints prints again, and a section added
                   to a list since prints.
  Project          A project's lists, read only in the folders its
                   `normative_references` preference names and not below them,
                   add their sections after Memar's, the project's own named
                   under its folder's name and a passage of Memar named by its
                   published address read from Memar's checkout; the first line
                   counts them apart. A project's drop of a passage of Memar
                   prints where the passage stood and is counted as the
                   project's; a drop with no reason drops nothing, and an
                   every-act section prints whatever the project's lists say.
                   A named folder that does not exist is said on the first
                   line; a project that names none reads Memar's lists alone.
  Absence          A document a plan names that is not there, or a section of it,
                   is said, and the rest still printed.
  Real             Every kind's context, on the real lists, is not empty.
  CommandLine      `memar content get-act-context` prints the composition, its help
                   lists every kind with when it applies; `--after` without
                   `--task-id` is refused; with `--task-id` the record is
                   written and `--after` subtracts it, and covering everything
                   says so; a project named by its flag has its lists read. A composition past the bound prints in ordered
                   parts, as `machine/console_parts.py` cuts them between its
                   blocks: each part under the bound, every part run in order
                   joins to the composition, and each closing line names the
                   verb again with the same kinds and the next part. With a
                   project named, its `most-characters` preference is the
                   bound, and the closing line names the project, not the bound.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
PUBLISHED_PAGES = _m_fs_memar.PUBLISHED_PAGES
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import argparse
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from machine.console_parts import CLOSING_MARK, MOST_CHARACTERS
from modules.knowledge.content.services.get_section import by_anchor, section_hash
from modules.knowledge.content.services.normative_references import EVERY_ACT, LIST_NAME, MEMAR_PLACE, PREFERENCE, memar_place
from modules.process.project.services.preferences import preferences_path, preferences_text
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, plan_skeleton
from modules.knowledge.content.services.task_context import CHANGED_DO, GONE_DO, Printed, Ref, compose, context, context_places, context_text, read_record, record_path, write_record
from modules.knowledge.documentation.primitive.label import Label, Labels
from modules.knowledge.documentation.plan.labels.task_kind import TaskKind
ROOT = SCRIPTS.parent.parent
LAUNCHER = SCRIPTS / 'memar'
DOCS = {'plain.md': '# Plain\n\n## Abstract\nPLAIN-ABSTRACT\n\n## One\nONE-TEXT\n\n## Two\nTWO-TEXT\n\n## Three\nTHREE-TEXT\n', 'way.practice.md': '---\nname: way\ndescription: WAY-DESCRIPTION\n---\n\n# Way Practice\n\n## First\nFIRST-TEXT\n\n## Second\nSECOND-TEXT\n\n### Inner\nINNER-TEXT\n\n## Third\nTHIRD-TEXT\n', 'core.md': '# Core\n\n## Abstract\nCORE-ABSTRACT\n\n## Norms\nCORE-NORMS\n'}
DESIGN, CRITIQUE = (TaskKind.DESIGN, TaskKind.CRITIQUE)

class Fixture(unittest.TestCase):
    """A scratch checkout: documents under docs/, and lists in Memar's place written by `lists`."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()
        (self.root / 'docs').mkdir()
        for name, text in DOCS.items():
            self.document(name, text)
        self.place = memar_place(self.root)
        self.place.folder.mkdir(parents=True)
        self.lists({EVERY_ACT: [('core.md', 'norms')]})

    def document(self, name: str, text: str) -> None:
        (self.root / 'docs' / name).write_text(text, encoding='utf-8', newline='\n')

    def entry(self, name: str, anchor: str, why: str='', mark: str | None=None, drop: bool=False) -> str:
        """An entry line naming docs/NAME#ANCHOR, marked with its section's current hash unless MARK is given."""
        if drop:
            return f"- Not read here: [{name}](../../../../../docs/{name}#{anchor}) — {why or 'not here.'}"
        if mark is None:
            found = by_anchor((self.root / 'docs' / name).read_text(encoding='utf-8'), anchor)
            mark = section_hash(found) if found else '0' * 12
        return f"- [{name} → {anchor}](../../../../../docs/{name}#{anchor}) — {why or f'WHY-{anchor}'} `reviewed {mark}`"

    def lists(self, given: dict) -> None:
        """Write each list GIVEN names: a word, and its entries as (name, anchor) or ready lines."""
        for word, entries in given.items():
            lines = [entry if isinstance(entry, str) else self.entry(*entry) for entry in entries]
            text = f'# Normative References — {word}\nWhy.\n\n' + '\n'.join(lines) + '\n'
            (self.place.folder / LIST_NAME.format(word=word)).write_text(text, encoding='utf-8', newline='\n')

    def text(self, kinds, **given) -> str:
        return context_text([self.place], kinds, **given)

def headers(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith('--- ')]

class Order(Fixture):

    def test_every_act_first_then_each_kind_in_the_order_given(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'two')], CRITIQUE.word: [('plain.md', 'one')]})
        found = headers(self.text([CRITIQUE, DESIGN]))
        self.assertEqual(found, ['--- docs/core.md#norms ---', '--- docs/plain.md#one ---', '--- docs/plain.md#two ---'])

    def test_within_a_list_documents_by_path_and_sections_in_document_order(self) -> None:
        self.lists({DESIGN.word: [('way.practice.md', 'third'), ('plain.md', 'three'), ('way.practice.md', 'first'), ('plain.md', 'one')]})
        found = [line for line in headers(self.text([DESIGN])) if '(description)' not in line]
        self.assertEqual(found, ['--- docs/core.md#norms ---', '--- docs/plain.md#one ---', '--- docs/plain.md#three ---', '--- docs/way.practice.md#first ---', '--- docs/way.practice.md#third ---'])

    def test_each_section_prints_under_its_line_and_its_why(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one', 'ONE-WHY')]})
        text = self.text([DESIGN])
        self.assertIn('--- docs/plain.md#one ---\nWhy: ONE-WHY\n## One\nONE-TEXT', text)
        self.assertNotIn('TWO-TEXT', text)

    def test_a_document_a_plan_names_with_no_anchor_is_read_at_its_abstract(self) -> None:
        text = '\n\n'.join(compose([Ref(self.root, 'docs/plain.md')]).blocks)
        self.assertIn('--- docs/plain.md (Abstract) ---', text)
        self.assertIn('PLAIN-ABSTRACT', text)
        self.assertNotIn('ONE-TEXT', text)

class FirstLine(Fixture):

    def test_the_first_line_names_the_kinds_and_counts_the_sections(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one'), ('plain.md', 'two')]})
        self.assertEqual(self.text([DESIGN]).splitlines()[0], "kinds: design; 3 sections from Memar's lists")

    def test_with_no_project_named_it_says_memars_lists_alone(self) -> None:
        first = self.text([DESIGN], project_named=False).splitlines()[0]
        self.assertTrue(first.endswith("; no project named, so Memar's lists alone"), first)

class Once(Fixture):

    def test_a_section_two_kinds_name_prints_once(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')], CRITIQUE.word: [('plain.md', 'one'), ('plain.md', 'two')]})
        text = self.text([DESIGN, CRITIQUE])
        self.assertEqual(text.count('ONE-TEXT'), 1)
        self.assertIn('TWO-TEXT', text)

    def test_a_section_inside_another_prints_once_whichever_comes_first(self) -> None:
        for first, second in ((DESIGN, CRITIQUE), (CRITIQUE, DESIGN)):
            with self.subTest(first=first.word):
                self.lists({DESIGN.word: [('way.practice.md', 'inner')], CRITIQUE.word: [('way.practice.md', 'second')]})
                text = self.text([first, second])
                self.assertEqual(text.count('INNER-TEXT'), 1)
                self.assertNotIn('--- docs/way.practice.md#inner ---', text)

class Description(Fixture):

    def test_a_practice_has_its_description_once_above_its_first_section(self) -> None:
        self.lists({DESIGN.word: [('way.practice.md', 'first'), ('way.practice.md', 'third'), ('plain.md', 'one')]})
        text = self.text([DESIGN])
        self.assertEqual(text.count('WAY-DESCRIPTION'), 1)
        self.assertLess(text.index('ONE-TEXT'), text.index('WAY-DESCRIPTION'))
        self.assertLess(text.index('WAY-DESCRIPTION'), text.index('--- docs/way.practice.md#first ---'))

    def test_a_document_with_no_description_has_none_printed(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')]})
        self.assertNotIn('(description)', self.text([DESIGN]))

class Marked(Fixture):

    def test_a_section_changed_since_reviewed_prints_as_it_reads_now_marked(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')]})
        self.document('plain.md', DOCS['plain.md'].replace('ONE-TEXT', 'ONE-EDITED'))
        text = self.text([DESIGN])
        where = f'{MEMAR_PLACE.as_posix()}/{LIST_NAME.format(word=DESIGN.word)}:4'
        self.assertIn(f'--- docs/plain.md#one (changed since reviewed: {where}) ---\n{CHANGED_DO.format(located=where)}\n', text)
        self.assertIn('ONE-EDITED', text)
        self.assertIn('; 1 changed since reviewed', text.splitlines()[0])

    def test_a_broken_entry_prints_its_link_label_and_why_marked(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'gone', 'GONE-WHY'), ('missing.md', 'x', 'MISSING-WHY', '0' * 12)]})
        text = self.text([DESIGN])
        where = f'{MEMAR_PLACE.as_posix()}/{LIST_NAME.format(word=DESIGN.word)}'
        self.assertIn(f'--- docs/plain.md#gone (anchor gone: {where}:4) ---', text)
        self.assertIn('[plain.md → gone](../../../../../docs/plain.md#gone) — GONE-WHY', text)
        self.assertIn(f'--- docs/missing.md#x (anchor gone: {where}:5) ---', text)
        self.assertIn('MISSING-WHY', text)
        self.assertEqual(text.count(GONE_DO), 2)
        self.assertIn('; 2 anchor gone', text.splitlines()[0])

class Dropped(Fixture):

    def test_a_drop_prints_where_the_passage_stood_with_its_reason_and_is_counted(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one'), ('plain.md', 'two'), self.entry('plain.md', 'one', 'NO-SUCH-STEP', drop=True)]})
        text = self.text([DESIGN])
        where = f'{MEMAR_PLACE.as_posix()}/{LIST_NAME.format(word=DESIGN.word)}:6'
        self.assertNotIn('ONE-TEXT', text)
        self.assertIn(f'--- docs/plain.md#one (dropped) ---\ndropped by {where}: NO-SUCH-STEP', text)
        self.assertLess(text.index('(dropped)'), text.index('TWO-TEXT'))
        self.assertIn('; 1 passage dropped (listed below)', text.splitlines()[0])

    def test_an_every_act_section_is_never_dropped(self) -> None:
        self.lists({DESIGN.word: [('core.md', 'norms'), self.entry('core.md', 'norms', drop=True)]})
        text = self.text([DESIGN])
        self.assertIn('CORE-NORMS', text)
        self.assertNotIn('(dropped)', text)

class Record(Fixture):

    def setUp(self) -> None:
        super().setUp()
        self.folder = self.root / 'task'
        self.folder.mkdir()

    def print_and_record(self, kinds, **given) -> str:
        composed = context([self.place], kinds, record=read_record(self.folder), **given)
        write_record(self.folder, composed.printed)
        return '\n\n'.join(composed.blocks)

    def test_what_a_context_printed_is_recorded_a_line_per_section(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')]})
        self.print_and_record([DESIGN])
        lines = record_path(self.folder).read_text(encoding='utf-8').splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn(f"memar\tdocs/plain.md\tone\t{section_hash(by_anchor(DOCS['plain.md'], 'one'))}", lines)
        self.print_and_record([DESIGN])
        self.assertEqual(len(record_path(self.folder).read_text(encoding='utf-8').splitlines()), 2, 'recorded once')

    def test_after_leaves_out_what_the_record_holds_with_the_same_hash(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')], CRITIQUE.word: [('plain.md', 'one'), ('plain.md', 'two')]})
        self.print_and_record([DESIGN])
        text = self.print_and_record([CRITIQUE], after=[DESIGN])
        self.assertNotIn('ONE-TEXT', text)
        self.assertNotIn('CORE-NORMS', text)
        self.assertIn('TWO-TEXT', text)
        self.assertIn('after design: 2 sections already printed left out', text.splitlines()[0])

    def test_a_section_changed_between_two_prints_prints_again(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')], CRITIQUE.word: [('plain.md', 'one')]})
        self.print_and_record([DESIGN])
        self.document('plain.md', DOCS['plain.md'].replace('ONE-TEXT', 'ONE-EDITED'))
        text = self.print_and_record([CRITIQUE], after=[DESIGN])
        self.assertIn('ONE-EDITED', text)
        self.assertNotIn('CORE-NORMS', text)

    def test_a_section_added_to_the_earlier_kinds_list_since_it_printed_prints(self) -> None:
        self.lists({DESIGN.word: [('plain.md', 'one')], CRITIQUE.word: [('plain.md', 'one'), ('plain.md', 'three')]})
        self.print_and_record([DESIGN])
        self.lists({DESIGN.word: [('plain.md', 'one'), ('plain.md', 'three')]})
        text = self.print_and_record([CRITIQUE], after=[DESIGN])
        self.assertIn('THREE-TEXT', text)
        self.assertNotIn('ONE-TEXT', text)

    def test_a_description_printed_with_the_record_is_not_printed_again(self) -> None:
        self.lists({DESIGN.word: [('way.practice.md', 'first')], CRITIQUE.word: [('way.practice.md', 'first'), ('way.practice.md', 'third')]})
        self.print_and_record([DESIGN])
        text = self.print_and_record([CRITIQUE], after=[DESIGN])
        self.assertNotIn('WAY-DESCRIPTION', text)
        self.assertIn('THIRD-TEXT', text)

    def test_the_record_is_read_back_as_printed(self) -> None:
        printed = [Printed('memar', 'docs/plain.md', 'one', '0' * 12)]
        write_record(self.folder, printed)
        self.assertEqual(read_record(self.folder), set(printed))

class Absence(Fixture):

    def test_a_missing_document_or_section_a_plan_names_is_said_and_the_rest_printed(self) -> None:
        refs = [Ref(self.root, 'docs/missing.md', 'x'), Ref(self.root, 'docs/plain.md', 'nowhere'), Ref(self.root, 'docs/plain.md', 'one')]
        text = '\n\n'.join(compose(refs).blocks)
        self.assertIn('the document docs/missing.md is not there', text)
        self.assertIn('no section answers to #nowhere in docs/plain.md', text)
        self.assertIn('ONE-TEXT', text)
OWN = '# Own\n\n## Abstract\nOWN-ABSTRACT\n\n## Mine\nMINE-TEXT\n'

class Project(Fixture):
    """A project inside the scratch checkout, its lists in the folder its preference names, beside Memar's."""

    def setUp(self) -> None:
        super().setUp()
        self.project = self.root / 'orchard'
        (self.project / 'docs').mkdir(parents=True)
        (self.project / 'docs' / 'own.md').write_text(OWN, encoding='utf-8', newline='\n')
        self.refs = self.project / 'rules' / 'refs'
        self.refs.mkdir(parents=True)
        self.prefer('rules/refs')
        self.lists({DESIGN.word: [('plain.md', 'one'), ('plain.md', 'two')]})

    def prefer(self, value: str) -> None:
        path = preferences_path(self.project)
        path.write_text(preferences_text({PREFERENCE: value}), encoding='utf-8', newline='\n')

    def own(self, anchor: str) -> str:
        mark = section_hash(by_anchor(OWN, anchor))
        return f'- [Own → {anchor}](../../docs/own.md#{anchor}) — OWN-WHY `reviewed {mark}`'

    def published(self, name: str, anchor: str, drop: str | None=None) -> str:
        link = f'[{name} → {anchor}]({PUBLISHED_PAGES}docs/{name}#{anchor})'
        if drop is not None:
            return f'- Not read here: {link}' + (f' — {drop}' if drop else '')
        mark = section_hash(by_anchor((self.root / 'docs' / name).read_text(encoding='utf-8'), anchor))
        return f'- {link} — PUBLISHED-WHY `reviewed {mark}`'

    def project_list(self, word: str, *lines: str, folder: Path | None=None) -> None:
        text = f'# Orchard — {word}\nWhy.\n\n' + '\n'.join(lines) + '\n'
        (folder or self.refs).mkdir(parents=True, exist_ok=True)
        ((folder or self.refs) / LIST_NAME.format(word=word)).write_text(text, encoding='utf-8', newline='\n')

    def text(self, kinds) -> str:
        places, problems = context_places(self.root, self.project)
        return context_text(places, kinds, place_problems=problems)

    def test_a_projects_added_section_prints_after_memars_and_is_counted(self) -> None:
        self.project_list(DESIGN.word, self.own('mine'))
        text = self.text([DESIGN])
        self.assertEqual(headers(text), ['--- docs/core.md#norms ---', '--- docs/plain.md#one ---', '--- docs/plain.md#two ---', '--- orchard: docs/own.md#mine ---'])
        self.assertIn('--- orchard: docs/own.md#mine ---\nWhy: OWN-WHY\n## Mine\nMINE-TEXT', text)
        self.assertEqual(text.splitlines()[0], "kinds: design; 3 sections from Memar's lists, 1 from this project's")

    def test_a_passage_of_memar_named_by_its_published_address_prints_from_memars_checkout(self) -> None:
        self.project_list(DESIGN.word, self.published('plain.md', 'three'))
        text = self.text([DESIGN])
        self.assertEqual(headers(text)[-1], '--- docs/plain.md#three ---')
        self.assertIn('Why: PUBLISHED-WHY\n## Three\nTHREE-TEXT', text)

    def test_a_drop_prints_where_the_passage_stood_and_is_counted(self) -> None:
        self.project_list(DESIGN.word, self.published('plain.md', 'one', drop='NO-ORCHARD-STEP'))
        text = self.text([DESIGN])
        self.assertNotIn('ONE-TEXT', text)
        where = f'orchard: rules/refs/{LIST_NAME.format(word=DESIGN.word)}:4'
        self.assertIn(f'--- docs/plain.md#one (dropped) ---\ndropped by {where}: NO-ORCHARD-STEP', text)
        self.assertLess(text.index('(dropped)'), text.index('TWO-TEXT'))
        self.assertIn('; 1 passage of Memar dropped by this project (listed below)', text.splitlines()[0])

    def test_a_drop_with_no_reason_drops_nothing(self) -> None:
        self.project_list(DESIGN.word, self.published('plain.md', 'one', drop=''))
        text = self.text([DESIGN])
        self.assertIn('ONE-TEXT', text)
        self.assertNotIn('(dropped)', text)

    def test_an_every_act_section_prints_whatever_the_projects_lists_say(self) -> None:
        for word in (EVERY_ACT, DESIGN.word):
            self.project_list(word, self.published('core.md', 'norms', drop='NOT-HERE'))
        text = self.text([DESIGN])
        self.assertIn('CORE-NORMS', text)
        self.assertNotIn('(dropped)', text)

    def test_a_named_folder_that_does_not_exist_is_reported_on_the_first_line(self) -> None:
        self.prefer('rules/refs, rules/gone')
        first = self.text([DESIGN]).splitlines()[0]
        self.assertIn('rules/gone', first)
        self.assertIn('not a folder', first)

    def test_a_list_outside_or_below_the_declared_folders_is_not_read(self) -> None:
        self.project_list(DESIGN.word, self.own('mine'), folder=self.project / 'docs')
        self.project_list(DESIGN.word, self.own('mine'), folder=self.refs / 'below')
        text = self.text([DESIGN])
        self.assertNotIn('MINE-TEXT', text)
        self.assertEqual(text.splitlines()[0], "kinds: design; 3 sections from Memar's lists, 0 from this project's")

    def test_a_project_that_declares_no_folder_reads_memars_lists_alone(self) -> None:
        self.prefer('')
        self.assertEqual(self.text([DESIGN]).splitlines()[0], "kinds: design; 3 sections from Memar's lists")

class Real(unittest.TestCase):

    def test_every_kinds_context_on_the_real_lists_is_not_empty(self) -> None:
        every_act = context([memar_place(ROOT)], []).listed
        self.assertGreater(every_act, 0)
        for kind in TaskKind:
            with self.subTest(kind=kind.word):
                composed = context([memar_place(ROOT)], [kind])
                self.assertGreater(composed.listed, every_act)
                self.assertEqual(composed.gone, 0)

def run_memar(*arguments: str) -> subprocess.CompletedProcess:
    environment = dict(os.environ, COLUMNS='100', PYTHONIOENCODING='utf-8', MEMAR_NO_AUTO_UPDATE='1')
    return subprocess.run([sys.executable, str(LAUNCHER), *arguments], capture_output=True, env=environment)

def every_part(*arguments: str) -> list[str]:
    """What `memar content get-act-context ARGUMENTS` prints, part after part, until the part that says it is the last."""
    parts: list[str] = []
    while True:
        done = run_memar('content', 'context', *arguments, '--part', str(len(parts) + 1))
        if done.returncode != 0:
            raise AssertionError(done.stderr.decode('utf-8'))
        parts.append(done.stdout.decode('utf-8').replace('\r\n', '\n'))
        if CLOSING_MARK not in parts[-1] or 'the last' in parts[-1][parts[-1].rindex(CLOSING_MARK):]:
            return parts

def joined(parts: list[str]) -> str:
    """PARTS without their closing lines, joined in order."""
    return ''.join((part[:part.rindex(CLOSING_MARK)] if CLOSING_MARK in part else part for part in parts)).strip()

def real(kinds, project_named: bool=False, **given) -> str:
    return context_text([memar_place(ROOT)], kinds, project_named=project_named, **given).strip()

class CommandLine(unittest.TestCase):

    def test_the_verb_prints_the_composition(self) -> None:
        self.assertEqual(joined(every_part('--kind', 'design')), real([DESIGN]))

    def test_a_composition_past_the_bound_prints_in_parts_each_under_it(self) -> None:
        bound = 8000
        parts = every_part('--kind', 'design', '--most-characters', str(bound))
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), bound)
        self.assertIn(f'`memar content get-act-context --kind design --most-characters {bound} --part 2`', parts[0])
        self.assertEqual(joined(parts), real([DESIGN]))

    def test_by_default_each_part_is_under_the_declared_bound(self) -> None:
        for number, part in enumerate(every_part('--kind', 'critique'), 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), MOST_CHARACTERS)

    def test_the_verb_takes_several_kinds(self) -> None:
        parts = every_part('--kind', 'critique', '--kind', 'plan')
        self.assertEqual(joined(parts), real([CRITIQUE, TaskKind.PLAN]))
        if len(parts) > 1:
            self.assertIn('`memar content get-act-context --kind critique --kind plan --part 2`', parts[0])

    def test_the_named_projects_preference_is_the_bound_and_the_closing_line_names_the_project(self) -> None:
        bound = 8000
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            (Path(folder) / 'manifest.yaml').write_text(f'memar:\n  most-characters: {bound}\n', encoding='utf-8', newline='\n')
            parts = every_part('--kind', 'design', '--project-path', folder)
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), bound)
        self.assertIn(f'`memar content get-act-context --kind design --project-path {folder} --part 2`', parts[0])
        self.assertEqual(joined(parts), real([DESIGN], project_named=True))

    def test_after_without_task_id_is_refused(self) -> None:
        done = run_memar('content', 'context', '--kind', 'critique', '--after', 'design')
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("--after needs --task-id: the record of what was printed is the task's", done.stderr.decode('utf-8'))
        self.assertEqual(done.stdout, b'')

    def test_the_help_lists_every_kind_with_when_it_applies(self) -> None:
        done = run_memar('content', 'context', '--help')
        self.assertEqual(done.returncode, 0, done.stderr)
        shown = ' '.join(done.stdout.decode('utf-8').split())
        for kind in TaskKind:
            with self.subTest(kind=kind.word):
                self.assertIn(f"{kind.word}: {' '.join(kind.applies.split())}", shown)
        self.assertIn('--after', shown)
        self.assertIn('--task-id', shown)

    def test_a_word_that_is_no_kind_is_refused(self) -> None:
        done = run_memar('content', 'context', '--kind', 'modelling')
        self.assertEqual(done.returncode, 2)

class CommandLineWithTask(Fixture):
    """`--task-id`, run in this process with the Memar root patched onto the scratch checkout, so the task's folder is under it."""
    SID = '20261016-T000000Z-1'

    def setUp(self) -> None:
        super().setUp()
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.root)
        patched.start()
        self.addCleanup(patched.stop)
        self.folder = memar_fs.task_dir(self.SID, create=True)
        plan = plan_skeleton(self.SID, 'Fixture', '2026-10-16T00:00:00Z', self.root, labels=Labels((Label('TaskKind', DESIGN.word),)))
        (self.folder / PLAN_NAME).write_text(plan, encoding='utf-8', newline='\n')
        self.lists({DESIGN.word: [('plain.md', 'one')], CRITIQUE.word: [('plain.md', 'one'), ('plain.md', 'two')]})

    def run_with(self, *arguments: str) -> str:
        import modules.knowledge.content.services.get_act_context as content_context
        parser = argparse.ArgumentParser()
        run = content_context.describe(parser.add_subparsers())
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            run(parser.parse_args(['get-act-context', '--task-id', self.SID, *arguments]))
        return printed.getvalue()

    def test_the_record_is_written_and_after_subtracts_it(self) -> None:
        self.run_with('--kind', DESIGN.word)
        self.assertTrue(record_path(self.folder).is_file())
        text = self.run_with('--kind', CRITIQUE.word, '--after', DESIGN.word)
        self.assertNotIn('ONE-TEXT', text)
        self.assertIn('TWO-TEXT', text)
        self.assertIn('after design: 2 sections already printed left out', text.splitlines()[0])

    def test_the_record_is_written_once_the_last_part_is_printed(self) -> None:
        self.document('plain.md', DOCS['plain.md'].replace('TWO-TEXT', 'TWO-TEXT\n\n' + 'A long paragraph. ' * 60))
        self.lists({CRITIQUE.word: [('plain.md', 'one'), ('plain.md', 'two')]})
        first = self.run_with('--kind', CRITIQUE.word, '--most-characters', '700')
        self.assertIn('--part 2', first)
        self.assertFalse(record_path(self.folder).is_file())
        last = first
        number = 1
        while 'the last' not in last:
            number += 1
            last = self.run_with('--kind', CRITIQUE.word, '--most-characters', '700', '--part', str(number))
        self.assertTrue(record_path(self.folder).is_file())

    def test_the_named_projects_lists_are_read_beside_memars(self) -> None:
        project = self.root / 'orchard'
        (project / 'docs').mkdir(parents=True)
        (project / 'docs' / 'own.md').write_text(OWN, encoding='utf-8', newline='\n')
        (project / 'rules').mkdir()
        mark = section_hash(by_anchor(OWN, 'mine'))
        (project / 'rules' / LIST_NAME.format(word=DESIGN.word)).write_text(f'# Orchard\nWhy.\n\n- [Own → Mine](../docs/own.md#mine) — OWN-WHY `reviewed {mark}`\n', encoding='utf-8', newline='\n')
        preferences = preferences_path(project)
        preferences.write_text(preferences_text({PREFERENCE: 'rules'}), encoding='utf-8', newline='\n')
        text = self.run_with('--kind', DESIGN.word, '--project-path', str(project))
        self.assertIn('MINE-TEXT', text)
        self.assertIn("2 sections from Memar's lists, 1 from this project's", text.splitlines()[0])

    def test_after_covering_everything_says_so(self) -> None:
        self.run_with('--kind', CRITIQUE.word)
        self.assertIn('already printed', self.run_with('--kind', DESIGN.word, '--after', CRITIQUE.word))

    def test_a_task_with_no_folder_is_refused(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            self.run_with_id('20261016-T000000Z-2', '--kind', DESIGN.word)
        self.assertIn('20261016-T000000Z-2', str(refused.exception.code))

    def run_with_id(self, task_id: str, *arguments: str) -> None:
        import modules.knowledge.content.services.get_act_context as content_context
        parser = argparse.ArgumentParser()
        run = content_context.describe(parser.add_subparsers())
        with contextlib.redirect_stdout(io.StringIO()):
            run(parser.parse_args(['get-act-context', '--task-id', task_id, *arguments]))
if __name__ == '__main__':
    unittest.main(verbosity=2)
