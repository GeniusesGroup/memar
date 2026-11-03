#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
Abstract = import_module('modules-plugable.knowledge.documentation.explanation.primitive.abstract').Abstract
_m_practice_key = import_module('modules-plugable.knowledge.documentation.practice.primitive.practice_key')
PracticeKey = _m_practice_key.PracticeKey
from pathlib import Path
from typing import Iterable, NamedTuple, Sequence
from modules.knowledge.content.services.reference import read_text
_m_content_get_section = import_module('modules-plugable.computer.codec.markdown.services.content_get_section')
outline = _m_content_get_section.outline
section_hash = _m_content_get_section.section_hash
span_by_anchor = _m_content_get_section.span_by_anchor
_m_normative_references = import_module('modules-plugable.knowledge.documentation.services.normative_references')
EVERY_ACT = _m_normative_references.EVERY_ACT
MEMAR_REPOSITORY = _m_normative_references.MEMAR_REPOSITORY
Entry = _m_normative_references.Entry
Place = _m_normative_references.Place
ReferenceList = _m_normative_references.ReferenceList
lists = _m_normative_references.lists
memar_place = _m_normative_references.memar_place
_m_normative_references = import_module('modules-plugable.knowledge.documentation.services.normative_references')
normative_reference_places = _m_normative_references.normative_reference_places
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
front_matter = _m_plan_file.front_matter
_m_task_kind = import_module('modules.management.task.labels.task_kind')
TaskKind = _m_task_kind.TaskKind
ABSTRACT = Abstract.heading.lower()
FIRST_SECTION = 'first section'
DESCRIPTION_KEY = PracticeKey.DESCRIPTION.key
CONTEXT_READ = 'context_read.txt'
RECORD_SEPARATOR = '\t'
CHANGED_MARK = 'changed since reviewed'
GONE_MARK = 'anchor gone'
DROPPED_MARK = 'dropped'
CHANGED_DO = "Read it as it reads now, and say under the report's Left open: `{located} changed since reviewed; read as it reads now`."
GONE_DO = "Search for its label (`memar content find`, or `memar content search` for where a term occurs), read the section judged to be the one meant, and say under the report's Left open which was read, or that none was."
WHY_LABEL = 'Why: '

class Ref(NamedTuple):
    top: Path
    path: str
    anchor: str = ''
    repository: str = MEMAR_REPOSITORY
    entry: Entry | None = None
    drop: Entry | None = None

class Printed(NamedTuple):
    repository: str
    path: str
    anchor: str
    hash: str

class Composed(NamedTuple):
    blocks: list[str]
    printed: list[Printed]
    listed: int
    changed: int
    gone: int
    dropped: int
    listed_project: int = 0
    dropped_project: int = 0

class _Read(NamedTuple):
    ref: Ref
    header: str
    span: tuple[int, int] | None
    absent: str | None

def _name(ref: Ref, read_at: str='') -> str:
    where = ref.path if ref.repository == MEMAR_REPOSITORY else f'{ref.repository}: {ref.path}'
    if ref.anchor:
        return f'{where}#{ref.anchor}'
    return where if ref.entry is not None else f'{where} ({read_at or ABSTRACT.capitalize()})'

def _header(ref: Ref, mark: str | None=None, read_at: str='') -> str:
    return f'--- {_name(ref, read_at)}' + (f' ({mark})' if mark else '') + ' ---'

def _text_of(ref: Ref, texts: dict[Path, str | None]) -> str | None:
    file = ref.top / ref.path
    if file not in texts:
        texts[file] = read_text(file) if file.is_file() else None
    return texts[file]

def _first_section(text: str) -> tuple[int, int] | None:
    found = outline(text)
    section = next((one for one in found if one.level > 1), None) or (found[0] if found else None)
    return None if section is None else (section.start, section.stop)

