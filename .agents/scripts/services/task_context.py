#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/task_context.py — the context of a set of kinds: the sections their normative references name, read and printed once each.

What an act reads before it starts is declared by the lists of the rule
[Normative References](../rules/normative_references/normative_references.md),
read by `services/normative_references.py`; this composes the sections they name
into the text an agent reads. Two commands print it, and neither composes on its
own: `memar session start`, for the Kind of the session's plan, followed by the
documents the plan's Steps name; and `memar content context`, for kinds given
with no session or with one.

**Places are explicit.** The lists are read from the places given — Memar's,
and later a project's — and every call reads the lists and the sections from
the live files, so what prints is what the files hold now.

**Order.** The every-act list's sections first, then each kind's in the order
the kinds are given; within one list group, in corpus order: the places in the
order given, then documents by path, then sections in document order, whatever
order a list writes them in. Each section prints under a line naming it, and
below that its entry's why.

**Each section once.** A section two kinds name prints once, and so does one
that lies inside another being printed, whichever comes first: the larger one
prints. That is told by where each section lies in its document, not by its
link, because two links can name text that overlaps.

**A changed or missing entry.** A section whose hash differs from its entry's
mark prints as it reads now, its line marked "changed since reviewed" with the
entry's list and line. An entry whose section is not there prints its link,
label and why, marked "anchor gone", so a mandatory passage is never dropped in
silence. A drop prints where the passage would have stood, with its reason; the
every-act sections are never dropped.

**The first line** counts what the context holds: its kinds, the sections the
lists gave it, what was left out as already printed, what changed or is gone,
and what was dropped.

**What was printed before.** A session's `temp/context_read.txt` records each
section a context printed for it: repository, path with forward slashes,
anchor, hash. Given kinds already read (`--after`), the sections their lists
name that the record holds with the same hash are left out, and so is a
Practice's description already printed with them; a section added to a list
since, or changed since it was printed, prints.

**A Practice's description.** A Practice says in its front matter's
`description` what it is for and when it applies. That sentence is printed
once, above the first section taken from it; a document with no `description`
gets none.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, NamedTuple, Sequence

from services.content_reference import read_text
from services.content_section import section_hash, span_by_anchor
from services.module_folders import TEMP_FOLDER
from services.normative_references import EVERY_ACT, MEMAR_REPOSITORY, Entry, Place, ReferenceList, lists, memar_place
from services.project_preferences import normative_reference_places
from services.session_plan import front_matter
from services.task_kind import TaskKind

# The anchor a reference with none is read at, for a document a plan's Steps name.
ABSTRACT = "abstract"
DESCRIPTION_KEY = "description"
# The record, in a session's temp folder, of every section a context printed for it.
CONTEXT_READ = "context_read.txt"
RECORD_SEPARATOR = "\t"
CHANGED_MARK = "changed since reviewed"
GONE_MARK = "anchor gone"
DROPPED_MARK = "dropped"
WHY_LABEL = "Why: "


class Ref(NamedTuple):
    """A section to print: its repository's top folder, its path from there, its anchor, the repository's name, and the entry that names it or the drop that removes it.

    A Ref with no entry is a document a plan's Steps name, read at its Abstract when it has no anchor; one with an
    entry and no anchor is that entry's whole document.
    """

    top: Path
    path: str
    anchor: str = ""
    repository: str = MEMAR_REPOSITORY
    entry: Entry | None = None
    drop: Entry | None = None


class Printed(NamedTuple):
    """One line of the record: a section as it was printed."""

    repository: str
    path: str
    anchor: str
    hash: str


class Composed(NamedTuple):
    """What a composition printed: its blocks, the sections it printed, and the entries it printed changed, gone and dropped.

    `listed` and `dropped` count what Memar's lists named and removed, `listed_project` and `dropped_project` what a
    project's lists did; `dropped` holds every drop, a project's included.
    """

    blocks: list[str]
    printed: list[Printed]
    listed: int
    changed: int
    gone: int
    dropped: int
    listed_project: int = 0
    dropped_project: int = 0


class _Read(NamedTuple):
    """REF as read: the heading line printed above it, and its span in its document's text, or the reason it has none."""

    ref: Ref
    header: str
    span: tuple[int, int] | None
    absent: str | None


def _name(ref: Ref) -> str:
    where = ref.path if ref.repository == MEMAR_REPOSITORY else f"{ref.repository}: {ref.path}"
    if ref.anchor:
        return f"{where}#{ref.anchor}"
    return where if ref.entry is not None else f"{where} (Abstract)"


def _header(ref: Ref, mark: str | None = None) -> str:
    return f"--- {_name(ref)}" + (f" ({mark})" if mark else "") + " ---"


def _text_of(ref: Ref, texts: dict[Path, str | None]) -> str | None:
    file = ref.top / ref.path
    if file not in texts:
        texts[file] = read_text(file) if file.is_file() else None
    return texts[file]


