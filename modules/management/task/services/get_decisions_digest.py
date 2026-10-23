#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/get_decisions_digest.py — every decision the tasks hand back, gathered into one digest.

Why one digest. The owner's attention is one of the two bottlenecks of the
work, and a question asked in each of a hundred tasks is a hundred
interruptions. A task that needs someone's decision writes it in its report
under `Decisions needed` — each entry the question, its options, and a
recommendation — and ends; `digest` gathers those entries across the tasks'
reports into one text, so the owner reads every open decision at once, each
beside the task and the report it came from. What a report's decisions are
is `task_report`'s answer, and so is whether the report is a hand-back at
all (`handback_problem`).

Why the hand-back is checked here. With no launcher, the digest is where the
agent that handed tasks out reads what came back, and so where a report
that is not a hand-back — longer than the delegating side may read, or with a
Status its plan's status disagrees with — has to be said: it is marked as a
failed hand-back beside its entries, for the owner to see, rather than
trusted. Each task's priority is shown too, since the owner answering
decisions answers the most pressing first.

Which tasks. Memar's own, newest first as `list` shows them, a project's
with `--project` — its own location included, which is where a project's
tasks lie by default (`.agents/tasks/` inside it) — or one conversation's
with `--conversation`, wherever its tasks lie; the task that handed
a conversation's tasks out asks for that one. Of those, a task is in the
digest when its report has entries, is a failed hand-back (even with no
entries, since a task that handed back nothing usable is itself what the
owner has to see), or looks finished or abandoned though it is not complete
(`task_concerns`). A complete task is in it too when it has entries: its
decisions are still the owner's to read. A queued task is left out, which no
one has worked yet and which has handed nothing back; one with no entries, no
flag, and a sound hand-back is left out too.

The review. With `--day` the digest is the owner's review of that day instead:
every task not queued that changed on that day (`task_day`), whatever
it holds, one by one, each with its status, report status, flags, a summary of its
Result (`task_summary`), its entries, and the command that closes it. The
owner and an agent read it together; the owner confirms which tasks really
finished, and the agent runs `close` (`task_close`) for those. The review
never closes: closing is the owner's word, spoken once per task, and one
service that both reads and removes would let a misread day remove work. What
a project wants kept of its finished tasks it keeps through `tasks` in its
own preferences; Memar's concern is the lasting summary in the changelog and
the final output, so a reviewed task leaves no folder behind.

