#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/text/services/index.py — the index `memar content find` ranks: the sections of the checkout's content, scored by word similarity.

**The corpus is the one `content_corpus` names**, the same as `search`'s, so no verb sees a narrower
or a wider world than the verb beside it. Its units are each Markdown section, from its heading to
the next heading of any level, and each document's text before its first heading; each `.kh` file
is one unit, since a declaration file has no headings. A unit records the links its text makes to
a section by anchor, resolved to a document of the corpus, which `find` prints under a hit. Its
sources are those `--from` names (`CorpusSource`), the documents and the code without it; the
tasks' files, read by `task_records.py`, are ranked the same way, a Markdown file by its
sections and any other text file as one unit named by its file, and the notes on what of them
could not be read are carried with the index for the verb to print.

**The ranking is BM25 over weighted fields**, the constants below. They are kept because they are
the first version's and nothing measured beats them, not because the probe of proposal v3 (section
11, 50 frozen tasks) chose them: no variant it measured can be told from them case by case on
the documents a planner named. A constant changes only when a variant beats the current one case
by case at a two-sided sign-test p below 0.05, on that sample plus the tasks completed since.
It does not find what an act must read: at most 12% of a kind's sections are in a top 10 with
links, which is why the lists of `normative_references` exist; the ranking is informative.

**The index is built in memory on each call** and kept nowhere: about a second for Memar's corpus,
a query in tens of milliseconds. A file to keep true by hand beside the documents would be a copy
with no re-derivation path.

**A process that lives across calls may ask to keep it** with `keep()`, which the MCP adapter's
worker does (`bundles/memar/services/mcp/`). Then each file's units are kept in memory with the stat they
were read at, and every `build` still lists the corpus and stats every file, so an added, deleted or
edited document is seen on the next call: a file whose size or modification time changed is read
again. A stat can stay the same across a write, when a second write lands in the same tick of the
filesystem's clock, so a file read within `RACY_SECONDS` of its modification time is read again on
the next call too, and kept only when its text's SHA-256 is unchanged; once read later than that, its
stat is trusted. A process that never asks keeps nothing, as before.

TODO(when the Memar server exists): rank by meaning as well as by words — a dense vector per
section, keyed by its hash, fused with BM25 by reciprocal rank. It needs a model this offline tool
does not carry. Recorded 2026-10-16, task 20261016-T135247Z-15464; the study of the server is
task 20261016-T095101Z-14276; the keep, task 20261019-T111413Z-21136.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
import hashlib
import math
import posixpath
import re
import time
from collections import Counter
from pathlib import Path, PurePath, PurePosixPath
from typing import NamedTuple
from modules.knowledge.text.services.corpus import content_files
from modules.knowledge.content.services.reference import read_text
_m_content_get_section = plugable_load('computer.codec.markdown.services.content_get_section')
outline = _m_content_get_section.outline
section_hash = _m_content_get_section.section_hash
K1 = 1.2
B = 0.75
HEADING_WEIGHT = 3
PATH_WEIGHT = 1
BODY_WEIGHT = 1
PER_DOCUMENT = 2
STOP = frozenset('the a an of to and or in is are for on that this it as be by with from at not its which each one into than then so if when what'.split())
WORD = re.compile('[a-z0-9][a-z0-9_-]+')
MINIMUM_WORD = 3
LINK = re.compile('\\[[^\\]]*\\]\\(([^)\\s]+)\\)')
EXTERNAL = re.compile('^[a-z][a-z0-9+.-]*:', re.IGNORECASE)
RACY_SECONDS = 2

class Unit(NamedTuple):
    """One section: its document's path from the checkout, where in the document's text it runs and where its whole section
    (subsections included) stops, its heading and anchor (both empty for the text before a first heading), its section's
    hash, the sections it links as (path, anchor), and whether it is a `.kh` file."""
    path: str
    start: int
    end: int
    stop: int
    heading: str
    anchor: str
    hash: str
    links: tuple[tuple[str, str], ...]
    kh: bool

