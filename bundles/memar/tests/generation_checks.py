#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations

from importlib import import_module

_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import ast
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
TOP = SCRIPTS.parent.parent
sys.dont_write_bytecode = True
BUDGET_SECONDS = 60
SOURCES = ('modules', 'modules-plugable', 'bundles')
SKIPPED_FOLDERS = ('__pycache__', 'node_modules', 'tests')
GENERATION_TOKEN = re.compile(r'(_new|_old|_legacy|_v\d+)$|^(v\d+)$|(_new|_old|_legacy|_v\d+)_', re.IGNORECASE)
STAMP_NAMES = ('writer_of', 'WRITER_FACT', 'FIRST_GENERATION_TYPE_UUID', 'count_written_by')
READERS_OF_THE_STAMP = (
    'modules-plugable/management/task/services/task_generation.py',
    'modules-plugable/management/task/services/task_memory.py',
    'modules-plugable/management/task/services/task_predecessor_adapter.py',
    'modules-plugable/management/task/services/task_conversion.py',
)
OWED_NAMES = (
    ('modules-plugable/ai/services/get_new_chats_ask.py', 'get_new_chats_ask'),
    ('modules-plugable/ai/services/get_new_chats_ask.py', 'get_new_chats_ask.py'),
    ('modules-plugable/management/task/services/new.py', '_m_new_chats'),
)


def sources(top: Path):
    for source in SOURCES:
        for folder, folders, names in os.walk(top / source):
            folders[:] = [name for name in folders if name not in SKIPPED_FOLDERS]
            for name in names:
                if name.endswith('.py'):
                    yield Path(folder) / name


def relative(top: Path, path: Path) -> str:
    return path.relative_to(top).as_posix()


def parsed(path: Path):
    try:
        return ast.parse(path.read_text(encoding='utf-8'))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return None


def generation_names(top: Path) -> list[tuple[str, str]]:
    found = []
    for path in sources(top):
        tree = parsed(path)
        if tree is None:
            continue
        where = relative(top, path)
        if GENERATION_TOKEN.search(path.stem):
            found.append((where, path.name))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and GENERATION_TOKEN.search(node.name):
                found.append((where, node.name))
            if isinstance(node, ast.Assign):
                found.extend((where, target.id) for target in node.targets if isinstance(target, ast.Name) and GENERATION_TOKEN.search(target.id))
    return sorted(set(found))


def stamp_readers(top: Path) -> list[str]:
    found = []
    for path in sources(top):
        where = relative(top, path)
        if where in READERS_OF_THE_STAMP:
            continue
        tree = parsed(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            used = node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else None
            if used in STAMP_NAMES:
                found.append(where)
                break
    return sorted(found)


def scratch_tree(files: dict[str, str]) -> tempfile.TemporaryDirectory:
    scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
    for name, text in files.items():
        path = Path(scratch.name) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
    return scratch


class NoGenerationInAName(unittest.TestCase):

    def test_no_declaration_outside_the_owed_ones_carries_a_generation_token(self) -> None:
        self.assertEqual([item for item in generation_names(TOP) if item not in OWED_NAMES], [])

    def test_every_owed_name_is_still_in_the_tree(self) -> None:
        present = generation_names(TOP)
        self.assertEqual([item for item in OWED_NAMES if item not in present], [])

    def test_a_token_written_into_a_scratch_tree_is_found(self) -> None:
        with scratch_tree({'modules/x/services/x.py': 'def read_v2(a):\n    return a\n\nclass Store_old:\n    pass\n\nLIMIT_new = 1\n\ndef read(a):\n    return a\n'}) as root:
            found = generation_names(Path(root))
        self.assertEqual([name for _, name in found], ['LIMIT_new', 'Store_old', 'read_v2'])

    def test_a_standard_word_inside_a_name_is_not_a_token(self) -> None:
        with scratch_tree({'modules/x/services/x.py': 'def renewal(a):\n    return a\n\ndef bold(a):\n    return a\n'}) as root:
            self.assertEqual(generation_names(Path(root)), [])


class NoCoreReadsAStamp(unittest.TestCase):

    def test_only_the_readers_of_the_stamp_name_it(self) -> None:
        self.assertEqual(stamp_readers(TOP), [])

    def test_every_reader_of_the_stamp_is_a_file_that_stands(self) -> None:
        self.assertEqual([name for name in READERS_OF_THE_STAMP if not (TOP / name).is_file()], [])

    def test_a_core_reading_the_stamp_written_into_a_scratch_tree_is_found(self) -> None:
        with scratch_tree({'modules/x/services/core.py': 'def run(folder, generation):\n    return generation.writer_of(folder)\n', 'modules/x/services/clean.py': 'def run(a):\n    return a\n'}) as root:
            self.assertEqual(stamp_readers(Path(root)), ['modules/x/services/core.py'])


if __name__ == '__main__':
    unittest.main()
