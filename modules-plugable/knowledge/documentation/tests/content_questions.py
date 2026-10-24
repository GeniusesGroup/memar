#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content questions` in `modules-plugable/knowledge/documentation/services/content_questions.py`.

    python modules-plugable/knowledge/documentation/tests/content_questions.py

The subject is the open-question list as a query, named for the file that holds
it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Scratch handoffs are written into a folder made under the one
`modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed again. The real
`bundles/khayyam/khayyam.handoff.md` is read, never written, as a fixture.

What is pinned, and what each pin is for:

  QuestionsAreListed      Entries under `## Open Questions` print as
                          `path:line: heading`, and nothing else does.
  QuestionsAreScoped      A file, a folder, and a project each bound the read;
                          none given reads the checkout.
  BlockingComesFirst      Blocking entries print first and are marked, then by
                          Asked date; `--blocking` keeps only them.
  KhayyamHandoffIsRead    The repository's own handoff, whose entries use the
                          older `Blocks continuation` field, is listed whole.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
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
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_questions = import_module('modules-plugable.knowledge.documentation.services.content_questions')
REPO = SCRIPTS.parent.parent
HANDOFF = '# Thing handoff\n\n## Open Questions\nPreamble line.\n\n### Old and blocking?\n- State: x\n- Blocks: the lint. Assumption meanwhile: none.\n- Asked: 2026-10-01, Claude, for Omid.\n\n### Newer and blocking?\n- State: x\n- Blocks: the verb.\n- Asked: 2026-10-12, Claude, for Omid.\n\n### Does not block?\n- State: x\n- Blocks: no.\n- Asked: 2026-09-01, Claude, for Omid.\n\n#### Deeper heading is not an entry\ntext\n\n## Anticipated Work\n\n### Not a question\n- Next: none.\n'

def namespace(**kw) -> Namespace:
    base = dict(scope=None, project=None, blocking=False)
    base.update(kw)
    return Namespace(**base)

