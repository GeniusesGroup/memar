#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/plan_labels.py — a plan's labels: the kinds a plan carries, the project's label registry, and writing one label in place.

A plan's `Labels` are the words that link it to other tasks outside the
structure of their ids (`modules/knowledge/documentation/primitive/label.py`),
each written with its identifier, `design(01a14a04-...)`. A label is defined
once and its definition takes labels: `design` takes `TaskKind`, a topic takes
`Topic`. The closed kinds (`TaskKind`, in `modules/knowledge/documentation/plan/labels/task_kind.py`) define their
words in code; the free kind (`Topic`, in `modules/knowledge/documentation/plan/labels/topic.py`) lists none, and
each of its words is declared as code by the domain whose it is, found in the
project's tree (`declarations.py`), so every clone reads one identifier for
one label and a plain search for the identifier finds every plan that took it.
A word nobody declared is refused with the declaration to write and the
declared words near it: a new subject is a decision written where it belongs,
with its meaning, and a typo is caught before it splits one subject in two.
This file gathers the kinds a plan carries and adds none of its own. A plan
takes as many labels as it needs and none it does not: a label is added only
when another task is to be found by it.

The rule `start` applies to say how able an agent a kind needs is transitional,
with its reason below, until the plan names its own AI (the Labels design's
`AIModel`, its own field, not done here).

A label is written one line at a time, as a priority is, through
`task_plan_rewrite`: the block under the key is found, the label's line added
or removed, and every other line kept as written.
"""
from __future__ import annotations
import time
from pathlib import Path
from machine.console import fail
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.label import FLAG_SEPARATOR, Label, LabelDefinition, LabelProblem, LabelRegistry, Labels
from modules.knowledge.documentation.plan.labels import task_kind, topic
from modules.knowledge.documentation.plan.labels.task_kind import TaskKind
from modules.knowledge.documentation.plan.services.plan import front_matter
from modules.knowledge.documentation.plan.services.rewrite import key_of, line_end, rewrite
from modules.knowledge.label.services.declarations import FOLDER, NAME, Declared, declared, declaring_files
KINDS = (task_kind.LABEL_KIND, topic.LABEL_KIND)
TASK_KIND = task_kind.LABEL_KIND_NAME
TOPIC = topic.LABEL_KIND_NAME
TASK_KINDS = TaskKind.words(carried=True)
CHEAPER_KINDS = (TaskKind.MECHANICAL.word,)
STRONG_KINDS = tuple((word for word in TaskKind.words() if word not in CHEAPER_KINDS))
NEAR_EDITS = 2
RECHECK_SECONDS = 2.0
_cache: dict[str, tuple[LabelRegistry, tuple[Declared, ...], tuple[tuple[str, float], ...], float]] = {}

def kinds_listing() -> str:
    """The kinds a plan carries as one line for a help text, e.g. `TaskKind, Topic`."""
    return ', '.join((kind.name for kind in KINDS))

def _stamp(project: Path) -> tuple[tuple[str, float], ...]:
    """What PROJECT's declarations are now: each declaring file with its modification time."""
    return tuple(((str(path), path.stat().st_mtime) for path in declaring_files(project))) if project.is_dir() else ()

def _known(project: Path | None) -> tuple[LabelRegistry, tuple[Declared, ...]]:
    """PROJECT's registry and declarations, read again when a declaring file changed.

    The walk is checked at most once every `RECHECK_SECONDS`, so one command
    that reads many plans walks once, and a process that serves many commands
    (the resident one) still sees a declaration written between two of them.
    """
    if project is None:
        return (LabelRegistry(KINDS), ())
    key = str(project)
    now = time.monotonic()
    held = _cache.get(key)
    if held is not None and now - held[3] < RECHECK_SECONDS:
        return (held[0], held[1])
    stamp = _stamp(project)
    if held is None or held[2] != stamp:
        found = declared(project) if stamp else ()
        held = (LabelRegistry(KINDS, (item.definition for item in found)), found, stamp, now)
    _cache[key] = (held[0], held[1], held[2], now)
    return (held[0], held[1])

def registry_for(project: Path | None) -> LabelRegistry:
    """The label registry of PROJECT for this run: the kinds' own definitions and those its domains declare; the kinds alone without a project."""
    return _known(project)[0]

def declarations_of(project: Path | None) -> tuple[Declared, ...]:
    """The labels PROJECT's domains declare, each with its file."""
    return _known(project)[1]

def forget() -> None:
    """Read the declarations again on the next call, without waiting `RECHECK_SECONDS`: for a run that has just written one."""
    _cache.clear()

def project_of(front: dict[str, str] | None) -> Path | None:
    """The project FRONT matter names, or None."""
    named = (front or {}).get(PlanKey.PROJECT.key, '').strip()
    return Path(named) if named else None

def registry_of(front: dict[str, str] | None) -> LabelRegistry:
    """The registry of the project a plan's FRONT matter names."""
    return registry_for(project_of(front))

def labels_of(front: dict[str, str] | None) -> Labels:
    """The labels FRONT matter gives its plan, as written; none when it has none. They are not checked: a plan is edited by hand."""
    return Labels.read((front or {}).get(PlanKey.LABELS.key, ''))

def topics_of(front: dict[str, str] | None) -> tuple[str, ...]:
    """The words of the topics FRONT matter gives its plan, in the order written."""
    return registry_of(front).words(labels_of(front), TOPIC)