class Index(NamedTuple):
    """The units, each document's text, what ranking needs of them, and the notes on what of the tasks could not be read."""
    units: tuple[Unit, ...]
    texts: dict[str, str]
    fields: tuple[Counter, ...]
    lengths: tuple[int, ...]
    idf: dict[str, float]
    notes: tuple[str, ...] = ()

    def rank(self, query: str) -> list[int]:
        """The numbers of the units with a word of QUERY, best first, at most `PER_DOCUMENT` of one document."""
        asked = set(words(query))
        average = sum(self.lengths) / len(self.lengths) if self.lengths else 1
        scored = []
        for number, field in enumerate(self.fields):
            norm = K1 * (1 - B + B * self.lengths[number] / average)
            score = sum((self.idf[word] * field[word] * (K1 + 1) / (field[word] + norm) for word in asked if field.get(word)))
            if score > 0:
                scored.append((-score, number))
        scored.sort()
        taken: Counter = Counter()
        ranked = []
        for _, number in scored:
            path = self.units[number].path
            if taken[path] < PER_DOCUMENT:
                taken[path] += 1
                ranked.append(number)
        return ranked

    def text_of(self, unit: Unit) -> str:
        """The text UNIT runs over, its heading line first."""
        return self.texts[unit.path][unit.start:unit.end]

def words(text: str) -> list[str]:
    """The words of TEXT that count: lower case, not a stop word, at least `MINIMUM_WORD` characters."""
    return [word for word in WORD.findall(text.lower()) if word not in STOP and len(word) >= MINIMUM_WORD]

def _link_target(path: str, link: str) -> tuple[str, str] | None:
    """The (document, anchor) a LINK in the document at PATH names by anchor; None for an external link or one with no anchor."""
    if EXTERNAL.match(link):
        return None
    file_part, _, anchor = link.partition('#')
    if not anchor:
        return None
    if not file_part:
        return (path, anchor)
    joined = file_part.lstrip('/') if file_part.startswith('/') else posixpath.join(posixpath.dirname(path), file_part)
    return (posixpath.normpath(joined), anchor)

def _links(path: str, body: str) -> tuple[tuple[str, str], ...]:
    found = (_link_target(path, link) for link in LINK.findall(body))
    return tuple(dict.fromkeys((target for target in found if target is not None)))

def _units(path: str, text: str) -> list[Unit]:
    headings = outline(text)
    bounds = [(0, 0, '', '', None)] + [(each.start, each.level, each.heading, each.anchor, each) for each in headings]
    units = []
    for number, (start, _, heading, anchor, found) in enumerate(bounds):
        end = bounds[number + 1][0] if number + 1 < len(bounds) else len(text)
        if not found and (not text[start:end].strip()):
            continue
        stop = found.stop if found else end
        units.append(Unit(path, start, end, stop, heading, anchor, section_hash(text[start:stop]), _links(path, text[start:end]), False))
    return units

class Read(NamedTuple):
    """One file as the index holds it: its text, its units, and each unit's weighted words and body length."""
    text: str
    units: tuple[Unit, ...]
    fields: tuple[Counter, ...]
    lengths: tuple[int, ...]

class Kept(NamedTuple):
    """One file kept across calls: the stat it was read at, when it was read, its text's SHA-256, and what was read."""
    size: int
    modified: int
    read_at: int
    digest: str
    read: Read
_kept: dict[object, dict[str, Kept]] | None = None

def _tasks_key(root: Path) -> tuple[Path, str]:
    return (root.resolve(), 'tasks')

def keep() -> None:
    """Keep each file's units across the `build` calls of this process, checked by stat on every call."""
    global _kept
    if _kept is None:
        _kept = {}

def _read(path: str, file: PurePath, text: str) -> Read:
    suffix = file.suffix.lower()
    if suffix == '.kh':
        units = [Unit(path, 0, len(text), len(text), file.stem, '', section_hash(text), (), True)]
    elif suffix == '.md':
        units = _units(path, text)
    else:
        units = [Unit(path, 0, len(text), len(text), file.name, '', section_hash(text), (), False)]
    fields, lengths = ([], [])
    for unit in units:
        body = text[unit.start:unit.end]
        field: Counter = Counter()
        for weight, part in ((HEADING_WEIGHT, unit.heading), (PATH_WEIGHT, unit.path.replace('/', ' ').replace('.', ' ')), (BODY_WEIGHT, body)):
            for word in words(part):
                field[word] += weight
        fields.append(field)
        lengths.append(len(words(body)) + 1)
    return Read(text, tuple(units), tuple(fields), tuple(lengths))

