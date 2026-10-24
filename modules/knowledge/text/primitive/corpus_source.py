#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/text/primitive/corpus_source.py — where the content a verb reads is read from, declared once.

`memar content find` and `memar content search` read a corpus, and the agent says which
sources it is made of with `--from`, once per source; without it, the documents and the code,
as before the flag existed. The tasks are a source of their own because what a task
wrote is that task's claim, never a ruling: a reader asks for them by name and a hit from
them names the task it came from (owner, 2026-10-19: a filter on `memar content`, not a new
verb). The flag, its values, what each reads and the default are the type's, and every help
text that names them asks it
([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_git_records = plugable_load('computer.git.services._git_records')
reference = _m_git_records.reference
import argparse
from enum import Enum
FLAG = '--from'
METAVAR = 'SOURCE'
DEST = 'sources'

class CorpusSource(Enum):
    """One source of the corpus a content verb reads."""
    DOCUMENTS = 'documents'
    CODE = 'code'
    TASKS = 'tasks'

    @property
    def suffixes(self) -> tuple[str, ...]:
        """The file suffixes this source takes from the checkout's folders; none for the tasks, which take every text file."""
        return {'documents': ('.md',), 'code': ('.kh',)}.get(self.value, ())

    @property
    def reads(self) -> str:
        """What this source reads, as a help text says it."""
        return {'documents': "the Markdown files of the checkout's docs/, modules/, modules-plugable/, bundles/ and .agents/, and its README.md and AGENTS.md; not handoffs, changelogs, research companions, temp/ or generated folders", 'code': 'the .kh files of the same folders', 'tasks': f"every task's records, each a task's claim and never a ruling: the archived ones on the project's records branch, cited as {reference('<id>')}, unless its preferences say `records: off`, and the live task folders of the project, each text file but a task's own temp/; a task with a live folder is read from it"}[self.value]

    @classmethod
    def default(cls) -> tuple[CorpusSource, ...]:
        """The sources read when none is named: the documents and the code."""
        return (cls.DOCUMENTS, cls.CODE)

    @classmethod
    def add_flag(cls, parser: argparse.ArgumentParser) -> None:
        """Give PARSER the `--from` flag, repeatable, its help listing each value and what it reads."""
        listed = '; '.join((f'`{each.value}`: {each.reads}' for each in cls))
        named = ' and '.join((f'`{each.value}`' for each in cls.default()))
        parser.add_argument(FLAG, dest=DEST, action='append', choices=[each.value for each in cls], metavar=METAVAR, help=f'a source to read, repeated for several; without it, {named}. {listed}')

    @classmethod
    def chosen(cls, args: argparse.Namespace) -> tuple[CorpusSource, ...]:
        """The sources the parsed flag names, each once in the type's order; the default when none."""
        named = getattr(args, DEST, None)
        if not named:
            return cls.default()
        return tuple((each for each in cls if each.value in named))
