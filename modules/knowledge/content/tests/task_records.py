#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the source `tasks` of `memar content find` and `memar content search`, in `modules/knowledge/content/services/task_records.py`, `modules/knowledge/content/primitive/corpus_source.py` and `modules-plugable/computer/git/services/_git_records.py`.

    python modules/knowledge/content/tests/task_records.py

The subject is the owner's ruling of 2026-10-19, carried out by task 20261019-T170853Z-4740:
archived task records are reached by content through `memar content`, with a filter `--from`
by which the agent says where the content is read from, and no new verb. Named for the file that
holds it per [Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md), in
the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Pinned on a scratch project of the suite's own, a git repository with a records branch made in
it, so no pin depends on this checkout's records. What is pinned, and what each pin is for:

  Archived   A term found only in an archived record is found by `search` and by `find` with
             `--from tasks`, and its hit names the records branch, the task and the file
             (`dev-knowledge:.agents/tasks/<id>/<file>`); the branch is read without moving
             HEAD, index or working tree.
  Filter     The same term is not found without `--from`, nor with `--from documents`; with
             `--from tasks` alone no document is read.
  Live       A live task folder in the project's tasks folder is read, its own temp/ is
             not, and a task with a live folder is read from it and not from the branch.
  None       A project whose preferences say `records: off`, one whose repository has no records
             branch, and a folder that is not a repository's top are each said in a note, and
             nothing archived is read.
  Default    Without `--from` the corpus is the documents and the code, as before the flag.
  Help/MCP   Each verb's help states the flag and what each value reads; the MCP tool generated
             from each verb takes it as a list of those values, with no code of its own.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import argparse
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.knowledge.content.primitive.corpus_source import CorpusSource
from modules.knowledge.content.services import find as content_find
from modules.knowledge.content.services import search as content_search
from modules.knowledge.content.services.corpus import content_files
from modules.process.project.services.preferences import preferences_path, preferences_text
ARCHIVED = '20261001-T000000Z-1'
LIVE = '20261002-T000000Z-2'
TERM = 'quokka'

def git(folder: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(folder), *args], capture_output=True, text=True, check=True).stdout.strip()

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

class Project(unittest.TestCase):
    """A project with a document, a `.kh` file, and a records branch holding one task that alone mentions TERM."""

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve() / 'orchard'
        write(self.root / 'docs' / 'pears.md', '# Pears\n\n## Rows\n\nPears grow in rows.\n')
        write(self.root / 'docs' / 'model.kh', 'declaration of a pear tree\n')
        git(self.root, 'init', '-q', '-b', 'main')
        git(self.root, 'config', 'user.name', 'Test')
        git(self.root, 'config', 'user.email', 'test@example.org')
        git(self.root, 'add', 'docs')
        git(self.root, 'commit', '-q', '-m', 'base')
        git(self.root, 'checkout', '-q', '--orphan', RECORDS_BRANCH)
        git(self.root, 'rm', '-q', '-r', '--cached', 'docs')
        write(self.root / '.agents' / 'tasks' / ARCHIVED / 'plan.md', f'# Plan\n\n## Request\n\nCount the {TERM} burrows.\n')
        write(self.root / '.agents' / 'tasks' / ARCHIVED / 'temp' / 'note.txt', f'{TERM} in scratch\n')
        write(self.root / '.agents' / 'tasks' / ARCHIVED / 'docs' / 'notes.txt', f'one {TERM} seen\n')
        git(self.root, 'add', '-f', '.agents')
        git(self.root, 'commit', '-q', '-m', 'records')
        git(self.root, 'checkout', '-q', '-f', 'main')
        git(self.root, 'clean', '-q', '-f', '-d', '-x', '.agents')

    def search(self, *patterns: str, sources=None) -> tuple[list[str], str]:
        out, err = (io.StringIO(), io.StringIO())
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            content_search.cmd_search(argparse.Namespace(patterns=list(patterns)), self.root, sources)
        return (out.getvalue().splitlines(), err.getvalue())

    def find(self, text: str, sources=None) -> tuple[list[str], tuple[str, ...]]:
        lines, notes = content_find.find_output(self.root, text, 10, False, 'orchard', sources)
        return (lines[1:], notes)