def _read(ref: Ref, texts: dict[Path, str | None]) -> _Read:
    text = _text_of(ref, texts)
    if text is None:
        return _Read(ref, _header(ref), None, f'the document {ref.path} is not there in this checkout')
    if ref.entry is not None and (not ref.anchor):
        return _Read(ref, _header(ref), (0, len(text)), None)
    span = span_by_anchor(text, ref.anchor or ABSTRACT)
    if span is None and ref.entry is None and (not ref.anchor):
        span = _first_section(text)
        if span is not None:
            return _Read(ref, _header(ref, read_at=FIRST_SECTION), span, None)
        if _description(text):
            return _Read(ref, '', None, '')
    if span is None:
        return _Read(ref, _header(ref), None, f'no section answers to #{ref.anchor or ABSTRACT} in {ref.path}')
    return _Read(ref, _header(ref), span, None)

def _covered(read: _Read, index: int, every: list[_Read]) -> bool:
    for other_index, other in enumerate(every):
        if other_index == index or (other.ref.top, other.ref.path) != (read.ref.top, read.ref.path) or other.ref.drop:
            continue
        if read.span is None or other.span is None:
            if read.span is None and other.span is None and (other.header == read.header) and (other_index < index):
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
    return (_text_of(read.ref, texts) or '')[read.span[0]:read.span[1]].strip()

def compose(wanted: Sequence[Ref], earlier: Sequence[Ref]=()) -> Composed:
    texts: dict[Path, str | None] = {}
    every = [_read(ref, texts) for ref in (*earlier, *wanted)]
    described = {(read.ref.top, read.ref.path) for read in every[:len(earlier)]}
    blocks: list[str] = []
    printed: list[Printed] = []
    listed = listed_project = changed = gone = dropped = dropped_project = 0
    for index in range(len(earlier), len(every)):
        read = every[index]
        ref, entry = (read.ref, read.ref.entry)
        if _covered(read, index, every):
            continue
        if ref.drop is not None:
            dropped += 1
            dropped_project += not ref.drop.place.is_memar
            blocks.append(f'{_header(ref, DROPPED_MARK)}\ndropped by {ref.drop.located}: {ref.drop.why}')
            continue
        document = (ref.top, ref.path)
        if document not in described:
            described.add(document)
            description = _description(_text_of(ref, texts))
            if description:
                where = ref.path if ref.repository == MEMAR_REPOSITORY else f'{ref.repository}: {ref.path}'
                blocks.append(f'--- {where} (description) ---\n{description}')
        if read.span is None:
            if entry is None:
                if read.absent:
                    blocks.append(f'{read.header}\n{read.absent}')
            else:
                gone += 1
                blocks.append(f"{_header(ref, f'{GONE_MARK}: {entry.located}')}\n{entry.written}\n{read.absent}\n{GONE_DO}")
            continue
        section = _section(read, texts)
        now = section_hash(section)
        printed.append(Printed(ref.repository, ref.path, ref.anchor, now))
        if entry is None:
            blocks.append(f'{read.header}\n{section}')
            continue
        if entry.place.is_memar:
            listed += 1
        else:
            listed_project += 1
        mark = None
        todo = ''
        if entry.reviewed != now:
            changed += 1
            mark = f'{CHANGED_MARK}: {entry.located}'
            todo = CHANGED_DO.format(located=entry.located) + '\n'
        blocks.append(f'{_header(ref, mark)}\n{todo}{WHY_LABEL}{entry.why}\n{section}')
    return Composed(blocks, printed, listed, changed, gone, dropped, listed_project, dropped_project)

def _order(ref: Ref, places: Sequence[Place], texts: dict[Path, str | None]) -> tuple[int, str, float]:
    place = places.index(ref.entry.place) if ref.entry.place in places else len(places)
    text = _text_of(ref, texts)
    span = None if text is None else (0, 0) if not ref.anchor else span_by_anchor(text, ref.anchor)
    return (place, ref.path, float('inf') if span is None else span[0])

def _ref(entry: Entry, drop: Entry | None=None) -> Ref:
    return Ref(entry.top, entry.path or entry.link, entry.anchor, entry.repository, entry, drop)

