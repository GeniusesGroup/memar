#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
record = import_module('modules-plugable.knowledge.documentation.services.changelog_record')
listing = import_module('modules-plugable.knowledge.documentation.services.content_list_ai_only_changelog_records')
task_records = import_module('modules-plugable.management.task.services.task_records')
Content = import_module('modules.management.timeline.services.timeline_files').Content
CONTRIBUTORS = '# Contributors\n\n## Template\n- Full Legal Name: Legal entity name (legal persons only).\n\n### {Brand}\n- **Bio**: One line.\n\n## Omid Hekayati\n- **Bio**: Architect.\n\n## Anthropic\n- Full Legal Name: Anthropic, PBC\n\n### Claude\n- **Bio**: A model.\n\n### Claude Code\n- **Bio**: A tool.\n\n## Zhipu\n- Full Legal Name: Zhipu AI\n\n### Super Z\n- **Bio**: A model.\n'


def changelog(number: int, author: str, title: str = 'A change', placed_at: str = '2026-10-01T00:00:00Z') -> Content:
    return Content(number, {'kind': 'changelog', 'author': author, 'placed_at': placed_at}, f'### {title}\n- Type: x\n')


def approval(number: int, author: str, refs: str, verdict: str = 'approved') -> Content:
    return Content(number, {'kind': 'approval', 'author': author, 'refs': refs}, f'### Approval\n- Judges: x\n- Verdict: {verdict}\n- Examined: y\n')


class Scratch(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / 'CONTRIBUTORS.md').write_text(CONTRIBUTORS, encoding='utf-8', newline='\n')
        self.sections = record.contributor_sections(self.root / 'CONTRIBUTORS.md')


class WhoIsWho(Scratch):

    def test_a_section_is_typed_by_its_level_and_its_legal_name(self) -> None:
        self.assertEqual(self.sections['omid-hekayati'].kind, record.NATURAL_PERSON)
        self.assertEqual(self.sections['anthropic'].kind, record.LEGAL_ENTITY)
        self.assertEqual(self.sections['claude'].kind, record.BRAND_OR_TOOL)
        self.assertEqual(self.sections['claude-code'].kind, record.BRAND_OR_TOOL)
        self.assertNotIn('template', self.sections)
        self.assertNotIn('brand', self.sections)

    def test_an_author_is_an_ai_contributor_by_name_or_anchor(self) -> None:
        self.assertTrue(record.is_ai_author('Claude', self.sections))
        self.assertTrue(record.is_ai_author('super-z', self.sections))
        self.assertFalse(record.is_ai_author('Omid Hekayati', self.sections))
        self.assertFalse(record.is_ai_author('Anthropic', self.sections))
        self.assertFalse(record.is_ai_author('ghost', self.sections))
        self.assertFalse(record.is_ai_author(None, self.sections))


