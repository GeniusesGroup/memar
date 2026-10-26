#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/normative_references.py — the lists of what each act reads before it starts, read from their declared places.

The rule is [Normative References](../../../../modules/knowledge/content/rules/normative_references/normative_references.md):
before an act starts, the agent reads every section the entries of the every-act
list and of its kinds' lists name. This file reads those lists and nothing else;
which kinds exist is `modules/management/task/labels/task_kind.py`'s, how the sections print is
`modules-plugable/ai/services/task_context.py`'s, and what `memar content check` reports of a list
is `modules-plugable/knowledge/documentation/services/normative_references_check.py`'s.

**Declared places.** A list is read only in a place declared to hold lists, so a
fixture or an example saved under a list's name binds nobody. Memar's place is
one folder, `MEMAR_PLACE`, under Memar's checkout: a constant and not a
preference, because Memar's lists bind every project and are found the same way
from every one. A project's places are the folders its preference `PREFERENCE`
names, read by `modules/process/project/services/preferences.py`; the places are always given
to `lists`, never inferred from the folder a command runs in.

**An entry** is one line at column 0, outside a fenced block: a list item whose
text begins with a link, then ` — ` and its why, then the review mark last, a
code span `reviewed` and the hash `memar content get-section FILE '#anchor' --hash`
prints. An entry that begins `Not read here: ` before its link drops a passage
and carries its reason as its why and no mark. Any other line of a list is not
an entry: the shape is the declaration.