Open handoff questions. A question only the owner can answer lives as an entry
under `Open Questions` in a handoff ([Questions Found During a
Task](../../../modules/knowledge/documentation/handoff/handoff.practice.md#questions-found-during-a-task)),
not in a report, so the digest ends with those entries as `content_questions`
lists them (blocking first, then oldest `Asked`), read from Memar's checkout or
from `--project`'s. An entry a report's `Decisions needed` line already points
to (the handoff's path with the entry's heading or line) is shown there and not
again here. A pointer to a handoff, or to a line of it, that holds no open
question is a failed hand-back: the question the task said it left is not
where it said. With `--day` only the entries asked that day are listed;
`--conversation` is about tasks, and leaves the entries out.
"""
from __future__ import annotations
import argparse
import re
from datetime import date
from pathlib import Path
from typing import Callable
from machine.console import note
from modules.knowledge.documentation.record import REPORT
from modules.knowledge.documentation.primitive.status import Status
from modules.knowledge.content.services.questions import BLOCKING_MARK, handoff_files, open_questions
from modules.knowledge.content.services.reference import content_root
from modules.management.task.services.dependency import Reader
from modules.management.task.services.concerns import concerns
from modules.management.task.services.depends import concerns_for, reconcile_all
from modules.management.task.services.day import DAY_NAMES, day_of, parse_day
from modules.process.project.services.find import add_project_flags, project_from_args
from modules.management.task.services.list import find_tasks, project_of
from modules.management.task.services.folder import Task
from modules.knowledge.documentation.plan.primitive.priority import Priority
from modules.knowledge.documentation.report.services.report import REPORT_NAME, decisions_needed, handback_problem, read_report_status
from modules.knowledge.documentation.report.services.summary import summary_lines
from modules.process.project.primitive.project_name import ProjectName
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
OPEN_HEADING = 'Open handoff questions'
DIGEST_COMMAND = 'get-decisions-digest'
_POINTER = re.compile('([\\w./\\\\~:-]*?[\\w.-]+\\.handoff\\.md)(?::(\\d+))?')
CLOSE_LINE = 'close, once the owner confirms it is finished: memar git trash-task-folder --task-id'

def open_entries(base: Path) -> list[tuple[bool, str, str, int, str, bool, Path]]:
    """The open entries under BASE, in `content questions` order: (not blocking, asked, shown path, line, heading, blocking, path)."""
    found = []
    for path in handoff_files(base):
        try:
            shown = path.relative_to(base).as_posix()
        except ValueError:
            shown = path.as_posix()
        for line, heading, blocking, asked in open_questions(path):
            found.append((not blocking, asked, shown, line, heading, blocking, path))
    found.sort(key=lambda hit: hit[:4])
    return found

def pointer_problem(lines: list[str], bases: list[Path]) -> str | None:
    """Why a `Decisions needed` line points to an entry that is not there; None when none does.

    A line naming `X.handoff.md` (with `:LINE` or not) points to the handoff
    at X, found under one of BASES; it fails when the file is missing, holds
    no open question, or holds none at that line.
    """
    for line in lines:
        for match in _POINTER.finditer(line):
            name, at = (match.group(1), match.group(2))
            relative = Path(name.replace('\\', '/'))
            file = next((base / relative for base in bases if (base / relative).is_file()), None)
            if relative.is_absolute() and relative.is_file():
                file = relative
            if file is None:
                return f'{REPORT.hand_back_part} points to {name}, which does not exist'
            lines_found = [entry[0] for entry in open_questions(file)]
            if at is not None and int(at) not in lines_found:
                return f'{REPORT.hand_back_part} points to {name}:{at}, which holds no open question there'
            if not lines_found:
                return f'{REPORT.hand_back_part} points to {name}, which holds no open question'
    return None

def points_to(lines: list[str], shown: str, line: int, heading: str) -> bool:
    """Whether a `Decisions needed` line names the entry: its handoff's path, and its heading or its line."""
    for text in lines:
        flat = text.replace('\\', '/')
        if shown in flat and (heading.lower() in text.lower() or f'{shown}:{line}' in flat):
            return True
    return False

def print_open_questions(base: Path, decisions: list[str], wanted: date | None) -> int:
    """The `Open handoff questions` section for BASE; the entries listed, 0 and nothing printed when none are."""
    shown_entries = [entry for entry in open_entries(base) if (wanted is None or entry[1] == wanted.isoformat()) and (not points_to(decisions, entry[2], entry[3], entry[4]))]
    if not shown_entries:
        return 0
    print()
    print(f"{OPEN_HEADING} — {len(shown_entries)} {('entry' if len(shown_entries) == 1 else 'entries')}")
    for _, _, shown, line, heading, blocking, _ in shown_entries:
        note(f'{shown}:{line}: {heading}' + (f' {BLOCKING_MARK}' if blocking else ''))
    return len(shown_entries)

def print_task(task: Task, entries: list[str], problem: str | None, flags: list[str], *, review: bool) -> None:
    """One task of the digest: its title, where it stands, what it came to when REVIEW, and what it asks."""
    print()
    print(f"{task.id}  {(task.front or {}).get('title', '')}")
    note(f"status: {task.status or 'none'}")
    note(f'priority: {Priority.of(task.front)}')
    note(f"report: {read_report_status(task.path) or 'none'}")
    if problem:
        note(f'failed hand-back: {problem}')
    for flag in flags:
        note(f'concerns: {flag}')
    note(f'report: {task.path / REPORT_NAME}')
    if review:
        for line in summary_lines(task.path):
            note(line)
    for entry in entries:
        note(entry)
    if review:
        note(f'{CLOSE_LINE} {task.id}')

def get_decisions_digest(conversation: str | None=None, project: str | None=None, day: str | None=None) -> None:
    """`digest`: print the decisions and failed hand-backs, or with DAY every task of that day, in one text.

    PROJECT, as `list --project` takes it, reads that project's tasks
    wherever they lie; it is a name or a folder, and an empty one is refused.
    """
    wanted = parse_day(day) if day is not None else None
    root = project_of(project)
    base = root if root is not None else content_root()
    bases = [base]
    gathered = []
    decisions: list[str] = []
    reconcile_all(find_tasks(conversation=conversation, project=project_of(project)))
    reader = Reader(None)
    for task in find_tasks(conversation=conversation, project=project_of(project)):
        if task.status == Status.QUEUED.key:
            continue
        if wanted is not None and day_of(task.path) != wanted:
            continue
        entries = decisions_needed(task.path)
        problem = handback_problem(task.path, task.status)
        decisions.extend(entries)
        owned = (task.front or {}).get(PlanKey.PROJECT.key, '')
        lying = pointer_problem(entries, [Path(owned), *bases] if owned and Path(owned).is_dir() else bases)
        if lying:
            problem = f'{problem}; {lying}' if problem else lying
        flags = [*concerns(task), *concerns_for(task, reader)]
        if wanted is not None or entries or problem or flags:
            gathered.append((task, entries, problem, flags))
    listed = 0 if conversation is not None else None
    if not gathered:
        if listed is None:
            listed = print_open_questions(base, decisions, wanted)
        if not listed:
            note(f'no task changed on {wanted.isoformat()}' if wanted else 'no decisions needed, and no failed hand-back')
        return
    count = sum((len(entries) for _, entries, _, _ in gathered))
    if wanted is not None:
        print(f'Review of {wanted.isoformat()} — {len(gathered)} tasks, {count} {REPORT.hand_back_part} entries')
    else:
        print(f'{REPORT.hand_back_part} — {len(gathered)} tasks, {count} entries')
    for task, entries, problem, flags in gathered:
        print_task(task, entries, problem, flags, review=wanted is not None)
    if listed is None:
        print_open_questions(base, decisions, wanted)

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task get-decisions-digest`."""
    digester = verbs.add_parser(DIGEST_COMMAND, help="gather every task's decisions needed into one digest, or review a day's tasks", description=f"""Without --day: one digest of every entry under `{REPORT.hand_back_part}` in the tasks'\n{REPORT_NAME}s: each task with entries, its title, status, priority, report status, and\nentries as written. A report that is not a short hand-back is in it too, marked `failed\nhand-back` with why, and so is a task not complete that looks finished or abandoned,\nmarked `concerns`; so is a task Blocked by its `{PlanKey.DEPENDS_ON.written}`, with what it waits for, and a\ndependency that cannot be found or makes a cycle. Queued tasks are left out; a complete task is in only when it has\nentries or a failed hand-back. A short hand-back is a {REPORT_NAME} whose Status equals its\nplan's and, only when it needs a decision, at most {REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`,\neach the question, its options, and the one it recommends.\n\nWith --day: the review, for when the owner asks to "review today's tasks with me and\nclose the ones I confirm". Every task not queued that changed on that day, one by one,\nwith the command that closes it. Read each with the owner; run that\n`memar git trash-task-folder --task-id ID` only for those the owner confirms finished, and for\nnone of a project that keeps its tasks (its preferences set `tasks`). The review closes\nnothing itself.\n\nAfter the tasks it lists the open handoff entries, as `memar content questions` does:\nblocking first, then oldest Asked; with --day only those asked that day; none with\n--conversation. A pointer to a handoff or line that holds no open question is a failed\nhand-back.\n\nWithout a project flag it reads Memar's own tasks; {ProjectName.FLAG} reads a project's wherever\nthey lie; --conversation one conversation's, by the id of a task in it.""")
    add_project_flags(digester, 'read the tasks of the project')
    digester.add_argument('--day', default=None, metavar='DAY', help=f'review the tasks that changed on DAY: {DAY_NAMES}')
    digester.add_argument('--conversation', default=None, metavar='ID', help='gather only the tasks of the conversation the task ID belongs to')
    return run

def run(args: argparse.Namespace) -> None:
    get_decisions_digest(args.conversation, project_from_args(args), args.day)
