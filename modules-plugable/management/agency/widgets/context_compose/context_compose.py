#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import hashlib
import re
import subprocess
import sys
_m_set_status = import_module('modules-plugable.knowledge.label.status.services.set_status')
from bundles.memar_adaptor.cli.call_names import call_of_module
_m_status_face = import_module('modules-plugable.knowledge.label.status.services.status_of_thing')
SET_STATUS_LINE = f"memar {call_of_module(_m_status_face.__name__, 'set')} ID WORD --project NAME"
Steps = import_module('modules-plugable.knowledge.documentation.plan.primitive.steps').Steps
from machine.console import called_through_mcp, fail
from machine.console_parts import bound, next_command
from machine.console_parts import part_text as parted
from modules.knowledge.content.services.reference import content_root, read_text
_m_entity = import_module('modules.knowledge.content.primitive.addressable_entity')
AddressableEntity = _m_entity.AddressableEntity
_m_comp = import_module('modules-plugable.management.agency.protocol.composition')
CompositionEntry = _m_comp.CompositionEntry
OrderedComposition = _m_comp.OrderedComposition
CompositionStore = _m_comp.CompositionStore
CompositionVersion = _m_comp.CompositionVersion
TakeupBinding = _m_comp.TakeupBinding
LAYER_STABLE = _m_comp.LAYER_STABLE
DEFAULT_STORE = _m_comp.DEFAULT_STORE
_m_resolve = import_module('modules-plugable.management.agency.services.resolve_composition')
ResolveComposition = _m_resolve.ResolveComposition
_m_bind = import_module('modules-plugable.management.agency.services.bind_takeup')
BindTakeup = _m_bind.BindTakeup
_m_serialize = import_module('modules-plugable.management.agency.widgets.serialize_for_intelligence.serialize_for_intelligence')
SerializeForIntelligence = _m_serialize.SerializeForIntelligence
_m_depends = import_module('modules-plugable.management.task.services.depends')
dependency_refusal = _m_depends.refusal
_m_storage = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage')
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_SENTENCE = _m_temp.TEMP_SENTENCE
_m_ensure = import_module('modules-plugable.management.task.services.ensure')
ensure_task = _m_ensure.ensure_task
from modules.computer.software.edges.manifest.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE, most_characters_preference
registry_of = import_module('modules-plugable.knowledge.documentation.plan.services.plan_registry').registry_of
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
_m_plan_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
_m_plan_acts = import_module('modules-plugable.knowledge.documentation.plan.services.plan_acts')
MODEL_RULE = _m_plan_acts.MODEL_RULE
ACTS = _m_plan_acts.ACTS
act_of = import_module('modules-plugable.knowledge.documentation.plan.services.plan_front').act_of
_m_task_context = import_module('modules-plugable.management.task.services.task_context.task_context')
Composed = _m_task_context.Composed
Ref = _m_task_context.Ref
context = _m_task_context.context
context_places = _m_task_context.context_places
write_record = _m_task_context.write_record
_m_acts = import_module('modules.management.agency.labels.acts')
Acts = _m_acts.Acts
from modules.computer.software.primitive.project_name import ProjectName
from modules.computer.software.primitive.project_path import ProjectPath
from modules.process.service.primitive.call_name import call_name
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
START_COMMAND = 'get-task-init-context'
commands = import_module('bundles.memar_adaptor.cli.services.commands')
MOST_NAMED_COMMANDS = 8
HELP_TIMEOUT_SECONDS = 60
STEP_DOCUMENT = re.compile('(?<![\\w./-])/?((?:docs|modules|modules-plugable|bundles|\\.agents)/[\\w./-]+?\\.md)(?:#([\\w-]+))?')
NAMED_COMMAND = re.compile('`memar ([^`]+)`')
COMMAND_WORD = re.compile('[a-z][a-z0-9_-]*$')
MOST_COMMAND_WORDS = 3
MARK = '==='
ALWAYS_HELP = (('task_ensure',), ('conversation_post',), ('content_write',))
CARD_LISTS_VERBS = ()
CARD_POINTER = 'Its verbs, each with its call shape, are on the card above (`=== commands ===`).'
ENDING = f"Do what the plan's Request says, without rewriting that Request. A read-only step takes no development or modeling act, so beyond what this prints it reads only what its step needs.\nEnd with a report content (kind report) and Status: post the report through `memar conversation_post --timeline ID --kind report` with the text on standard input (or the verb's `text`), or `--content-file SCRATCHFILE` only under the project's `{_m_temp.TEMP_FOLDER}/` scratch root — never under `.agents/` and never as `.agents/tmp_*` — then set Status with `{SET_STATUS_LINE}`. Where you may only return text, return the report as your final text, and the delegating task posts it as kind report and sets Status before its next step.\n{TEMP_SENTENCE}\n- A text of a task is added as a new content with `memar conversation_post`, never written over; the current plan is the latest content of kind plan and the current report the latest of kind report; read them with `memar git_show_task_records` (by kind); a fact of a task (status, title, …) is changed through its task verbs, never by naming a facts filename."

