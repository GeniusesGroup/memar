#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/normative_references.py — the lists of what each act reads before it starts, read from their declared places.

The rule is [Normative References](../rules/normative_references/normative_references.md):
before an act starts, the agent reads every section the entries of the every-act
list and of its kinds' lists name. This file reads those lists and nothing else;
which kinds exist is `services/task_kind.py`'s, how the sections print is
`services/task_context.py`'s, and what `memar content check` reports of a list
is `services/normative_references_check.py`'s.

**Declared places.** A list is read only in a place declared to hold lists, so a
fixture or an example saved under a list's name binds nobody. Memar's place is
one folder, `MEMAR_PLACE`, under Memar's checkout: a constant and not a
preference, because Memar's lists bind every project and are found the same way
from every one. A project's places are the folders its preference `PREFERENCE`
names, read by `services/project_preferences.py`; the places are always given
to `lists`, never inferred from the folder a command runs in.

**An entry** is one line at column 0, outside a fenced block: a list item whose
text begins with a link, then ` — ` and its why, then the review mark last, a
code span `reviewed` and the hash `memar content section FILE '#anchor' --hash`
prints. An entry that begins `Not read here: ` before its link drops a passage
and carries its reason as its why and no mark. Any other line of a list is not
an entry: the shape is the declaration.

