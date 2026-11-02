#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
BUNDLE = TESTS.parent
TOP = BUNDLE.parent.parent
ROUTER = TOP / 'bundles' / 'memar' / 'memar'
for _folder in (TOP, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
suite_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch').suite_scratch
PROCESS_SECONDS = 60
_TEMPLATES: dict = {}

def bundle(dotted: str):
    return import_module(f'bundles.memar_git.{dotted}')

def errors():
    return bundle('errors.errors')

def git_in(folder: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(folder), *args], capture_output=True, text=True, check=True, timeout=PROCESS_SECONDS).stdout.strip()

def templates() -> dict:
    if not _TEMPLATES:
        import atexit
        holder = tempfile.TemporaryDirectory(dir=suite_scratch(), prefix='tmp-git-template-', ignore_cleanup_errors=True)
        atexit.register(holder.cleanup)
        repo = Path(holder.name) / 'repo'
        elsewhere = Path(holder.name) / 'elsewhere'
        repo.mkdir()
        elsewhere.mkdir()
        git_in(repo, 'init', '-q', '-b', 'main')
        git_in(repo, 'config', 'user.name', 'Test')
        git_in(repo, 'config', 'user.email', 'test@example.org')
        git_in(repo, 'config', 'core.autocrlf', 'false')
        for name in ('mine.md', 'theirs.md', 'shared.md'):
            (repo / name).write_text('base\n', encoding='utf-8', newline='\n')
        git_in(repo, 'add', '.')
        git_in(repo, 'commit', '-q', '-m', 'base')
        git_in(elsewhere, 'init', '-q', '-b', 'main')
        git_in(elsewhere, 'config', 'user.name', 'Other')
        git_in(elsewhere, 'config', 'user.email', 'other@example.org')
        (elsewhere / 'other.md').write_text('other\n', encoding='utf-8', newline='\n')
        git_in(elsewhere, 'add', '.')
        git_in(elsewhere, 'commit', '-q', '-m', 'other')
        _TEMPLATES.update(repo=repo, elsewhere=elsewhere, base=git_in(repo, 'rev-parse', 'HEAD'), elsewhere_tip=git_in(elsewhere, 'rev-parse', 'HEAD'))
    return _TEMPLATES

class ScratchRepository(unittest.TestCase):
    TIER = 'system'

    def setUp(self) -> None:
        template = templates()
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch(), prefix='tmp-git-repo-', ignore_cleanup_errors=True)
        self.addCleanup(scratch.cleanup)
        self.repo = Path(scratch.name)
        shutil.copytree(template['repo'], self.repo, dirs_exist_ok=True)
        self.base = template['base']
        self.message = self.repo / '.git' / 'message.txt'
        self.message.write_text('subject\n', encoding='utf-8', newline='\n')
        elsewhere = tempfile.TemporaryDirectory(dir=suite_scratch(), prefix='tmp-git-elsewhere-', ignore_cleanup_errors=True)
        self.addCleanup(elsewhere.cleanup)
        self.elsewhere = Path(elsewhere.name)
        shutil.copytree(template['elsewhere'], self.elsewhere, dirs_exist_ok=True)
        self.elsewhere_tip = template['elsewhere_tip']
        self.addCleanup(self.assert_elsewhere_untouched)

    def git(self, *args: str) -> str:
        return git_in(self.repo, *args)

    def assert_elsewhere_untouched(self) -> None:
        self.assertEqual(git_in(self.elsewhere, 'rev-parse', 'HEAD'), self.elsewhere_tip)
        self.assertEqual(git_in(self.elsewhere, 'status', '--porcelain'), '')

    def put(self, name: str, text: str) -> None:
        (self.repo / name).write_text(text, encoding='utf-8', newline='\n')

    def router(self, *args: str, folder: Path | None = None) -> subprocess.CompletedProcess:
        env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, str(ROUTER), *args], cwd=folder or self.elsewhere, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, timeout=PROCESS_SECONDS)

    def verb(self, verb: str, *args: str, repository: bool = True) -> subprocess.CompletedProcess:
        flag = ['--repository', str(self.repo)] if repository else []
        return self.router('git', verb, *flag, *args)

    def commit(self, *args: str) -> subprocess.CompletedProcess:
        return self.verb('commit', '-F', str(self.message), '--no-task', *args)

    def a_file_long_enough_to_keep_a_rename(self) -> str:
        body = ''.join((f'line {number}\n' for number in range(20)))
        self.put('mine.md', body)
        self.git('commit', '-q', '-am', 'body')
        self.base = self.git('rev-parse', 'HEAD')
        return body