**Where an entry's link leads.** A relative link names a file of the place's own
repository. In a project's list a link may instead be a page of Memar's
published repository (`modules-plugable/computer/memory/filesystem/services/fs_memar.py`'s `PUBLISHED_PAGES`): it names that
file of the Memar checkout the place was given, and is read and hashed from
there, so a project can name a passage Memar's lists omit, or drop one they name,
without knowing where Memar's checkout lies on a machine.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
PUBLISHED_PAGES = _m_fs_memar.PUBLISHED_PAGES
import re
from pathlib import Path, PurePosixPath
from typing import NamedTuple
from urllib.parse import unquote
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
EXTERNAL_LINK = _m_markdown.EXTERNAL_LINK
from modules.knowledge.content.services.reference import read_text
_m_content_get_section = import_module('modules-plugable.computer.codec.markdown.services.content_get_section')
_fenceless = _m_content_get_section._fenceless
by_anchor = _m_content_get_section.by_anchor
section_hash = _m_content_get_section.section_hash
from modules.process.project.services.preferences import FOLDER_SEPARATOR, NORMATIVE_REFERENCES_KEY, preferences_path, read_preferences
RULE = 'normative_references'
MEMAR_PLACE = PurePosixPath('modules/knowledge/content/rules') / RULE
LIST_NAME = f'{RULE}-{{word}}.md'
PREFERENCE = NORMATIVE_REFERENCES_KEY
assert PREFERENCE == RULE
EVERY_ACT = 'every_act'
MEMAR_REPOSITORY = 'memar'
DROP_MARK = 'Not read here: '
REVIEWED_MARK = 'reviewed'
WHY_MARK = ' — '
_PREFIX, _SUFFIX = LIST_NAME.split('{word}')
LIST_FILE = re.compile(f'^{re.escape(_PREFIX)}(?P<word>.+){re.escape(_SUFFIX)}$')
ENTRY = re.compile(f'^- (?P<drop>{re.escape(DROP_MARK)})?\\[(?P<label>[^\\]]+)\\]\\((?P<link>[^)\\s]+)\\)(?:{re.escape(WHY_MARK)}(?P<why>.*?))?(?:\\s*`{REVIEWED_MARK} (?P<mark>[0-9a-f]+)`)?\\s*$')

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
        return self.repository == MEMAR_REPOSITORY and self.memar == self.top and (self.folder == self.top / MEMAR_PLACE)

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
        return f'{_posix(self.list_path, self.place.top)}:{self.line}'

    @property
    def located(self) -> str:
        """`where`, a project's under the project's name, so that a reader of a context tells it from Memar's."""
        return self.where if self.place.is_memar else f'{self.place.repository}: {self.where}'

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
        return self.link.startswith('/')

    @property
    def written(self) -> str:
        """The entry's link and why as the list writes them, for a reader who must find the section it meant."""
        return f'[{self.label}]({self.link})' + (f'{WHY_MARK}{self.why}' if self.why else '')

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
    file_part, _, anchor = link.partition('#')
    if file_part.startswith(PUBLISHED_PAGES):
        published = file_part.removeprefix(PUBLISHED_PAGES)
        if place.memar is None or not published:
            return (None, anchor, place.top, place.repository)
        return ((place.memar / unquote(published)).resolve(), anchor, place.memar, MEMAR_REPOSITORY)
    if not file_part or file_part.startswith('/') or EXTERNAL_LINK.match(link):
        return (None, anchor, place.top, place.repository)
    return ((list_path.parent / unquote(file_part)).resolve(), anchor, place.top, place.repository)

def read_list(place: Place, path: Path, word: str) -> ReferenceList:
    """The list in the file PATH of PLACE, for the act WORD."""
    entries = []
    for number, line in enumerate(_fenceless(read_text(path)).splitlines(), 1):
        match = ENTRY.match(line)
        if match is None:
            continue
        target, anchor, top, repository = _target(place, path, match['link'])
        entries.append(Entry(place, path, number, match['label'], match['link'], target, anchor, (match['why'] or '').strip(), match['mark'], bool(match['drop']), top, repository))
    return ReferenceList(place, path, word, tuple(entries))

def list_files(folder: Path) -> list[tuple[str, Path]]:
    """The files directly in FOLDER named like a list, with the word each names, by name; none when FOLDER is no folder."""
    if not folder.is_dir():
        return []
    found = []
    for path in sorted(folder.iterdir(), key=lambda each: each.name):
        match = LIST_FILE.match(path.name)
        if match and path.is_file():
            found.append((match['word'], path))
    return found

def lists(places: list[Place] | tuple[Place, ...]) -> list[ReferenceList]:
    """Every list in PLACES, place by place in the order given, and within a place by file name."""
    return [read_list(place, path, word) for place in places for word, path in list_files(place.folder)]

def section_text(entry: Entry, texts: dict[Path, str | None] | None=None) -> str | None:
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

def current_hash(entry: Entry, texts: dict[Path, str | None] | None=None) -> str | None:
    """The hash of the section ENTRY names as it reads now; None when it is not there."""
    found = section_text(entry, texts)
    return None if found is None else section_hash(found)

def normative_reference_places(project: Path | None, memar: Path) -> tuple[list[Place], list[str]]:
    """The places PROJECT's preferences declare for its own normative-references lists, and the problems with what they name.

    One place for each folder the key names, in the order named, under the project's folder name and with MEMAR, the
    Memar checkout, as the checkout its links to Memar's published pages are read from. A folder that is not a folder, is
    the top folder itself, is an absolute path or leaves the project is a problem naming the file and the value, and gives no
    place; the others still do. None for no project, or an empty or absent key.
    """
    if project is None:
        return ([], [])
    value = read_preferences(project).get(PREFERENCE, '').strip().strip('"\'').strip()
    top = project.resolve()
    places: list[Place] = []
    problems: list[str] = []
    for named in (each.strip() for each in value.split(FOLDER_SEPARATOR)):
        if not named:
            continue
        folder = (top / named).resolve()
        if Path(named).is_absolute() or named.startswith(('/', '\\')):
            refused = "an absolute path; name a folder relative to the project's top folder"
        elif folder == top:
            refused = "the project's top folder itself"
        elif top not in folder.parents:
            refused = 'a folder outside the project'
        elif not folder.is_dir():
            refused = 'not a folder'
        else:
            place = Place(project.name, project, project / named, memar)
            if place not in places:
                places.append(place)
            continue
        problems.append(f'{preferences_path(project).as_posix()}: {PREFERENCE} {named!r} is {refused}')
    return (places, problems)