def _digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def _read_kept(kept: dict[str, Kept], path: str, file: Path) -> Read:
    """FILE's read, from KEPT when its stat says it is unchanged; read again, and kept, when not."""
    status = file.stat()
    now = time.time_ns()
    found = kept.get(path)
    if found and found.size == status.st_size and (found.modified == status.st_mtime_ns):
        if found.read_at - found.modified >= RACY_SECONDS * 1000000000:
            return found.read
        text = read_text(file)
        digest = _digest(text)
        read = found.read if digest == found.digest else _read(path, file, text)
    else:
        text = read_text(file)
        digest = _digest(text)
        read = _read(path, file, text)
    kept[path] = Kept(status.st_size, status.st_mtime_ns, now, digest, read)
    return read

def _task_reads(root: Path, kept: dict[str, Kept] | None) -> tuple[list[tuple[str, Read]], list[str]]:
    """Each text file of the tasks of the project at ROOT, read, by the path a hit names; and the notes on what could not be read.

    A live file is kept as a document is, by its stat; an archived one by its blob id, which
    changes whenever its bytes do. A file that turns out binary is left out.
    """
    _m_task_records = plugable_load('management.task.services.task_records')
    read_all = _m_task_records.read_all
    task_records = _m_task_records.task_records
    records, notes = task_records(root)
    reads: dict[str, Read] = {}
    missing = []
    for record in records:
        if record.file is not None:
            read = _read(record.path, PurePosixPath(record.path), read_text(record.file)) if kept is None else _read_kept(kept, record.path, record.file)
            if '\x00' not in read.text:
                reads[record.path] = read
        elif kept is not None and record.path in kept and (kept[record.path].digest == record.blob):
            reads[record.path] = kept[record.path].read
        else:
            missing.append(record)
    blobs = {each.path: each.blob or '' for each in missing}
    for path, text in read_all(root, missing).items():
        read = _read(path, PurePosixPath(path), text)
        reads[path] = read
        if kept is not None:
            kept[path] = Kept(0, 0, 0, blobs[path], read)
    ordered = [(record.path, reads[record.path]) for record in records if record.path in reads]
    if kept is not None:
        for gone in set(kept) - set(reads):
            del kept[gone]
    return (ordered, notes)

def build(root: Path, sources=None) -> Index:
    """The index of the corpus of the checkout at ROOT, of the SOURCES named (`CorpusSource`; the default ones without), read now, or checked now against what `keep()` kept."""
    from modules.knowledge.text.primitive.corpus_source import CorpusSource
    chosen = CorpusSource.default() if sources is None else tuple(sources)
    kept = None if _kept is None else _kept.setdefault(root.resolve(), {})
    units: list[Unit] = []
    texts: dict[str, str] = {}
    fields: list[Counter] = []
    lengths: list[int] = []
    seen: set[str] = set()
    reads: list[tuple[str, Read]] = []
    for file in content_files(root, chosen):
        path = file.relative_to(root).as_posix()
        reads.append((path, _read(path, file, read_text(file)) if kept is None else _read_kept(kept, path, file)))
    notes: list[str] = []
    if CorpusSource.TASKS in chosen:
        tasks_kept = None if _kept is None else _kept.setdefault(_tasks_key(root), {})
        found, notes = _task_reads(root, tasks_kept)
        reads.extend(found)
    for path, read in reads:
        seen.add(path)
        texts[path] = read.text
        units.extend(read.units)
        fields.extend(read.fields)
        lengths.extend(read.lengths)
    if kept is not None:
        read_suffixes = {suffix for source in chosen for suffix in source.suffixes}
        for gone in set(kept) - seen:
            if PurePosixPath(gone).suffix.lower() in read_suffixes:
                del kept[gone]
    frequency: Counter = Counter()
    for field in fields:
        frequency.update(field.keys())
    count = len(units)
    idf = {word: math.log(1 + (count - seen + 0.5) / (seen + 0.5)) for word, seen in frequency.items()}
    return Index(tuple(units), texts, tuple(fields), tuple(lengths), idf, tuple(notes))