def _read(ref: Ref, texts: dict[Path, str | None]) -> _Read:
    text = _text_of(ref, texts)
    if text is None:
        return _Read(ref, _header(ref), None, f"the document {ref.path} is not there in this checkout")
    if ref.entry is not None and not ref.anchor:
        return _Read(ref, _header(ref), (0, len(text)), None)
    span = span_by_anchor(text, ref.anchor or ABSTRACT)
    if span is None:
        return _Read(ref, _header(ref), None, f"no section answers to #{ref.anchor or ABSTRACT} in {ref.path}")
    return _Read(ref, _header(ref), span, None)


def _covered(read: _Read, index: int, every: list[_Read]) -> bool:
    """Whether another reading holds READ: one of its document, not a drop, whose span contains READ's, larger or earlier."""
    for other_index, other in enumerate(every):
        if other_index == index or (other.ref.top, other.ref.path) != (read.ref.top, read.ref.path) or other.ref.drop:
            continue
        if read.span is None or other.span is None:
            if read.span is None and other.span is None and other.header == read.header and other_index < index:
                return True
            continue
        inside = other.span[0] <= read.span[0] and read.span[1] <= other.span[1]
        if inside and (other.span != read.span or other_index < index):
            return True
    return False


def _description(text: str | None) -> str | None:
    if text is None:
        return None
    front, _ = front_matter(text.splitlines())
    return (front or {}).get(DESCRIPTION_KEY) or None


def _section(read: _Read, texts: dict[Path, str | None]) -> str:
    return (_text_of(read.ref, texts) or "")[read.span[0] : read.span[1]].strip()


def compose(wanted: Sequence[Ref], earlier: Sequence[Ref] = ()) -> Composed:
    """WANTED's sections, in order, each once and none that EARLIER already printed."""
    texts: dict[Path, str | None] = {}
    every = [_read(ref, texts) for ref in (*earlier, *wanted)]
    described = {(read.ref.top, read.ref.path) for read in every[: len(earlier)]}
    blocks: list[str] = []
    printed: list[Printed] = []
    listed = listed_project = changed = gone = dropped = dropped_project = 0
    for index in range(len(earlier), len(every)):
        read = every[index]
        ref, entry = read.ref, read.ref.entry
        if _covered(read, index, every):
            continue
        if ref.drop is not None:
            dropped += 1
            dropped_project += not ref.drop.place.is_memar
            blocks.append(f"{_header(ref, DROPPED_MARK)}\ndropped by {ref.drop.located}: {ref.drop.why}")
            continue
        document = (ref.top, ref.path)
        if document not in described:
            described.add(document)
            description = _description(_text_of(ref, texts))
            if description:
                where = ref.path if ref.repository == MEMAR_REPOSITORY else f"{ref.repository}: {ref.path}"
                blocks.append(f"--- {where} (description) ---\n{description}")
        if read.span is None:
            if entry is None:
                blocks.append(f"{read.header}\n{read.absent}")
            else:
                gone += 1
                blocks.append(f"{_header(ref, f'{GONE_MARK}: {entry.located}')}\n{entry.written}\n{read.absent}")
            continue
        section = _section(read, texts)
        now = section_hash(section)
        printed.append(Printed(ref.repository, ref.path, ref.anchor, now))
        if entry is None:
            blocks.append(f"{read.header}\n{section}")
            continue
        if entry.place.is_memar:
            listed += 1
        else:
            listed_project += 1
        mark = None
        if entry.reviewed != now:
            changed += 1
            mark = f"{CHANGED_MARK}: {entry.located}"
        blocks.append(f"{_header(ref, mark)}\n{WHY_LABEL}{entry.why}\n{section}")
    return Composed(blocks, printed, listed, changed, gone, dropped, listed_project, dropped_project)


def _order(ref: Ref, places: Sequence[Place], texts: dict[Path, str | None]) -> tuple[int, str, float]:
    """REF's corpus order: its place, its document's path, its section's place in the document (a gone one last)."""
    place = places.index(ref.entry.place) if ref.entry.place in places else len(places)
    text = _text_of(ref, texts)
    span = None if text is None else ((0, 0) if not ref.anchor else span_by_anchor(text, ref.anchor))
    return place, ref.path, float("inf") if span is None else span[0]


def _ref(entry: Entry, drop: Entry | None = None) -> Ref:
    return Ref(entry.top, entry.path or entry.link, entry.anchor, entry.repository, entry, drop)


def _group(found: Sequence[ReferenceList], word: str, places: Sequence[Place], every_act: set, texts) -> list[Ref]:
    """The sections WORD's lists name, in corpus order, a drop standing where the passage it drops would have."""
    entries = [entry for listed in found if listed.word == word for entry in listed.entries]
    drops = {(entry.target, entry.anchor): entry for entry in entries if entry.drops and entry.why and entry.target is not None}
    refs = []
    for entry in entries:
        if entry.drops:
            continue
        key = (entry.target, entry.anchor)
        drop = drops.get(key) if key not in every_act else None
        refs.append(_ref(entry, drop))
    return sorted(refs, key=lambda ref: _order(ref, places, texts))


