#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/normative_references_check.py — what `memar content check` reports of a normative-references list.

The governance report of the rule
[Normative References](../rules/normative_references/normative_references.md):
the composer prints what an act reads whatever state a list is in, and marks a
changed or broken entry where it prints it; this says what a list's owner must
repair. `content_check` calls it for every Markdown file.

A file is judged as a list only where lists are read: in Memar's declared place,
or in a folder the preference `normative_references` of the project it lies in
declares (`modules/process/project/services/preferences.py`; the project is the nearest folder
above the file that holds a preferences file). A file named like a list anywhere
else is not read, and is warned of, since a fixture or an example is legitimate
there and an author who believed it binding learns otherwise. A missing file or
anchor in a relative link is the anchor check's report (`content_links.link_problems`),
not repeated here; a link to Memar's published pages is not a relative link, so
this reports the section it names when it is not in Memar's checkout.

**A project's list** may name its own sections by relative links and Memar's by
their published address. It may drop a passage Memar's list for the same act
names, with a reason; it may not drop an every-act section, which is refused. A
list of Memar names its sections relatively only.

**Counting drops.** `list_drops` is how many passages of Memar a project's list
removes, the number `check`'s summary line says: only a drop that removes a
passage counts, not one with no reason, one of an every-act section, or one of a
passage no list of Memar names.
"""
from __future__ import annotations

from pathlib import Path

from modules.knowledge.content.services.reference import read_text
from modules.knowledge.content.services.section import span_by_anchor
from modules.knowledge.content.services.normative_references import (
    EVERY_ACT,
    LIST_FILE,
    REVIEWED_MARK,
    Entry,
    Place,
    current_hash,
    lists,
    memar_place,
    read_list,
)
from modules.process.project.services.preferences import preferences_path
from modules.knowledge.content.services.normative_references import normative_reference_places
from modules.knowledge.documentation.plan.primitive.task_kind import TaskKind

OUTSIDE_WARNING = "not read: outside the declared places"
CHANGED = (
    "changed since reviewed: re-read the section, then update the hash; "
    "if the section was split, add an entry for each part the act must read"
)
EVERY_ACT_REFUSED = "refused: the every-act sections cannot be dropped"


def _word(path: Path) -> str | None:
    match = LIST_FILE.match(path.name)
    return None if match is None else match["word"]


def _project_top(path: Path) -> Path | None:
    """The nearest folder above PATH that holds a preferences file, the project PATH lies in; None when none does."""
    for folder in path.resolve().parents:
        if preferences_path(folder).is_file():
            return folder
    return None


def place_of(path: Path, root: Path) -> Place | None:
    """The declared place the folder of PATH is, Memar's under ROOT or a folder a project's preference declares; None when it is neither."""
    folder = path.resolve().parent
    memar = memar_place(root)
    if folder == memar.folder.resolve():
        return memar
    top = _project_top(path)
    if top is None:
        return None
    places, _ = normative_reference_places(top, root)
    return next((place for place in places if place.folder.resolve() == folder), None)


def _resolves(entry: Entry) -> bool:
    """Whether ENTRY's link names a section that is there, its file and its anchor."""
    if entry.target is None or not entry.target.is_file():
        return False
    return not entry.anchor or span_by_anchor(read_text(entry.target), entry.anchor) is not None


def _named_by_memar(root: Path, *words: str) -> set[tuple[Path, str]]:
    """The passages Memar's lists for the acts WORDS name, a word being a kind's or the every-act one."""
    return {
        (entry.target, entry.anchor)
        for found in lists([memar_place(root)])
        if found.word in words
        for entry in found.entries
        if not entry.drops and entry.target is not None
    }


def list_problems(path: Path, root: Path) -> list[str]:
    """The problems of PATH as a list in a declared place under ROOT; none for a file that is not one."""
    word = _word(path)
    place = None if word is None else place_of(path, root)
    if word is None or place is None:
        return []
    problems: list[str] = []
    known = (EVERY_ACT, *TaskKind.words())
    if word not in known:
        problems.append(f"the list's word '{word}' names no kind; the words are {', '.join(known)}")
    named = every_act = None
    for entry in read_list(place, path, word).entries:
        line = f"line {entry.line}"
        if entry.root_relative:
            problems.append(
                f"{line}: root-relative link {entry.link}: an entry's link is written relative to its list, "
                "since in a project's list a root-relative one could mean the project's root or Memar's"
            )
            continue
        if entry.published and place.is_memar:
            problems.append(f"{line}: {entry.link} is a published address: a list of Memar links its sections relatively")
            continue
        if entry.target is None or entry.path is None or entry.target.suffix.lower() != ".md":
            repository = "Memar's checkout" if entry.published else "this repository"
            problems.append(f"{line}: {entry.link} names no Markdown file of {repository}")
            continue
        if not _resolves(entry):
            if entry.published:
                problems.append(f"{line}: {entry.link} names no section of Memar's checkout")
            continue
        if entry.drops:
            named = _named_by_memar(root, word, EVERY_ACT) if named is None else named
            every_act = _named_by_memar(root, EVERY_ACT) if every_act is None else every_act
            key = (entry.target, entry.anchor)
            if not place.is_memar and key in every_act:
                problems.append(f"{line}: {EVERY_ACT_REFUSED}: {entry.link}")
            elif key not in named:
                problems.append(f"{line}: drops nothing: no list of Memar for this act names {entry.link}")
            elif not entry.why:
                problems.append(f"{line}: a drop with no reason: say after the link, once the ' — ', why this project does not read it")
            continue
        now = current_hash(entry)
        if entry.reviewed is None:
            problems.append(
                f"{line}: no review mark: read the section, then end the entry with `{REVIEWED_MARK} {now}`, "
                "the hash `memar content section FILE '#anchor' --hash` prints"
            )
        elif entry.reviewed != now:
            problems.append(f"{line}: {CHANGED} (it is {now} now)")
    return problems


def list_drops(path: Path, root: Path) -> int:
    """How many passages of Memar PATH, a project's list, removes: those a drop with a reason names that Memar's list for its act names and no every-act list does."""
    word = _word(path)
    place = None if word is None else place_of(path, root)
    if word is None or place is None or place.is_memar:
        return 0
    named, every_act = _named_by_memar(root, word, EVERY_ACT), _named_by_memar(root, EVERY_ACT)
    removed = set()
    for entry in read_list(place, path, word).entries:
        key = (entry.target, entry.anchor)
        if entry.drops and entry.why and entry.target is not None and key in named and key not in every_act:
            removed.add(key)
    return len(removed)


def is_declared(path: Path, root: Path) -> bool:
    """Whether PATH is a file named like a list in a declared place."""
    return _word(path) is not None and place_of(path, root) is not None


def list_warnings(path: Path, root: Path) -> list[str]:
    """The warnings of PATH: named like a list outside the declared places under ROOT, or one passage twice in a list."""
    word = _word(path)
    if word is None:
        return []
    place = place_of(path, root)
    if place is None:
        return [OUTSIDE_WARNING]
    seen: dict[tuple[Path | None, str], int] = {}
    warnings = []
    for entry in read_list(place, path, word).entries:
        key = (entry.target, entry.anchor)
        if entry.target is not None and key in seen:
            warnings.append(f"line {entry.line}: names the same passage as line {seen[key]}")
        else:
            seen.setdefault(key, entry.line)
    return warnings