def _group(found: Sequence[ReferenceList], word: str, places: Sequence[Place], every_act: set, texts) -> list[Ref]:
    entries = [entry for listed in found if listed.word == word for entry in listed.entries]
    drops = {(entry.target, entry.anchor): entry for entry in entries if entry.drops and entry.why and (entry.target is not None)}
    refs = []
    for entry in entries:
        if entry.drops:
            continue
        key = (entry.target, entry.anchor)
        drop = drops.get(key) if key not in every_act else None
        refs.append(_ref(entry, drop))
    return sorted(refs, key=lambda ref: _order(ref, places, texts))

def kind_refs(places: Sequence[Place], kinds: Iterable[TaskKind]) -> list[Ref]:
    found = lists(list(places))
    every_act = {(entry.target, entry.anchor) for listed in found if listed.word == EVERY_ACT for entry in listed.entries if not entry.drops}
    texts: dict[Path, str | None] = {}
    words = list(dict.fromkeys([EVERY_ACT, *(kind.title for kind in kinds)]))
    return [ref for word in words for ref in _group(found, word, places, every_act, texts)]

def _same(refs: Sequence[Ref], record: set[Printed]) -> list[Ref]:
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
    return f'{count} {word}' + ('' if count == 1 else 's')

def first_line(kinds: Sequence[TaskKind], after: Sequence[TaskKind], composed: Composed, left_out: int, project_named: bool, project_places: bool=False, problems: Sequence[str]=()) -> str:
    words = ', '.join((kind.title for kind in kinds)) or 'none'
    parts = [f'kinds: {words}', f"{_plural(composed.listed, 'section')} from Memar's lists" + (f", {composed.listed_project} from this project's" if project_places else '')]
    if after:
        parts.append(f"after {', '.join((kind.title for kind in after))}: {_plural(left_out, 'section')} already printed left out")
    if composed.changed:
        parts.append(f'{composed.changed} {CHANGED_MARK}')
    if composed.gone:
        parts.append(f'{composed.gone} {GONE_MARK}')
    if composed.dropped_project:
        parts.append(f"{_plural(composed.dropped_project, 'passage')} of Memar {DROPPED_MARK} by this project (listed below)")
    if composed.dropped > composed.dropped_project:
        parts.append(f"{_plural(composed.dropped - composed.dropped_project, 'passage')} {DROPPED_MARK} (listed below)")
    parts.extend(problems)
    if not project_named:
        parts.append("no project named, so Memar's lists alone")
    return '; '.join(parts)

def context(places: Sequence[Place], kinds: Sequence[TaskKind], after: Sequence[TaskKind]=(), record: set[Printed] | frozenset=frozenset(), extra: Sequence[Ref]=(), project_named: bool=True, place_problems: Sequence[str]=()) -> Composed:
    earlier = _same(kind_refs(places, after), set(record)) if after else []
    composed = compose([*kind_refs(places, kinds), *extra], earlier)
    project_places = any((not place.is_memar for place in places))
    line = first_line(kinds, after, composed, len(earlier), project_named, project_places, place_problems)
    return composed._replace(blocks=[line, *composed.blocks])

def context_places(checkout: Path, project: Path | None) -> tuple[list[Place], list[str]]:
    declared, problems = normative_reference_places(project, checkout)
    places = [memar_place(checkout)]
    places.extend((place for place in declared if place not in places))
    return (places, problems)

def context_text(places: Sequence[Place], kinds: Sequence[TaskKind], **given) -> str:
    return '\n\n'.join(context(places, kinds, **given).blocks)

def record_path(folder: Path) -> Path:
    return folder / TEMP_FOLDER / CONTEXT_READ

def read_record(folder: Path) -> set[Printed]:
    path = record_path(folder)
    if not path.is_file():
        return set()
    found = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        fields = line.split(RECORD_SEPARATOR)
        if len(fields) == len(Printed._fields):
            found.add(Printed(*fields))
    return found

def write_record(folder: Path, printed: Iterable[Printed]) -> None:
    held = read_record(folder)
    new = [line for line in dict.fromkeys(printed) if line not in held]
    if not new:
        return
    path = record_path(folder)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8', newline='\n') as record:
        for line in new:
            record.write(RECORD_SEPARATOR.join(line) + '\n')
