#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/archive_task_records.py — a session's records kept on a branch of its project's repository.

A live session folder is scratch: it is swept once its task is done, and it
holds a claim that means nothing on another clone. Its record is not scratch:
changelogs and handoffs cite session ids, and a cited id whose folder the sweep
has sent to the trash cites nothing. So the two are two concerns with two
locations: the folder stays where it is and goes as it
always went, and its records are kept in the project's own repository, on the
branch `fs_memar.RECORDS_BRANCH` names, at
`.agents/tasks/<id>/` in that branch's tree. A branch, because the full
records would otherwise grow the history of the work; a branch of the project's
own repository, because that is where the project's people already are, and
nothing is pushed: publishing the branch is the owner's act. What is kept is
read by id (`session_show`) and by content: `memar content find` and `search`
read the branch with `--from sessions` (owner, 2026-10-19), so a later session
can find what an earlier one wrote.

**What is kept.** The whole folder (`session_keep`), except the claim, caches,
a path with a `.git` part, binary files, a non-document file over 256 KB, and
the session's own `temp` folder. The plan is kept naming its project by the
project's registered name rather than by the path it has on the computer that
opened it, which means nothing elsewhere (`memar project find` turns the name
into this computer's path); every other byte is kept as written. The commit's
message lists each leave-out with its size and reason.

**Who may have records.** Every project, unless its preferences say
`records: off` (`project_preferences`); a project must be a git repository and
must have a registered name. What cannot be kept — a project folder not on this
computer, no registered name, a `records` value it may not take, a project that
is no repository or has the records branch checked out, a commit that fails —
is refused with why, and the caller that would move the folder leaves it where
it is: a record dropped without a word is the defect this file exists to end. A
folder with no plan, or a plan naming no project, has no project to keep
anything in, and owes nothing.

**Archived.** A session is archived when the branch holds, for every file
keeping it now would write, the same bytes (`standing`): a change in a kept file
after archiving makes it not archived until it is archived again, and a change in
`temp` does not. `close` acts only on an archived session; the sweep archives
before it trashes (`session_close`, `session_gc`).

`archive` is the verb a coordinator runs before committing a task: it keeps the
records of the session named and of every session whose Parent chain leads to it
— the sessions it handed work to — in one commit, and prints where each one's
records are, so they are named in the commit of the work. Keeping again writes
what the folder holds now, drops what it no longer holds, and makes no commit
when nothing changed. A session any of them cannot be kept stops the verb before
anything is written.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
scratch_root = _m_fs_memar.scratch_root
import argparse
import os
import tempfile
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, NamedTuple
from machine.console import fail, note
from . import branch as session_branch
from modules.process.project.services.preferences import RECORDS_KEY, Records, preferences_path, read_preferences, records_preference
from modules.process.project.services.registry import read_entries
from .branch import RecordRefused, folder_on_branch, reference
from modules.management.task.services.folder import Session, folder_of, read_session, session_folders
from .keep import KEEP_LIMIT_BYTES, Left, Selection, select
from modules.process.project.services.task_location import same_path
from .log import record
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.report.services.report import REPORT_NAME
from modules.management.task.services.temp import TEMP_FOLDER
ARCHIVE_COMMAND = 'archive-task-records'

class Outcome(Enum):
    """How keeping one session's records ended."""
    KEPT = 'kept'
    NOT_OWED = 'not owed'
    REFUSED = 'refused'

class Kept(NamedTuple):
    """One session's keeping: how it ended, where its records are when kept, why when not, the files kept, and the branch's tip after."""
    outcome: Outcome
    reference: str | None
    why: str = ''
    files: tuple[str, ...] = ()
    commit: str | None = None

class State(Enum):
    """Whether a session's records are on the branch as keeping would write them now."""
    ARCHIVED = 'archived'
    WAITING = 'not archived'
    NOT_OWED = 'not owed'
    REFUSED = 'refused'

class Standing(NamedTuple):
    """A session's State, and why when it is not owed or refused."""
    state: State
    why: str = ''

class Owed(NamedTuple):
    """A session whose records are owed: its folder, its id, its project, the project's registered name, and what keeping takes."""
    folder: Path
    project: Path
    name: str
    selection: Selection

def _project_of(session: Session) -> str:
    return (session.front or {}).get(PlanKey.PROJECT.key, '').strip()

def project_name(project: Path) -> str | None:
    """PROJECT's own registered name, the first on its entry; None when it has no entry."""
    entry = next((each for each in read_entries() if same_path(each.path, project)), None)
    return entry.names[0] if entry is not None and entry.names else None

def _named_plan(data: bytes, name: str) -> bytes:
    """The plan bytes DATA with its front matter's Project value replaced by NAME, every other byte as written."""
    lines = data.decode('utf-8-sig').splitlines(keepends=True)
    key = f'{PlanKey.PROJECT.written}:'
    if lines and lines[0].strip() == '---':
        for index in range(1, len(lines)):
            line = lines[index]
            if line.strip() == '---':
                break
            if line.startswith(key):
                ending = line[len(line.rstrip('\r\n')):]
                lines[index] = f'{key} {name}{ending}'
                break
    return ''.join(lines).encode('utf-8')

def owed(folder: Path) -> Owed | Kept:
    """What keeping FOLDER's records takes, or the Kept that says they are not owed or cannot be kept."""
    session = read_session(folder)
    if not session.has_plan:
        return Kept(Outcome.NOT_OWED, None, f'it has no {PLAN_NAME}')
    if not session.readable or session.front is None:
        return Kept(Outcome.REFUSED, None, f'its {PLAN_NAME} cannot be read, so its project is not known')
    named = _project_of(session)
    if not named:
        return Kept(Outcome.NOT_OWED, None, f'its {PLAN_NAME} names no project to keep its records in')
    project = Path(named)
    if not project.is_dir():
        return Kept(Outcome.REFUSED, None, f'its project {named} is not a folder on this computer')
    preference = records_preference(project)
    if preference is None:
        return Kept(Outcome.REFUSED, None, f"`{RECORDS_KEY}: {read_preferences(project).get(RECORDS_KEY, '')}` in {preferences_path(project)} is none of {Records.listing()}, or empty")
    if preference is Records.OFF:
        return Kept(Outcome.NOT_OWED, None, f"its project's preferences say `{RECORDS_KEY}: {Records.OFF.value}`")
    name = project_name(project)
    if name is None:
        return Kept(Outcome.REFUSED, None, f'its project {project} has no registered name to write in the kept plan; give it one with `memar project add`')
    if not session_branch.is_repository(project):
        return Kept(Outcome.REFUSED, None, f"its project {project} is not the top folder of a git repository, and its records are kept on the branch {RECORDS_BRANCH} of the project's own repository")
    if session_branch.is_checked_out(project):
        return Kept(Outcome.REFUSED, None, f'the branch {RECORDS_BRANCH} is the branch checked out in {project}; the records branch is never worked on, so check out another')
    return Owed(folder, project, name, select(folder))

def _entries(owing: Owed, workdir: Path) -> dict[str, Path]:
    """The branch path and the source file of each file keeping OWING writes; the plan is a copy in WORKDIR naming its project."""
    sid = owing.folder.name
    entries: dict[str, Path] = {}
    for relative in owing.selection.kept:
        source = owing.folder / relative
        if relative == PLAN_NAME:
            named = workdir / sid / PLAN_NAME
            named.parent.mkdir(parents=True, exist_ok=True)
            named.write_bytes(_named_plan(source.read_bytes(), owing.name))
            source = named
        entries[f'{folder_on_branch(sid)}/{relative}'] = source
    return entries

def standing(folder: Path) -> Standing:
    """Whether FOLDER's records are on the branch as keeping them now would write them; nothing is written."""
    judged = owed(folder)
    if isinstance(judged, Kept):
        return Standing(State.NOT_OWED if judged.outcome is Outcome.NOT_OWED else State.REFUSED, judged.why)
    with tempfile.TemporaryDirectory(dir=scratch_root(), prefix='archive-') as workdir:
        entries = _entries(judged, Path(workdir))
        sources = list(entries.values())
        ids = session_branch.blob_ids(judged.project, sources)
        have = session_branch.held(judged.project, folder.name)
        prefix = folder_on_branch(folder.name) + '/'
        same = all((have.get(target.removeprefix(prefix)) == blob for target, blob in zip(entries, ids)))
    return Standing(State.ARCHIVED if same else State.WAITING)

def _size(size: int) -> str:
    return f'{size} bytes'

def _left_line(left: Left) -> str:
    held = f'{left.files} files, ' if left.files != 1 else ''
    return f'  {left.path} ({held}{_size(left.size)}): {left.reason.sentence}'

def _message(group: list[Owed]) -> str:
    """The commit message for GROUP's sessions: their ids, then each leave-out with its size and reason."""
    ids = ', '.join((each.folder.name for each in group))
    lines = [f"Record {('session' if len(group) == 1 else 'sessions')} {ids}", '']
    for each in group:
        if each.selection.left:
            lines.append(f'Left out of {each.folder.name}:')
            lines.extend((_left_line(left) for left in each.selection.left))
            lines.append('')
    lines.append(f'Kept whole except what is listed: files over {KEEP_LIMIT_BYTES // 1024} KB are left out unless they are documents.')
    return '\n'.join(lines) + '\n'

def keep_records(folders: Iterable[Path], *, write: bool=True) -> list[Kept]:
    """Keep the records of FOLDERS on their projects' branches, one commit for each project's sessions; one Kept for each folder, in order.

    A project's sessions are committed together, and a session that is not
    owed or cannot be kept does not hold the others back. Unless WRITE, nothing
    is written, and what would be is returned: a dry run.
    """
    folders = list(folders)
    outcomes: list[Kept | None] = [None] * len(folders)
    groups: dict[str, list[tuple[int, Owed]]] = {}
    for index, folder in enumerate(folders):
        judged = owed(folder)
        if isinstance(judged, Kept):
            outcomes[index] = judged
        else:
            groups.setdefault(os.path.normcase(str(judged.project.resolve())), []).append((index, judged))
    with tempfile.TemporaryDirectory(dir=scratch_root(), prefix='archive-') as workdir:
        for number, members in enumerate(groups.values()):
            project = members[0][1].project
            group = [owing for _, owing in members]
            if not write:
                for index, owing in members:
                    outcomes[index] = Kept(Outcome.KEPT, reference(owing.folder.name), files=owing.selection.kept)
                continue
            scratch = Path(workdir) / str(number)
            scratch.mkdir()
            entries: dict[str, Path] = {}
            for owing in group:
                entries.update(_entries(owing, scratch))
            try:
                tip = session_branch.record(project, entries, [folder_on_branch(owing.folder.name) for owing in group], _message(group), scratch)
            except RecordRefused as error:
                for index, owing in members:
                    outcomes[index] = Kept(Outcome.REFUSED, None, f'its records could not be written to {RECORDS_BRANCH} of {project} ({error})')
                continue
            for index, owing in members:
                outcomes[index] = Kept(Outcome.KEPT, reference(owing.folder.name), files=owing.selection.kept, commit=tip)
                record('recorded', owing.folder.name, reference(owing.folder.name), folder=owing.folder)
    return [each for each in outcomes if each is not None]

def related_sessions(folder: Path) -> list[Path]:
    """FOLDER and every session folder whose Parent chain leads to it, FOLDER first, each once."""
    children: dict[str, list[Path]] = {}
    for entry in session_folders(projects=True):
        parent = read_session(entry).parent
        if parent:
            children.setdefault(parent, []).append(entry)
    found = [folder]
    for each in found:
        for child in children.get(each.name, []):
            if all((child.resolve() != known.resolve() for known in found)):
                found.append(child)
    return found

def archive(task_id: str) -> None:
    """`archive`: keep the records of TASK_ID and of the sessions it handed work to in one commit, and say where each is."""
    folder = folder_of(task_id)
    if not folder.is_dir():
        fail(f'no session folder {task_id} was found')
    related = related_sessions(folder)
    refused = [(each.name, kept.why) for each, kept in zip(related, keep_records(related, write=False)) if kept.outcome is Outcome.REFUSED]
    if refused:
        for name, why in refused:
            note(f'refused, {why}: {name}')
        fail(f"the records of {', '.join((name for name, _ in refused))} could not be kept, so none of this task's were written")
    tips: list[str] = []
    refused = []
    for each, kept in zip(related, keep_records(related)):
        if kept.outcome is Outcome.KEPT:
            note(f'kept: {each.name}')
            note(f'records: {kept.reference}')
            if kept.commit and kept.commit not in tips:
                tips.append(kept.commit)
        elif kept.outcome is Outcome.NOT_OWED:
            note(f'not kept, {kept.why}: {each.name}')
        else:
            note(f'refused, {kept.why}: {each.name}')
            refused.append(each.name)
    for tip in tips:
        note(f'commit: {tip}')
    if refused:
        fail(f"the records of {', '.join(refused)} could not be kept; commit none of this task until they are")

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar git archive-task-records`."""
    parser = verbs.add_parser(ARCHIVE_COMMAND, help="keep a task's records on its project's records branch, to cite with the task's work and to find by content", description=f"Keep the records of the task TASK_ID on the branch {RECORDS_BRANCH} of the repository of\nthe project its plan names, at {RECORDS_RELATIVE.as_posix()}/<id>/ in that branch, and do the same for\nevery task whose Parent chain leads to it, all in one commit. The whole\nfolder is kept except the claim, caches, a path with a .git part, binary files,\na file over {KEEP_LIMIT_BYTES // 1024} KB that is not a document, and the task's own {TEMP_FOLDER}/ folder; the commit's\nmessage lists each of those with its size and why. The kept plan names the\nproject by its registered name, not by its path. Each kept task's\nreference (the branch, a colon, the folder) is printed, and the commit; the\ntask's commit cites each task by its id, with `_host_git_cli.py commit\n--task-id`, which finds it there. The project's HEAD,\nindex and working tree are not touched, and it never pushes. A project whose\npreferences say `{RECORDS_KEY}: {Records.OFF.value}` keeps none. A task whose records cannot be\nkept is named with why, and the verb fails before writing anything. What is kept\nis read by content as well as by id: `memar content find` and `memar content search`\nread it with `--from sessions`.")
    parser.add_argument('--task-id', required=True, help='the task whose work is being committed')
    return run

def run(args: argparse.Namespace) -> None:
    archive(args.task_id)
