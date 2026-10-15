#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/project_find.py — a word turned into a project folder, so no agent reasons about a name.

Why a service. An agent told "the organization project" would otherwise guess a
folder, read the calling folder, or write a script to hunt for it; each is
slower and less certain than asking the registry (`project_registry`). The
lookup answers in this order, and stops at the first that answers:

1. The word is a name or alias of a project, in any case and Unicode
   composition: that one project.
2. The word is near a name or alias of exactly one project: that one. Near is
   deliberately generous, because its only job is that the name need not be
   exact and the agent need not reason to find it: the word is a prefix of the
   name (two characters or more), or its text is at least `SIMILARITY` alike
   (the ratio of matching characters of both, `difflib`), or, for a name of
   three characters or more, one edit away (a letter added, dropped, changed,
   or two swapped), which is how a short name like org is mistyped. The whole
   name or alias is compared, on text normalised as the registry compares it.
3. The word is near the names of several projects: all are returned, in the
   order registered, as candidates, and none is picked. Choosing between
   projects is the caller's, and a wrong guess acts on the wrong project.
4. Nothing is near: a bounded local search for a repository (a folder holding
   .git, a file in a worktree) of exactly that name, among the children of
   the Memar checkout's parent and of each registered project and its parent.
   It runs for `SEARCH_SECONDS` at most, lists only direct children, and
   records what it finds in the registry under the folder's name, so the next
   ask is an exact one. Seconds, never minutes: an agent waiting on a search
   would sooner write its own.
5. Otherwise none, which the verb and `resolve_project` report as an error.