class Scratch(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def run_verb(self, args: Namespace, root: Path | None=None) -> str:
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_questions.cmd_questions(args, root or self.root)
        return printed.getvalue()

class QuestionsAreListed(Scratch):

    def test_entries_print_as_path_line_heading(self) -> None:
        self.write('docs/a.handoff.md', HANDOFF)
        out = self.run_verb(namespace())
        self.assertIn(f"{Path('docs/a.handoff.md')}:6: Old and blocking?", out)
        self.assertIn('Does not block?', out)

    def test_other_sections_and_deeper_headings_are_not_entries(self) -> None:
        self.write('docs/a.handoff.md', HANDOFF)
        out = self.run_verb(namespace())
        self.assertNotIn('Not a question', out)
        self.assertNotIn('Deeper heading', out)

    def test_fenced_headings_are_not_entries(self) -> None:
        self.write('a.handoff.md', '## Open Questions\n```\n### Fake?\n```\n### Real?\n- Blocks: no.\n')
        out = self.run_verb(namespace())
        self.assertIn('Real?', out)
        self.assertNotIn('Fake?', out)

    def test_empty_prints_the_marker(self) -> None:
        self.write('a.handoff.md', '# T\n\n## Anticipated Work\n### X\n')
        self.assertIn('(no open questions)', self.run_verb(namespace()))

    def test_only_handoff_files_are_read(self) -> None:
        self.write('a.md', HANDOFF)
        self.assertIn('(no open questions)', self.run_verb(namespace()))

class QuestionsAreScoped(Scratch):

    def setUp(self) -> None:
        super().setUp()
        self.write('docs/a.handoff.md', HANDOFF.replace('Old and', 'Alpha and'))
        self.write('bundles/b.handoff.md', HANDOFF.replace('Old and', 'Beta and'))

    def test_a_file_scope_reads_that_file(self) -> None:
        out = self.run_verb(namespace(scope='docs/a.handoff.md'))
        self.assertIn('Alpha', out)
        self.assertNotIn('Beta', out)

    def test_a_folder_scope_reads_recursively(self) -> None:
        out = self.run_verb(namespace(scope='bundles'))
        self.assertIn('Beta', out)
        self.assertNotIn('Alpha', out)

    def test_no_scope_reads_the_checkout(self) -> None:
        out = self.run_verb(namespace())
        self.assertIn('Alpha', out)
        self.assertIn('Beta', out)

    def test_a_project_reads_that_projects_folder(self) -> None:
        project = self.root / 'other'
        (project / 'x').mkdir(parents=True)
        (project / 'x' / 'p.handoff.md').write_text(HANDOFF.replace('Old and', 'Gamma and'), encoding='utf-8', newline='\n')
        out = self.run_verb(namespace(project_path=str(project)))
        self.assertIn('Gamma', out)
        self.assertNotIn('Alpha', out)

    def test_a_project_given_by_name_is_looked_up_and_a_path_in_its_place_is_refused(self) -> None:
        project = self.root / 'other'
        project.mkdir()
        (project / 'p.handoff.md').write_text(HANDOFF.replace('Old and', 'Gamma and'), encoding='utf-8', newline='\n')
        with unittest.mock.patch('modules.process.project.services.find.resolve_project', return_value=project) as found:
            out = self.run_verb(namespace(project='other'))
        found.assert_called_once_with('other')
        self.assertIn('Gamma', out)
        with self.assertRaises(SystemExit) as refused:
            self.run_verb(namespace(project=str(project)))
        self.assertIn('--project-path', str(refused.exception.code))

    def test_a_scope_with_a_project_is_inside_that_project(self) -> None:
        project = self.root / 'other'
        (project / 'x').mkdir(parents=True)
        (project / 'x' / 'p.handoff.md').write_text(HANDOFF.replace('Old and', 'Gamma and'), encoding='utf-8', newline='\n')
        (project / 'y.handoff.md').write_text(HANDOFF.replace('Old and', 'Delta and'), encoding='utf-8', newline='\n')
        out = self.run_verb(namespace(project_path=str(project), scope='x'))
        self.assertIn('Gamma', out)
        self.assertNotIn('Delta', out)

    def test_a_missing_scope_stops(self) -> None:
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                self.run_verb(namespace(scope='nowhere'))

class BlockingComesFirst(Scratch):

    def setUp(self) -> None:
        super().setUp()
        self.write('docs/a.handoff.md', HANDOFF)

    def test_blocking_entries_come_first_oldest_first_and_are_marked(self) -> None:
        lines = self.run_verb(namespace()).splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].endswith('Old and blocking? [blocks]'), lines[0])
        self.assertTrue(lines[1].endswith('Newer and blocking? [blocks]'), lines[1])
        self.assertTrue(lines[2].endswith('Does not block?'), lines[2])

    def test_the_blocking_filter_drops_the_rest(self) -> None:
        out = self.run_verb(namespace(blocking=True))
        self.assertNotIn('Does not block?', out)
        self.assertEqual(len(out.splitlines()), 2)

    def test_the_older_field_name_and_mixed_answers_block(self) -> None:
        self.write('docs/b.handoff.md', '## Open Questions\n### Mixed?\n- Blocks continuation: no for M1; yes for M2.\n### Plain no?\n- Blocks continuation: no; it gates later.\n')
        out = self.run_verb(namespace(scope='docs/b.handoff.md'))
        self.assertIn('Mixed? [blocks]', out)
        self.assertNotIn('Plain no? [blocks]', out)

class KhayyamHandoffIsRead(unittest.TestCase):

    def test_every_entry_of_the_khayyam_handoff_is_listed(self) -> None:
        path = REPO / 'bundles' / 'khayyam' / 'khayyam.handoff.md'
        text = path.read_text(encoding='utf-8')
        inside = text.split('\n## Open Questions', 1)[1].split('\n## ', 1)[0]
        expected = [l for l in inside.splitlines() if l.startswith('### ')]
        self.assertGreater(len(expected), 5)
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            content_questions.cmd_questions(namespace(scope='bundles/khayyam/khayyam.handoff.md'), REPO)
        out = printed.getvalue()
        self.assertEqual(len(out.splitlines()), len(expected))
        self.assertIn("Two analysers: `analyze()` and the server's own binding table", out)
        self.assertIn('[blocks]', out)
if __name__ == '__main__':
    unittest.main(verbosity=2)