def task_kind_of(front: dict[str, str] | None) -> str:
    """The task kind FRONT matter gives its plan, lower case as written; empty when it has none.

    A plan with several task kinds is read as its first judgment kind, so that
    a task that is also mechanical is not moved to a cheaper model.
    """
    words = [word.strip().lower() for word in registry_of(front).words(labels_of(front), TASK_KIND)]
    return next((word for word in words if word in STRONG_KINDS), words[0] if words else '')

def edit_distance(one: str, two: str) -> int:
    """How many single-character insertions, deletions, or substitutions turn ONE into TWO."""
    previous = list(range(len(two) + 1))
    for row, first in enumerate(one, 1):
        current = [row]
        for column, second in enumerate(two, 1):
            current.append(min(previous[column] + 1, current[column - 1] + 1, previous[column - 1] + (first != second)))
        previous = current
    return previous[-1]

def near_words(word: str, kind: str, registry: LabelRegistry) -> list[str]:
    """The words REGISTRY defines under the kind named KIND within `NEAR_EDITS` of WORD, ended ones left out."""
    return sorted((definition.label.word for definition in registry.definitions(kind) if not definition.ended and edit_distance(word, definition.label.word) <= NEAR_EDITS))

def undeclared(fresh: LabelDefinition, kind: str, project: Path | None, registry: LabelRegistry) -> str:
    """What is said of a word of the free kind KIND that PROJECT does not declare: where it is declared, the declaration to write, and the declared words near it."""
    word = fresh.label.word
    said = f"{kind} {word!r} is declared by no module of this project; a {kind} is code, declared by the domain whose it is: by the module it names, or, for a stream of work, by the task domain. Write it in a Python file of that module's `{FOLDER}/` folder, in its `{NAME}` tuple: {kind.lower()}({word!r}, {fresh.label.id!r}, '<one sentence: what work it names>'), then label the task"
    files = sorted({str(item.source.relative_to(project)) if project else str(item.source) for item in declarations_of(project) if item.definition.is_a(registry.kinds[kind].label)})
    if files:
        said += f"; this project declares its {kind} labels in {', '.join(files)}"
    near = near_words(word, kind, registry)
    if near:
        said += f"; near it: {', '.join(near)} — if it is one of them, use that one"
    return said

def checked_label(text: str, project: Path | None, registry: LabelRegistry | None=None) -> Label:
    """TEXT, `KIND=WORD`, as a label a plan in PROJECT may take: refused with the kind's words when it is none, with the declaration to write when its word is declared nowhere, and with what replaced it when it has ended."""
    registry = registry or registry_for(project)
    try:
        label, fresh = registry.resolve(text)
    except LabelProblem as problem:
        fail(str(problem))
    kind = text.partition(FLAG_SEPARATOR)[0].strip()
    if fresh is not None:
        fail(undeclared(fresh, kind, project, registry))
    definition = registry.definition(label)
    if definition is not None and definition.ended:
        instead = ', '.join((item.word for item in definition.replaced_by)) or 'none named'
        fail(f'{kind} {label.word} ended on {definition.ended}; it is taken by no new task. In its place: {instead}')
    return label

def label_to_remove(text: str, project: Path | None, carried: Labels) -> Label | None:
    """TEXT, `KIND=WORD`, as the label to take out of a plan carrying CARRIED: the declared one, or else the one carried under that word; None when the plan carries no such word. Refused only when TEXT is no label of a kind a plan carries."""
    try:
        label, fresh = registry_for(project).resolve(text)
    except LabelProblem as problem:
        fail(str(problem))
    if fresh is None:
        return label
    return next((item for item in carried if item.word == fresh.label.word), None)

def _block(lines: list[str], start: int) -> tuple[int, int] | None:
    """Where the `Labels:` block lies among the front matter's LINES (before START): the header's index and the index after its last line; None without one."""
    for index in range(1, start - 1):
        if key_of(lines[index]) == PlanKey.LABELS.written and lines[index].split(':', 1)[1].strip() == '':
            end = index + 1
            while end < start - 1 and lines[end][:1] in (' ', '\t'):
                end += 1
            return (index, end)
    return None

def _written(labels: Labels, newline: str) -> list[str]:
    return [f'{PlanKey.LABELS.written}:{newline}', *(f'{line}{newline}' for line in labels.lines())] if labels else []

def _change(path: Path, edit) -> None:
    """Rewrite PATH's labels as EDIT makes them from the ones it holds; every other line is kept."""

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its labels cannot be set')
        newline = line_end(lines[0])
        found = _block(lines, start)
        was = Labels.read('\n'.join((line.strip() for line in lines[found[0] + 1:found[1]]))) if found else Labels()
        written = _written(edit(was), newline)
        if found:
            return [*lines[:found[0]], *written, *lines[found[1]:]]
        return [*lines[:start - 1], *written, *lines[start - 1:]]
    rewrite(path, change)

def add_label(path: Path, label: Label) -> None:
    """Add LABEL to PATH's labels, last; unchanged when the plan already carries it. LABEL has been checked (`checked_label`)."""
    _change(path, lambda was: was.with_label(label))

def remove_label(path: Path, label: Label) -> None:
    """Remove LABEL from PATH's labels, the block with the last one; unchanged when the plan does not carry it."""
    _change(path, lambda was: was.without(label))