class AiOnlyChangelogs(Scratch):

    def listed(self, contents) -> list:
        return [(task, number) for task, number, _, _ in record.ai_only_changelogs(contents, self.sections)]

    def test_a_changelog_by_a_model_with_no_approval_is_listed_with_its_title(self) -> None:
        found = record.ai_only_changelogs([('T-1', changelog(2, 'Claude', 'Fixed the lint'))], self.sections)
        self.assertEqual(found, [('T-1', 2, 'Fixed the lint', '2026-10-01T00:00:00Z')])

    def test_a_changelog_by_a_person_or_an_unknown_name_is_not_listed(self) -> None:
        contents = [('T-1', changelog(1, 'Omid Hekayati')), ('T-1', changelog(2, 'ghost'))]
        self.assertEqual(self.listed(contents), [])

    def test_only_contents_of_kind_changelog_are_listed(self) -> None:
        self.assertEqual(self.listed([('T-1', Content(1, {'kind': 'report', 'author': 'Claude'}, 'x'))]), [])

    def test_an_approved_by_a_person_removes_it(self) -> None:
        contents = [('T-1', changelog(1, 'Claude')), ('T-1', approval(2, 'Omid Hekayati', '1'))]
        self.assertEqual(self.listed(contents), [])

    def test_an_approval_in_another_task_by_a_timeline_ref_removes_it(self) -> None:
        contents = [('T-1', changelog(1, 'Claude')), ('T-2', approval(1, 'Omid Hekayati', 'T-1:1'))]
        self.assertEqual(self.listed(contents), [])

    def test_an_approval_by_a_model_does_not_remove_it(self) -> None:
        contents = [('T-1', changelog(1, 'Claude')), ('T-1', approval(2, 'Super Z', '1'))]
        self.assertEqual(self.listed(contents), [('T-1', 1)])

    def test_a_withheld_verdict_does_not_remove_it(self) -> None:
        contents = [('T-1', changelog(1, 'Claude')), ('T-1', approval(2, 'Omid Hekayati', '1', 'withheld'))]
        self.assertEqual(self.listed(contents), [('T-1', 1)])

    def test_an_approval_of_another_content_does_not_remove_it(self) -> None:
        contents = [('T-1', changelog(1, 'Claude')), ('T-1', changelog(2, 'Claude')), ('T-1', approval(3, 'Omid Hekayati', '2'))]
        self.assertEqual(self.listed(contents), [('T-1', 1)])

    def test_a_title_falls_back_to_the_first_line(self) -> None:
        content = Content(1, {'kind': 'changelog', 'author': 'Claude'}, 'Plain first line\nmore\n')
        self.assertEqual(record.ai_only_changelogs([('T-1', content)], self.sections)[0][2], 'Plain first line')


class TheVerb(Scratch):

    def setUp(self) -> None:
        super().setUp()
        elsewhere = self.root / 'memar-tasks'
        elsewhere.mkdir()
        patched = unittest.mock.patch.object(task_records, 'tasks_root', return_value=elsewhere)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, task_id: str, number: int, text: str) -> None:
        folder = self.root / '.agents' / 'tasks' / task_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'task.yaml').write_text('title: t\n', encoding='utf-8', newline='\n')
        (folder / f'content.{number:05d}.md').write_text(text, encoding='utf-8', newline='\n')

    def run_verb(self, after=None) -> str:
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            listing.list_ai_only(Namespace(after=after), self.root)
        return printed.getvalue()

    def test_the_verb_prints_task_hash_number_title(self) -> None:
        self.task('T-1', 1, '---\nkind: changelog\nauthor: Claude\nplaced_at: 2026-10-01T00:00:00Z\n---\n### Fixed the lint\n')
        self.task('T-1', 2, '---\nkind: approval\nauthor: Omid Hekayati\nrefs: 1\n---\n- Verdict: approved\n')
        self.task('T-2', 1, '---\nkind: changelog\nauthor: Super Z\nplaced_at: 2026-10-02T00:00:00Z\n---\n### Moved the rule\n')
        self.assertEqual(self.run_verb().splitlines(), ['T-2#1: Moved the rule'])

    def test_after_keeps_only_what_was_placed_later(self) -> None:
        self.task('T-1', 1, '---\nkind: changelog\nauthor: Claude\nplaced_at: 2026-10-01T00:00:00Z\n---\n### Early\n')
        self.task('T-1', 2, '---\nkind: changelog\nauthor: Claude\nplaced_at: 2026-10-03T00:00:00Z\n---\n### Late\n')
        self.assertEqual(self.run_verb(after='2026-10-02T00:00:00Z').splitlines(), ['T-1#2: Late'])

    def test_none_listed_prints_the_marker(self) -> None:
        self.assertEqual(self.run_verb().strip(), '(no changelog record has only AI authors)')

    def test_the_ledger_reading_and_the_approval_writer_are_gone(self) -> None:
        self.assertFalse(hasattr(record, 'changelog_records'))
        self.assertFalse(hasattr(record, 'ai_only_records'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