**Where an entry's link leads.** A relative link names a file of the place's own
repository. In a project's list a link may instead be a page of Memar's
published repository (`machine/fs_memar.py`'s `PUBLISHED_PAGES`): it names that
file of the Memar checkout the place was given, and is read and hashed from
there, so a project can name a passage Memar's lists omit, or drop one they name,
without knowing where Memar's checkout lies on a machine.
"""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import NamedTuple
from urllib.parse import unquote

from machine.fs_memar import PUBLISHED_PAGES
from services.content_markdown import EXTERNAL_LINK
from services.content_reference import read_text
from services.content_section import _fenceless, by_anchor, section_hash

# The rule's name, which its folder, its lists' names and a project's preference all carry.
RULE = "normative_references"
# Memar's one declared place, relative to Memar's checkout. It moves with the rule
# to the `rules/` folder of the scripts' `task` module when the scripts become modules.
MEMAR_PLACE = PurePosixPath(".agents/scripts/rules") / RULE
# A list's file name: the rule's name, a hyphen, and the word of its act.
LIST_NAME = f"{RULE}-{{word}}.md"
# The key of a project's preferences that names its declared places: the rule's
# name, so the key and the folder it usually names say the same.
PREFERENCE = RULE
# The word of the list every act reads, whatever its kind.
EVERY_ACT = "every_act"
# The name a section of Memar's checkout is recorded under, beside a project's own name.
MEMAR_REPOSITORY = "memar"
DROP_MARK = "Not read here: "
REVIEWED_MARK = "reviewed"
WHY_MARK = " — "

_PREFIX, _SUFFIX = LIST_NAME.split("{word}")
LIST_FILE = re.compile(rf"^{re.escape(_PREFIX)}(?P<word>.+){re.escape(_SUFFIX)}$")
ENTRY = re.compile(
    rf"^- (?P<drop>{re.escape(DROP_MARK)})?\[(?P<label>[^\]]+)\]\((?P<link>[^)\s]+)\)"
    rf"(?:{re.escape(WHY_MARK)}(?P<why>.*?))?(?:\s*`{REVIEWED_MARK} (?P<mark>[0-9a-f]+)`)?\s*$"
)


class Place(NamedTuple):
    """A folder declared to hold lists: the name its sections are recorded under, its repository's top folder, the folder,
    and the Memar checkout a link to a page of Memar's published repository is read from (None: such a link names no file)."""

    repository: str
    top: Path
    folder: Path
    memar: Path | None = None

    @property
    def is_memar(self) -> bool:
        """Whether this is Memar's own place, whose lists bind every project."""
        return self.repository == MEMAR_REPOSITORY and self.memar == self.top and self.folder == self.top / MEMAR_PLACE


def memar_place(checkout: Path) -> Place:
    """Memar's declared place in the checkout CHECKOUT."""
    return Place(MEMAR_REPOSITORY, checkout, checkout / MEMAR_PLACE, checkout)


class Entry(NamedTuple):
    """One entry of a list: where it is, its link as written and the file and anchor it names, its why, its mark, whether
    it drops, and the repository the file lies in: its top folder and the name its sections are recorded under."""

    place: Place
    list_path: Path
    line: int
    label: str
    link: str
    target: Path | None
    anchor: str
    why: str
    reviewed: str | None
    drops: bool
    top: Path
    repository: str

    @property
    def where(self) -> str:
        """The entry's list and line, the list's path from its repository's top folder."""
        return f"{_posix(self.list_path, self.place.top)}:{self.line}"

    @property
    def located(self) -> str:
        """`where`, a project's under the project's name, so that a reader of a context tells it from Memar's."""
        return self.where if self.place.is_memar else f"{self.place.repository}: {self.where}"

    @property
    def path(self) -> str | None:
        """The target's path from its repository's top folder, with forward slashes; None when the link names no file inside it."""
        if self.target is None:
            return None
        try:
            return self.target.relative_to(self.top.resolve()).as_posix()
        except ValueError:
            return None

    @property
    def published(self) -> bool:
        """Whether the link is a page of Memar's published repository."""
        return self.link.startswith(PUBLISHED_PAGES)

    @property
    def root_relative(self) -> bool:
        return self.link.startswith("/")

    @property
    def written(self) -> str:
        """The entry's link and why as the list writes them, for a reader who must find the section it meant."""
        return f"[{self.label}]({self.link})" + (f"{WHY_MARK}{self.why}" if self.why else "")


class ReferenceList(NamedTuple):
    """One list: its place, its file, the word of its act (`EVERY_ACT` or a kind's), and its entries in order."""

    place: Place
    path: Path
    word: str
    entries: tuple[Entry, ...]


def _posix(path: Path, top: Path) -> str:
    try:
        return path.resolve().relative_to(top.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _target(place: Place, list_path: Path, link: str) -> tuple[Path | None, str, Path, str]:
    """The file LINK names from LIST_PATH, its anchor, and its repository's top folder and name.

    A page of Memar's published repository names the file of PLACE's Memar checkout; a relative link a file of PLACE's
    own repository; a root-relative, other external or in-page link no file.
    """
    file_part, _, anchor = link.partition("#")
    if file_part.startswith(PUBLISHED_PAGES):
        published = file_part.removeprefix(PUBLISHED_PAGES)
        if place.memar is None or not published:
            return None, anchor, place.top, place.repository
        return (place.memar / unquote(published)).resolve(), anchor, place.memar, MEMAR_REPOSITORY
    if not file_part or file_part.startswith("/") or EXTERNAL_LINK.match(link):
        return None, anchor, place.top, place.repository
    return (list_path.parent / unquote(file_part)).resolve(), anchor, place.top, place.repository


def read_list(place: Place, path: Path, word: str) -> ReferenceList:
    """The list in the file PATH of PLACE, for the act WORD."""
    entries = []
    for number, line in enumerate(_fenceless(read_text(path)).splitlines(), 1):
        match = ENTRY.match(line)
        if match is None:
            continue
        target, anchor, top, repository = _target(place, path, match["link"])
        entries.append(
            Entry(
                place, path, number, match["label"], match["link"], target, anchor,
                (match["why"] or "").strip(), match["mark"], bool(match["drop"]), top, repository,
            )
        )
    return ReferenceList(place, path, word, tuple(entries))


def list_files(folder: Path) -> list[tuple[str, Path]]:
    """The files directly in FOLDER named like a list, with the word each names, by name; none when FOLDER is no folder."""
    if not folder.is_dir():
        return []
    found = []
    for path in sorted(folder.iterdir(), key=lambda each: each.name):
        match = LIST_FILE.match(path.name)
        if match and path.is_file():
            found.append((match["word"], path))
    return found


def lists(places: list[Place] | tuple[Place, ...]) -> list[ReferenceList]:
    """Every list in PLACES, place by place in the order given, and within a place by file name."""
    return [read_list(place, path, word) for place in places for word, path in list_files(place.folder)]


def section_text(entry: Entry, texts: dict[Path, str | None] | None = None) -> str | None:
    """The section ENTRY names as it reads now, the whole document for an entry with no anchor; None when it is not there."""
    if entry.target is None or entry.path is None:
        return None
    cache = {} if texts is None else texts
    if entry.target not in cache:
        cache[entry.target] = read_text(entry.target) if entry.target.is_file() else None
    text = cache[entry.target]
    if text is None:
        return None
    return text.strip() if not entry.anchor else by_anchor(text, entry.anchor)


def current_hash(entry: Entry, texts: dict[Path, str | None] | None = None) -> str | None:
    """The hash of the section ENTRY names as it reads now; None when it is not there."""
    found = section_text(entry, texts)
    return None if found is None else section_hash(found)