class _Storage:

    def is_task(self, task_id: str) -> bool:
        return _m_storage.is_task_folder(task_id)

    def has_plan(self, task_id: str) -> bool:
        return _m_storage.has_plan(task_id)

    def plan_path(self, task_id: str):
        return _m_storage.plan_path(task_id)

    def report_path(self, task_id: str):
        return _m_storage.report_path(task_id)

    def plan_text(self, task_id: str) -> str:
        return _m_storage.plan_text(task_id)

    def plan_front(self, task_id: str):
        return _m_storage.plan_front(task_id)

    def tree_names(self, task_id: str) -> list[str]:
        return _m_storage.tree_names(task_id)

    def project_named(self, task_id: str):
        return _m_storage.project_named(task_id)

    def skill_relative(self):
        _m_fs = import_module('bundles.memar.services.location.memar_location')
        return (_m_fs.SKILL_RELATIVE / 'SKILL.md').as_posix()

    def skill_text(self, root) -> str:
        return read_text(root / self.skill_relative())

    def content_root(self):
        return content_root()

    def help_of(self, words: tuple[str, ...]) -> str | None:
        try:
            done = subprocess.run([*import_module('bundles.memar.services.location.memar_location').program(), *words, '--help'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=HELP_TIMEOUT_SECONDS)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else None

_storage = _Storage()

def marked_part(name: str, body: str) -> str:
    return marked_passages(name, [body])[0]

def marked_passages(name: str, blocks: list[str]) -> list[str]:
    kept = [block.strip() for block in blocks if block.strip()] or ['']
    kept[0] = f'{MARK} {name} {MARK}\n{kept[0]}'
    return [block + '\n' for block in kept]

def _task_part(task_id: str) -> str:
    return marked_part('task', f'task_id: {task_id}\nplan: (latest content of kind plan)\nreport: (latest content of kind report)')

def model_part(kind: str) -> str:
    rule = f'The model a task runs on follows what it needs, not its kind alone: the rule is {MODEL_RULE} (`memar content_resolve_path {MODEL_RULE}` gives its path); the plan states the facts it reads.'
    too_weak = 'If you judge your reasoning too weak for this task, write that and why in its report, name the level you ran at and what it lacked, end Blocked, and ask for another agent one level above to take it up.'
    if kind in Acts.titles():
        body = f'kind: {kind}\n{rule} The kind is its starting point. {too_weak}'
    elif kind:
        body = f"kind: {kind}\n{kind!r} is not a kind; the kinds are {', '.join(ACTS)}. End Blocked saying so, for the task that handed you the task to correct it."
    else:
        body = f'kind: the plan states no kind.\n{rule} Determine the act from the work and fetch its required context before acting. {too_weak}'
    return marked_part('model', body)

def _folder_part(task_id: str) -> str:
    lines = _storage.tree_names(task_id)
    return marked_part('folder', '\n'.join(lines) if lines else '(no files on the records branch)')

def _heading_part(text: str, part: str) -> str:
    found: list[str] | None = None
    for line in text.splitlines():
        if line.startswith('## '):
            if found is not None:
                break
            if line[3:].strip() == part:
                found = []
        elif found is not None:
            found.append(line)
    return '\n'.join(found or []).strip()

def step_documents(root, steps: str) -> list:
    found = []
    for path, anchor in STEP_DOCUMENT.findall(steps):
        ref = Ref(root, path, anchor)
        if ref not in found:
            found.append(ref)
    return found

def documents(root, kinds: list, named: list, project) -> Composed:
    places, problems = context_places(root, project)
    return context(places, kinds, extra=named, project_named=project is not None, place_problems=problems)

def documents_bootstrap(kind: str, composed: Composed) -> str:
    if kind in Acts.titles():
        head = f'kinds: {kind}; index only — bodies are not dumped in init'
    elif kind:
        head = f'kinds: {kind!r} is not a kind; index only — bodies are not dumped in init'
    else:
        head = 'kinds: none; index only — bodies are not dumped in init'
    paths: list[str] = []
    for printed in composed.printed:
        paths.append(f'{printed.path}#{printed.anchor}' if printed.anchor else printed.path)
    fetch = 'Fetch act passages with `memar content_get_act_context --kind K` when the act begins; per step call `memar ai_get_rules_for_subject` with the subject. Do not treat this init as the normative dump.'
    index = '\n'.join(paths) if paths else '(no index entries)'
    return marked_part('documents', f'{head}\n{fetch}\nIndex:\n{index}')

def _kinds(kind: str) -> list:
    found = Acts.read(kind)
    return [found] if found else []

def named_commands(plan: str) -> list[tuple[str, ...]]:
    found: list[tuple[str, ...]] = []
    for text in NAMED_COMMAND.findall(plan):
        words: list[str] = []
        for word in text.split():
            if not COMMAND_WORD.match(word) or len(words) == MOST_COMMAND_WORDS:
                break
            words.append(word)
        command = tuple(words)
        if command and command not in found and (command not in ALWAYS_HELP):
            found.append(command)
    return found

def _help_of(words: tuple[str, ...]) -> str | None:
    return _storage.help_of(_flat_words(words))

def _flat_words(words: tuple[str, ...]) -> tuple[str, ...]:
    """Replace a leading legacy command path with its flat parser name, retaining extras."""
    if len(words) == 1 and '_' in words[0]:
        return words
    legacy = words[:2] if len(words) > 1 else ('Memar', words[0])
    class LegacyDetails:
        def Domain(self):
            return legacy[0]

        def Name(self):
            return legacy[1]

    return (call_name(LegacyDetails()), *words[2:])

def _help_part(plan: str) -> list[str]:
    named = named_commands(plan)
    shown, left = (named[:MOST_NAMED_COMMANDS], named[MOST_NAMED_COMMANDS:])
    blocks = []
    for words in (*ALWAYS_HELP, *shown):
        words = _flat_words(words)
        command = 'memar ' + ' '.join(words)
        found = _help_of(words)
        if found is not None and words in CARD_LISTS_VERBS:
            found = found.split('\noptions:', 1)[0].rstrip() + '\n\n' + CARD_POINTER
        blocks.append(f'--- `{command} --help` ---\n' + (found if found is not None else f'no such command: `{command}`'))
    if left:
        blocks.append('--- not printed ---\n' + '\n'.join((f"`memar {' '.join(words)}`: ask `--help` of it" for words in left)))
    return marked_passages('help', blocks)

def plan_project(task_id: str):
    return _storage.project_named(task_id)

def _plan_front(plan: str, project) -> dict[str, str]:
    front, _ = _m_plan_text.front_matter(plan.splitlines())
    current = _m_plan_record.PLAN.current({
        key.lower(): value
        for key, value in (front or {}).items()
        if key == _m_plan_text.front_key(key)
    })
    if project is not None:
        current[_m_plan_key.PlanKey.PROJECT.key] = str(project)
    return current

def _mark_of(text: str) -> bytes:
    return hashlib.sha256(text.encode('utf-8')).digest()

def _stable_entries(composed: Composed, with_skill: bool, skill_relative: str) -> list[CompositionEntry]:
    entries: list[CompositionEntry] = []
    if with_skill:
        entries.append(CompositionEntry(AddressableEntity.of(skill_relative, ''), LAYER_STABLE, _mark_of(skill_relative)))
    for printed in composed.printed:
        entries.append(CompositionEntry(AddressableEntity.of(printed.path, printed.anchor), LAYER_STABLE, _mark_of(printed.hash)))
    return entries

class ContextCompose:

    def __init__(self, storage: _Storage | None=None, composition_store: CompositionStore | None=None, resolve: ResolveComposition | None=None, bind: BindTakeup | None=None, prefix_cache=None, durable_kv=None) -> None:
        self.storage = storage or _storage
        self.composition_store = composition_store or DEFAULT_STORE
        self.resolve = resolve or ResolveComposition(self.composition_store)
        self.bind = bind or BindTakeup(self.composition_store, self.resolve)
        self.prefix_cache = prefix_cache
        self.durable_kv = durable_kv

    def bind_and_resolve_entries(self, principal: str, version: CompositionVersion) -> tuple[OrderedComposition | None, TakeupBinding | None, str | None]:
        binding, err = self.bind.bind(principal, version, None, False)
        if err or binding is None:
            return (None, None, err)
        ordered, err = self.resolve.resolve(version)
        if err or ordered is None:
            return (None, binding, err)
        return (ordered, binding, None)

    def serialize_for(self, binding: TakeupBinding, body_of=None, include_session: bool=False) -> tuple[bytes, bytes, bytes, str | None]:
        serialize = SerializeForIntelligence(self.resolve, body_of=body_of, prefix_cache=self.prefix_cache, durable_kv=self.durable_kv)
        return serialize.serialize(binding, include_session=include_session)

    def compose(self, task_id: str, with_skill: bool=True) -> list[str]:
        store = self.storage
        if not store.is_task(task_id) or not store.has_plan(task_id):
            fail(f'no task to start in {task_id}: it has no plan on its timeline. Open it with `memar task_ensure --title T --parent ID {ProjectName.FLAG} {ProjectName.METAVAR}` (or `{ProjectPath.FLAG} {ProjectPath.METAVAR}`), ID the task handing it over, and post its plan with `memar conversation_post --kind plan` first')
        unmet = dependency_refusal(task_id, 'start')
        if unmet:
            fail(unmet)
        ensure_task(task_id)
        plan = store.plan_text(task_id)
        front = _plan_front(plan, store.project_named(task_id))
        kind = act_of(front, registry_of(front))
        root = store.content_root()
        composed = documents(root, _kinds(kind), step_documents(root, _heading_part(plan, Steps.heading)), store.project_named(task_id))
        write_record(task_id, composed.printed)
        skill_relative = store.skill_relative()
        version = self.composition_store.put(OrderedComposition(_stable_entries(composed, with_skill, skill_relative)))
        ordered, _binding, err = self.bind_and_resolve_entries(task_id, version)
        if err or ordered is None:
            fail(err or 'ResolveComposition refused the takeup composition')
        expected = ([skill_relative] if with_skill else []) + [printed.path for printed in composed.printed]
        if [entry.locator.document for entry in ordered.entries] != expected:
            fail('ResolveComposition returned a different Stable order than Bind stored')
        passages = [_task_part(task_id), model_part(kind), marked_part('plan', plan), _folder_part(task_id), *([marked_part('skill', store.skill_text(root))] if with_skill else []), documents_bootstrap(kind, composed), *([] if called_through_mcp() else [marked_part('commands', commands.card_text()), *_help_part(plan)]), marked_part('ending', ENDING)]
        return [passage + '\n' for passage in passages[:-1]] + passages[-1:]

def start_passages(task_id: str, with_skill: bool=True) -> list[str]:
    return ContextCompose().compose(task_id, with_skill)

def start_text(task_id: str, with_skill: bool=True) -> str:
    return ''.join(start_passages(task_id, with_skill))

def get_task_init_context(task_id: str, with_skill: bool=True, part: int=1, most: int | None=None) -> None:
    words = ['memar', *_flat_words(('agency', START_COMMAND)), TaskId.FLAG, task_id, *([] if with_skill else ['--without-skill'])]
    passages = start_passages(task_id, with_skill)
    limit = bound(most, most_characters_preference(plan_project(task_id)))
    sys.stdout.write(parted(passages, part, limit, next_command(words, most)))

SKILL_FILE = _storage.skill_relative()


def task_init_context(*, task_id: str, without_skill: bool = False, part: int = 1, most_characters: int | None = None) -> None:
    get_task_init_context(task_id, not without_skill, part, most_characters)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_init_context,
        name=START_COMMAND,
        summary='print, in one output, everything an agent taking up a task needs in its context',
        description=f"""For every agent that takes up a task: a sub-agent handed one, and the agent of a task after\n`ensure` opened its own. Print, in parts each opened by a line `=== NAME ===`, and in this\norder: the task's id, the model its Kind needs, its plan (latest content of kind plan), the\nfolder's listing, the Memar skill, the passages of Memar's documents the plan's Kind requires\n(as `memar content_get_act_context --kind K` prints them; the core alone for a plan with no\nKind) and then the documents the plan's Steps name that those do not hold, the help of the\ncommands every task uses and those the plan names, and how to end. Run it first, once, and\nread nothing else before acting on the plan.\n\nA text too long for one tool output prints in ordered parts, each at most --most-characters\nlong: each part but the last ends with the exact command for the next (--part N), to run\nat once; read every part before acting. The same task prints the same parts, and each\npart says "part N of M of text H", H a hash of the whole text: a part naming another H\nis of another version of it.\n\nThe kinds a plan carries: {', '.join(ACTS)}.\n\nA task holds contents: its plan is its latest content of kind plan and its report its latest\nof kind report; a new plan or report is added with `memar conversation_post`, never written\nover. Read them with `memar git_show_task_records` (by kind). Facts change through task verbs\n(`{SET_STATUS_LINE}`, …).\n\nIt is `task_ensure --task-id ID` as well, so the role folders are there after it; it opens no new\ntask, and refuses an ID that has no plan on its timeline.""",
        help={'task_id': 'the task handed to you', 'without_skill': 'leave the Memar skill out, for an agent whose runtime already loaded it', 'part': 'print part N of a text too long for one output; each part names the command for the next', 'most_characters': 'the most characters one part holds; when not given, the preference of the project the plan names, else the default below the smallest output cut known among the runtimes in use'},
    ),
)