class Archived(Project):

    def test_search_finds_a_term_only_an_archived_record_holds_and_names_the_task_and_file(self) -> None:
        lines, notes = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertIn(f'{RECORDS_BRANCH}:.agents/tasks/{ARCHIVED}/plan.md:5:Count the {TERM} burrows.', lines)
        self.assertIn(f'{RECORDS_BRANCH}:.agents/tasks/{ARCHIVED}/docs/notes.txt:1:one {TERM} seen', lines)
        self.assertEqual(notes, '')

    def test_a_tasks_own_temp_folder_is_not_read(self) -> None:
        lines, _ = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertFalse(any(('/temp/' in line for line in lines)), lines)

    def test_find_ranks_the_sections_of_an_archived_record_like_a_documents(self) -> None:
        hits, _ = self.find(f'{TERM} burrows', sources=(CorpusSource.TASKS,))
        self.assertTrue(hits, hits)
        self.assertTrue(hits[0].startswith(f'orchard:{RECORDS_BRANCH}:.agents/tasks/{ARCHIVED}/plan.md#request | Request | '), hits)

    def test_the_branch_is_read_without_moving_head_index_or_working_tree(self) -> None:
        before = (git(self.root, 'symbolic-ref', 'HEAD'), git(self.root, 'rev-parse', 'HEAD'), git(self.root, 'status', '--porcelain'))
        self.search(TERM, sources=(CorpusSource.TASKS,))
        after = (git(self.root, 'symbolic-ref', 'HEAD'), git(self.root, 'rev-parse', 'HEAD'), git(self.root, 'status', '--porcelain'))
        self.assertEqual(before, after)

class Filter(Project):

    def test_without_the_filter_the_term_is_not_found(self) -> None:
        self.assertEqual(self.search(TERM)[0], [])
        self.assertEqual(self.find(TERM)[0], [])

    def test_with_documents_alone_the_term_is_not_found(self) -> None:
        self.assertEqual(self.search(TERM, sources=(CorpusSource.DOCUMENTS,))[0], [])
        self.assertEqual(self.find(TERM, sources=(CorpusSource.DOCUMENTS,))[0], [])

    def test_with_tasks_alone_no_document_is_read(self) -> None:
        lines, _ = self.search('pear', sources=(CorpusSource.TASKS,))
        self.assertEqual(lines, [])

    def test_tasks_and_documents_together_read_both(self) -> None:
        lines, _ = self.search(f'pears|{TERM}', sources=(CorpusSource.DOCUMENTS, CorpusSource.TASKS))
        self.assertTrue(any((line.startswith(str(Path('docs/pears.md'))) for line in lines)), lines)
        self.assertTrue(any((line.startswith(RECORDS_BRANCH) for line in lines)), lines)

class Live(Project):

    def setUp(self) -> None:
        super().setUp()
        self.folder = self.root / '.agents' / 'tasks' / LIVE
        write(self.folder / 'plan.md', f'# Plan\n\n## Request\n\nFeed the {TERM}.\n')
        write(self.folder / 'temp' / 'scratch.txt', f'{TERM} scratch\n')

    def test_a_live_folder_is_read_and_its_own_temp_is_not(self) -> None:
        lines, _ = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertIn(f'.agents/tasks/{LIVE}/plan.md:5:Feed the {TERM}.', lines)
        self.assertFalse(any((f'{LIVE}/temp/' in line for line in lines)), lines)

    def test_a_task_with_a_live_folder_is_read_from_it_and_not_from_the_branch(self) -> None:
        write(self.root / '.agents' / 'tasks' / ARCHIVED / 'plan.md', '# Plan\n\n## Request\n\nCount the burrows again.\n')
        lines, _ = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertFalse(any((f'tasks/{ARCHIVED}/' in line for line in lines)), lines)