def kind_refs(places: Sequence[Place], kinds: Iterable[TaskKind]) -> list[Ref]:
    """The sections the every-act lists and KINDS' lists in PLACES name, group after group, each group in corpus order."""
    found = lists(list(places))
    every_act = {
        (entry.target, entry.anchor) for listed in found if listed.word == EVERY_ACT for entry in listed.entries if not entry.drops
    }
    texts: dict[Path, str | None] = {}
    words = list(dict.fromkeys([EVERY_ACT, *(kind.word for kind in kinds)]))
    return [ref for word in words for ref in _group(found, word, places, every_act, texts)]


def _same(refs: Sequence[Ref], record: set[Printed]) -> list[Ref]:
    """Those of REFS the RECORD holds as printed with the section's hash as it reads now."""
    texts: dict[Path, str | None] = {}
    kept = []
    for ref in refs:
        if ref.drop is not None:
            continue
        read = _read(ref, texts)
        if read.span is not None and Printed(ref.repository, ref.path, ref.anchor, section_hash(_section(read, texts))) in record:
            kept.append(ref)
    return kept


def _plural(count: int, word: str) -> str:
    return f"{count} {word}" + ("" if count == 1 else "s")


def first_line(
    kinds: Sequence[TaskKind], after: Sequence[TaskKind], composed: Composed, left_out: int, project_named: bool,
    project_places: bool = False, problems: Sequence[str] = (),
) -> str:
    """The context's first line: its kinds, the counts of what it holds and of what it left out, and the problems of a project's declared places."""
    words = ", ".join(kind.word for kind in kinds) or "none"
    parts = [f"kinds: {words}", f"{_plural(composed.listed, 'section')} from Memar's lists" + (f", {composed.listed_project} from this project's" if project_places else "")]
    if after:
        parts.append(f"after {', '.join(kind.word for kind in after)}: {_plural(left_out, 'section')} already printed left out")
    if composed.changed:
        parts.append(f"{composed.changed} {CHANGED_MARK}")
    if composed.gone:
        parts.append(f"{composed.gone} {GONE_MARK}")
    if composed.dropped_project:
        parts.append(f"{_plural(composed.dropped_project, 'passage')} of Memar {DROPPED_MARK} by this project (listed below)")
    if composed.dropped > composed.dropped_project:
        parts.append(f"{_plural(composed.dropped - composed.dropped_project, 'passage')} {DROPPED_MARK} (listed below)")
    parts.extend(problems)
    if not project_named:
        parts.append("no project named, so Memar's lists alone")
    return "; ".join(parts)


def context(
    places: Sequence[Place],
    kinds: Sequence[TaskKind],
    after: Sequence[TaskKind] = (),
    record: set[Printed] | frozenset = frozenset(),
    extra: Sequence[Ref] = (),
    project_named: bool = True,
    place_problems: Sequence[str] = (),
) -> Composed:
    """The context KINDS require from the lists in PLACES, then EXTRA; with AFTER, less what RECORD holds of AFTER's sections. Its first block is the first line.

    PLACE_PROBLEMS are the problems of the project's declared places (`context_places`), said on the first line.
    """
    earlier = _same(kind_refs(places, after), set(record)) if after else []
    composed = compose([*kind_refs(places, kinds), *extra], earlier)
    project_places = any(not place.is_memar for place in places)
    line = first_line(kinds, after, composed, len(earlier), project_named, project_places, place_problems)
    return composed._replace(blocks=[line, *composed.blocks])


def context_places(checkout: Path, project: Path | None) -> tuple[list[Place], list[str]]:
    """Every place a context reads lists from: Memar's in CHECKOUT, then the folders PROJECT's preference declares, and the problems with those."""
    declared, problems = normative_reference_places(project, checkout)
    places = [memar_place(checkout)]
    places.extend(place for place in declared if place not in places)
    return places, problems


def context_text(places: Sequence[Place], kinds: Sequence[TaskKind], **given) -> str:
    """The context `context` composes, as one text."""
    return "\n\n".join(context(places, kinds, **given).blocks)


def record_path(folder: Path) -> Path:
    """Where the session in FOLDER records what its contexts printed."""
    return folder / TEMP_FOLDER / CONTEXT_READ


def read_record(folder: Path) -> set[Printed]:
    """What the session in FOLDER's contexts printed; empty when nothing was recorded."""
    path = record_path(folder)
    if not path.is_file():
        return set()
    found = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split(RECORD_SEPARATOR)
        if len(fields) == len(Printed._fields):
            found.add(Printed(*fields))
    return found


def write_record(folder: Path, printed: Iterable[Printed]) -> None:
    """Add to the session in FOLDER's record each of PRINTED it does not hold yet."""
    held = read_record(folder)
    new = [line for line in dict.fromkeys(printed) if line not in held]
    if not new:
        return
    path = record_path(folder)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as record:
        for line in new:
            record.write(RECORD_SEPARATOR.join(line) + "\n")