`resolve_project` is the function other verbs call: it returns one folder or
stops with the candidates or the absence stated. Memar's own checkout is
always an entry (`project_registry.ensure_memar_entry`), so asking for memar
needs no registration.
"""
from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable

from machine.console import fail
import machine.fs_memar as memar_fs
from services.project_registry import (
    Entry,
    add_project,
    ensure_memar_entry,
    normalized,
    path_key,
    read_entries,
)

FIND_COMMAND = "find"
# The ratio of matching characters at or above which two names are taken for one mistyped.
SIMILARITY = 0.8
# A prefix shorter than this is not a name started, only a letter.
MIN_PREFIX = 2
# A name this short or shorter is not compared by edit distance: one edit would be most of it.
MIN_EDITED = 3
# The local search stops after this long, because an agent waiting longer would write its own.
SEARCH_SECONDS = 3.0

EXACT = "exact"
NEAR = "near"
FOUND = "found"
CANDIDATES = "candidates"
NONE = "none"


@dataclass(frozen=True)
class Lookup:
    """What a lookup answered: its kind, and the projects (one, several for candidates, none for none)."""

    kind: str
    entries: list[Entry]


def _one_edit(one: str, two: str) -> bool:
    """Whether ONE becomes TWO by one letter added, dropped, or changed, or two neighbours swapped."""
    if one == two:
        return True
    if abs(len(one) - len(two)) > 1:
        return False
    if len(one) == len(two):
        differing = [index for index in range(len(one)) if one[index] != two[index]]
        if len(differing) == 1:
            return True
        return len(differing) == 2 and differing[1] == differing[0] + 1 and one[differing[0]] == two[differing[1]] and one[differing[1]] == two[differing[0]]
    shorter, longer = sorted((one, two), key=len)
    return any(longer[:index] + longer[index + 1:] == shorter for index in range(len(longer)))


def is_near(word: str, name: str) -> bool:
    """Whether WORD may be NAME written inexactly: a prefix of it, alike in text, or one edit away."""
    asked, known = normalized(word), normalized(name)
    if not asked or not known:
        return False
    if len(asked) >= MIN_PREFIX and known.startswith(asked):
        return True
    if SequenceMatcher(None, asked, known).ratio() >= SIMILARITY:
        return True
    return min(len(asked), len(known)) >= MIN_EDITED and _one_edit(asked, known)


def _is_repository(folder: Path) -> bool:
    return (folder / ".git").exists()


def _search_folders() -> list[Path]:
    """Where the local search looks: beside the Memar checkout, and in and beside each registered project."""
    folders: list[Path] = [memar_fs.memar_root().resolve().parent]
    for entry in read_entries():
        project = Path(entry.path)
        folders += [project.parent, project]
    unique: dict[str, Path] = {}
    for folder in folders:
        unique.setdefault(path_key(folder), folder)
    return list(unique.values())


def search_locally(word: str, budget: float = SEARCH_SECONDS) -> Entry | None:
    """A repository named WORD (any case) among the direct children of `_search_folders`, recorded and returned.

    Stops when BUDGET seconds are used up. A folder with that name that is no
    repository is not a project. A name the registry refuses (another
    project's) records nothing and finds nothing.
    """
    deadline = time.monotonic() + budget
    key = normalized(word)
    if not key:
        return None
    for folder in _search_folders():
        try:
            children = os.scandir(folder)
        except OSError:
            continue
        with children:
            for child in children:
                if time.monotonic() >= deadline:
                    return None
                if normalized(child.name) != key:
                    continue
                try:
                    if not child.is_dir() or not _is_repository(Path(child.path)):
                        continue
                except OSError:
                    continue
                try:
                    return add_project(child.name, child.path)
                except (SystemExit, OSError):
                    return None
    return None


def lookup(word: str, *, budget: float = SEARCH_SECONDS) -> Lookup:
    """The answer to WORD, by the order the module header gives; see it for each kind."""
    ensure_memar_entry()
    entries = read_entries()
    key = normalized(word)
    exact = [entry for entry in entries if any(normalized(name) == key for name in entry.names)]
    if exact:
        return Lookup(EXACT, exact[:1])
    near = [entry for entry in entries if any(is_near(word, name) for name in entry.names)]
    if len(near) == 1:
        return Lookup(NEAR, near)
    if near:
        return Lookup(CANDIDATES, near)
    found = search_locally(word, budget)
    return Lookup(FOUND, [found]) if found is not None else Lookup(NONE, [])


def _described(entries: list[Entry]) -> str:
    return "\n".join(f"  {', '.join(entry.names)}  {entry.path}" for entry in entries)


def refusal(word: str, found: Lookup) -> str:
    """The words an unanswered lookup stops with: the candidates, or what was tried and what to do."""
    if found.kind == CANDIDATES:
        return (
            f"{word} is near several projects and none is picked; ask again with the exact name or alias of one:\n"
            f"{_described(found.entries)}"
        )
    return (
        f"no project is named or near {word}. It is not in the registry (`memar project list`), and no repository "
        f"of that name is beside the Memar checkout or the registered projects. Register it with "
        f"`memar project add NAME PATH`, or ask the owner for the name."
    )


def resolve_project(word: str) -> Path:
    """The folder of the one project WORD names, for the verbs that are given a project by name.

    Stops with the candidates stated when several are near, and with what was
    tried when none is: a verb must not act on a guess.
    """
    found = lookup(word)
    if found.kind in (EXACT, NEAR, FOUND):
        return Path(found.entries[0].path)
    fail(refusal(word, found))


NAME_FLAG = "--project"
PATH_FLAG = "--project-path"


def _looks_like_a_path(text: str) -> bool:
    """Whether TEXT is written as a path: absolute, with a drive or a separator, or starting with . or ~."""
    return (
        Path(text).is_absolute()
        or bool(Path(text).drive)
        or "/" in text
        or "\\" in text
        or text[0] in ".~"
    )


def project_by_name(value: str) -> Path:
    """The folder of the project VALUE names in the registry; a value written as a path is an error.

    The caller said it is a name (`--project`), so a value that looks like a
    path is not looked up and not taken as a folder: it is refused with the
    flag that takes a path. Nothing here reads the folder the process is in.
    """
    if not value or not value.strip():
        fail(f"{NAME_FLAG} needs the name of a project, one `memar project list` shows")
    text = value.strip()
    if _looks_like_a_path(text):
        fail(f"{NAME_FLAG} takes a project's name, and {value} looks like a path; for a folder use {PATH_FLAG} PATH")
    return resolve_project(text)


def project_by_path(value: str | Path) -> Path:
    """The folder VALUE is, as given; anything that is not an existing folder is an error.

    The caller said it is a path (`--project-path`), so no registry is asked: a
    word that is not a folder is refused, with the flag that takes a name.
    """
    text = str(value).strip()
    if not text:
        fail(f"{PATH_FLAG} needs the folder of a project")
    folder = Path(text).expanduser().resolve()
    if not folder.is_dir():
        hint = "" if _looks_like_a_path(text) else f"; for a registered project's name use {NAME_FLAG} NAME"
        fail(f"{value} is not a folder{hint}")
    return folder


def add_project_flags(parser: argparse.ArgumentParser, what: str, *, required: bool = False) -> None:
    """Give PARSER the two flags that name a project, at most one of them: `--project NAME` and `--project-path PATH`.

    WHAT says, in the help, which project the verb means. REQUIRED only changes
    the help: a verb refuses a missing project itself, in its own words.
    """
    group = parser.add_mutually_exclusive_group()
    need = "required, one of the two: " if required else "one of the two: "
    group.add_argument(
        NAME_FLAG,
        metavar="NAME",
        default=None,
        help=f"{need}{what}, by the name or alias `memar project find` resolves; a folder is not accepted here, use {PATH_FLAG}",
    )
    group.add_argument(
        PATH_FLAG,
        metavar="PATH",
        default=None,
        help=f"{need}{what}, by its folder, taken as given (its git top-level is the project); a name is not accepted here, use {NAME_FLAG}",
    )


def project_from_args(args: argparse.Namespace) -> Path | None:
    """The folder the parsed `--project` or `--project-path` names, None when neither was given."""
    name = getattr(args, "project", None)
    path = getattr(args, "project_path", None)
    if name is not None:
        return project_by_name(name)
    if path is not None:
        return project_by_path(path)
    return None


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar project find`."""
    finder = verbs.add_parser(
        FIND_COMMAND,
        help="print the folder of the project a name, alias, or near-miss of one names",
        description=(
            "Print the folder of the project WORD names, and nothing else. WORD is a name\n"
            "or alias in any case and any language, or near one: a prefix, or a typo.\n"
            "One near project is one answer. Several are listed as candidates on stderr\n"
            "with a non-zero status, and none is picked. When nothing is near, a search\n"
            "of a few seconds for a repository of that name beside the Memar checkout\n"
            "and the registered projects runs first, and what it finds is registered.\n"
            "Only then is it an error. Ask `find` for a name; do not write a script to\n"
            "search for one, and do not guess a path."
        ),
    )
    finder.add_argument("word", metavar="WORD", help="the project's name or alias, or near it")
    return run


def run(args: argparse.Namespace) -> None:
    print(resolve_project(args.word))