class Nothing(Project):

    def test_records_off_is_said_and_nothing_archived_is_read(self) -> None:
        write(preferences_path(self.root), preferences_text({'records': 'off'}))
        lines, notes = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertEqual(lines, [])
        self.assertIn('records: off', notes)
        self.assertTrue(any(('records: off' in note for note in self.find(TERM, sources=(CorpusSource.TASKS,))[1])))

    def test_a_repository_with_no_records_branch_is_said(self) -> None:
        git(self.root, 'branch', '-q', '-D', RECORDS_BRANCH)
        lines, notes = self.search(TERM, sources=(CorpusSource.TASKS,))
        self.assertEqual(lines, [])
        self.assertIn(f'no branch {RECORDS_BRANCH}', notes)

    def test_a_folder_inside_another_repository_is_not_taken_for_it(self) -> None:
        inner = self.root / 'docs'
        lines, notes = content_search_in(inner, TERM)
        self.assertEqual(lines, [])
        self.assertIn('not the top folder of a git repository', notes)

def content_search_in(root: Path, pattern: str) -> tuple[list[str], str]:
    out, err = (io.StringIO(), io.StringIO())
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        content_search.cmd_search(argparse.Namespace(patterns=[pattern]), root, (CorpusSource.TASKS,))
    return (out.getvalue().splitlines(), err.getvalue())

class Default(Project):

    def test_without_sources_the_corpus_is_the_documents_and_the_code(self) -> None:
        found = {path.relative_to(self.root).as_posix() for path in content_files(self.root)}
        self.assertEqual(found, {'docs/pears.md', 'docs/model.kh'})
        self.assertEqual(CorpusSource.default(), (CorpusSource.DOCUMENTS, CorpusSource.CODE))
        self.assertEqual(content_files(self.root), content_files(self.root, CorpusSource.default()))

    def test_each_source_takes_its_own_files(self) -> None:
        self.assertEqual([path.name for path in content_files(self.root, (CorpusSource.CODE,))], ['model.kh'])
        self.assertEqual([path.name for path in content_files(self.root, (CorpusSource.DOCUMENTS,))], ['pears.md'])
        self.assertEqual(content_files(self.root, (CorpusSource.TASKS,)), [])

    def test_no_note_is_printed_without_the_tasks(self) -> None:
        _, notes = self.search('pear')
        self.assertEqual(notes, '')

class HelpAndTools(unittest.TestCase):

    def parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog='memar')
        top = parser.add_subparsers()
        verbs = top.add_parser('content').add_subparsers()
        content_search.describe(verbs)
        content_find.describe(verbs)
        return parser

    def test_each_verbs_help_states_the_flag_and_what_each_value_reads(self) -> None:
        from unittest import mock
        parser = self.parser()
        for verb in ('search', 'find'):
            out = io.StringIO()
            with mock.patch.dict('os.environ', {'COLUMNS': '2000'}), contextlib.redirect_stdout(out), self.assertRaises(SystemExit):
                parser.parse_args(['content', verb, '--help'])
            shown = ' '.join(out.getvalue().split())
            self.assertIn('--from SOURCE', shown, verb)
            for source in CorpusSource:
                self.assertIn(f"`{source.value}`: {' '.join(source.reads.split())}", shown, verb)

    def test_the_mcp_tool_of_each_verb_takes_the_sources_as_a_list_of_the_values(self) -> None:
        from mcp.services._tools import argv, definition, tools
        made = {tool.name: tool for tool in tools(self.parser())}
        for name in ('content_search', 'content_find'):
            properties = definition(made[name])['inputSchema']['properties']
            key, = [key for key, schema in properties.items() if schema.get('description', '').startswith('--from')]
            self.assertEqual(properties[key]['type'], 'array')
            self.assertEqual(properties[key]['items']['enum'], [each.value for each in CorpusSource])
        typed, _ = argv(made['content_search'], {'patterns': [TERM], key: ['tasks', 'documents']})
        self.assertIn('--from=tasks', typed)
        self.assertIn('--from=documents', typed)
if __name__ == '__main__':
    unittest.main(verbosity=2)
