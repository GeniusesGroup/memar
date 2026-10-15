#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_digest.py — every decision the sessions hand back, gathered into one digest.

Why one digest. The owner's attention is one of the two bottlenecks of the
work, and a question asked in each of a hundred sessions is a hundred
interruptions. A session that needs someone's decision writes it in its report
under `Decisions needed` — each entry the question, its options, and a
recommendation — and ends; `digest` gathers those entries across the sessions'
reports into one text, so the owner reads every open decision at once, each
beside the session and the report it came from. What a report's decisions are
is `session_report`'s answer, and so is whether the report is a hand-back at
all (`handback_problem`).

Why the hand-back is checked here. With no launcher, the digest is where the
agent that handed sessions out reads what came back, and so where a report
that is not a hand-back — longer than the delegating side may read, or with a
Status its plan's status disagrees with — has to be said: it is marked as a
failed hand-back beside its entries, for the owner to see, rather than
trusted. Each session's priority is shown too, since the owner answering
decisions answers the most pressing first.

Which sessions. Memar's own, newest first as `list` shows them, a project's
with `--project` — its own location included, which is where a project's
sessions lie by default (`temp/sessions/` inside it) — or one conversation's
with `--conversation`, wherever its sessions lie; the coordinator that handed
a conversation's sessions out asks for that one. Of those, a session is in the
digest when its report has entries, is a failed hand-back (even with no
entries, since a session that handed back nothing usable is itself what the
owner has to see), or looks finished or abandoned though it is not complete
(`session_concerns`). A complete session is in it too when it has entries: its
decisions are still the owner's to read. A queued session is left out, which no
one has worked yet and which has handed nothing back; one with no entries, no
flag, and a sound hand-back is left out too.

The review. With `--day` the digest is the owner's review of that day instead:
every session not queued that changed on that day (`session_day`), whatever
it holds, one by one, each with its status, report status, flags, a summary of its
Result (`session_summary`), its entries, and the command that closes it. The
owner and an agent read it together; the owner confirms which sessions really
finished, and the agent runs `close` (`session_close`) for those. The review
never closes: closing is the owner's word, spoken once per session, and one
service that both reads and removes would let a misread day remove work. What
a project wants kept of its finished tasks it keeps through `sessions` in its
own preferences; Memar's concern is the lasting summary in the changelog and
the final output, so a reviewed session leaves no folder behind.

Open handoff questions. A question only the owner can answer lives as an entry
under `Open Questions` in a handoff ([Questions Found During a
Task](../../docs/documentation-handoff.practice.md#questions-found-during-a-task)),
not in a report, so the digest ends with those entries as `content_questions`
lists them (blocking first, then oldest `Asked`), read from Memar's checkout or
from `--project`'s. An entry a report's `Decisions needed` line already points
to (the handoff's path with the entry's heading or line) is shown there and not
again here. A pointer to a handoff, or to a line of it, that holds no open
question is a failed hand-back: the question the session said it left is not
where it said. With `--day` only the entries asked that day are listed;
`--conversation` is about sessions, and leaves the entries out.
"""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import Callable

from machine.console import note
from services.session_record import REPORT
from services.status import Status
from services.content_questions import BLOCKING_MARK, handoff_files, open_questions
from services.content_reference import content_root
from services.session_concerns import concerns
from services.session_day import DAY_NAMES, day_of, parse_day
from services.project_find import add_project_flags, project_from_args
from services.session_find import find_sessions, project_of
from services.session_folder import Session
from services.session_plan_priority import priority_of
from services.session_report import REPORT_NAME, decisions_needed, handback_problem, read_report_status
from services.session_summary import summary_lines

OPEN_HEADING = "Open handoff questions"
DIGEST_COMMAND = "digest"
_POINTER = re.compile(r"([\w./\\~:-]*?[\w.-]+\.handoff\.md)(?::(\d+))?")
CLOSE_LINE = "close, once the owner confirms it is finished: memar session close --session-id"


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
            name, at = match.group(1), match.group(2)
            relative = Path(name.replace("\\", "/"))
            file = next((base / relative for base in bases if (base / relative).is_file()), None)
            if relative.is_absolute() and relative.is_file():
                file = relative
            if file is None:
                return f"{REPORT.hand_back_part} points to {name}, which does not exist"
            lines_found = [entry[0] for entry in open_questions(file)]
            if at is not None and int(at) not in lines_found:
                return f"{REPORT.hand_back_part} points to {name}:{at}, which holds no open question there"
            if not lines_found:
                return f"{REPORT.hand_back_part} points to {name}, which holds no open question"
    return None


def points_to(lines: list[str], shown: str, line: int, heading: str) -> bool:
    """Whether a `Decisions needed` line names the entry: its handoff's path, and its heading or its line."""
    for text in lines:
        flat = text.replace("\\", "/")
        if shown in flat and (heading.lower() in text.lower() or f"{shown}:{line}" in flat):
            return True
    return False


def print_open_questions(base: Path, decisions: list[str], wanted: date | None) -> int:
    """The `Open handoff questions` section for BASE; the entries listed, 0 and nothing printed when none are."""
    shown_entries = [
        entry for entry in open_entries(base)
        if (wanted is None or entry[1] == wanted.isoformat()) and not points_to(decisions, entry[2], entry[3], entry[4])
    ]
    if not shown_entries:
        return 0
    print()
    print(f"{OPEN_HEADING} — {len(shown_entries)} {'entry' if len(shown_entries) == 1 else 'entries'}")
    for _, _, shown, line, heading, blocking, _ in shown_entries:
        note(f"{shown}:{line}: {heading}" + (f" {BLOCKING_MARK}" if blocking else ""))
    return len(shown_entries)


def print_session(session: Session, entries: list[str], problem: str | None, flags: list[str], *, review: bool) -> None:
    """One session of the digest: its title, where it stands, what it came to when REVIEW, and what it asks."""
    print()
    print(f"{session.id}  {(session.front or {}).get('title', '')}")
    note(f"status: {session.status or 'none'}")
    note(f"priority: {priority_of(session.front)}")
    note(f"report: {read_report_status(session.path) or 'none'}")
    if problem:
        note(f"failed hand-back: {problem}")
    for flag in flags:
        note(f"concerns: {flag}")
    note(f"report: {session.path / REPORT_NAME}")
    if review:
        for line in summary_lines(session.path):
            note(line)
    for entry in entries:
        note(entry)
    if review:
        note(f"{CLOSE_LINE} {session.id}")


def print_digest(conversation: str | None = None, project: str | None = None, day: str | None = None) -> None:
    """`digest`: print the decisions and failed hand-backs, or with DAY every session of that day, in one text.

    PROJECT, as `list --project` takes it, reads that project's sessions
    wherever they lie; it is a name or a folder, and an empty one is refused.
    """
    wanted = parse_day(day) if day is not None else None
    root = project_of(project)
    base = root if root is not None else content_root()
    bases = [base]
    gathered = []
    decisions: list[str] = []
    for session in find_sessions(conversation=conversation, project=project_of(project)):
        if session.status == Status.QUEUED.key:
            continue
        if wanted is not None and day_of(session.path) != wanted:
            continue
        entries = decisions_needed(session.path)
        problem = handback_problem(session.path, session.status)
        decisions.extend(entries)
        owned = (session.front or {}).get("project", "")
        lying = pointer_problem(entries, [Path(owned), *bases] if owned and Path(owned).is_dir() else bases)
        if lying:
            problem = f"{problem}; {lying}" if problem else lying
        flags = concerns(session)
        if wanted is not None or entries or problem or flags:
            gathered.append((session, entries, problem, flags))
    listed = 0 if conversation is not None else None
    if not gathered:
        if listed is None:
            listed = print_open_questions(base, decisions, wanted)
        if not listed:
            note(f"no session changed on {wanted.isoformat()}" if wanted else "no decisions needed, and no failed hand-back")
        return
    count = sum(len(entries) for _, entries, _, _ in gathered)
    if wanted is not None:
        print(f"Review of {wanted.isoformat()} — {len(gathered)} sessions, {count} {REPORT.hand_back_part} entries")
    else:
        print(f"{REPORT.hand_back_part} — {len(gathered)} sessions, {count} entries")
    for session, entries, problem, flags in gathered:
        print_session(session, entries, problem, flags, review=wanted is not None)
    if listed is None:
        print_open_questions(base, decisions, wanted)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session digest`."""
    digester = verbs.add_parser(
        DIGEST_COMMAND,
        help="gather every session's decisions needed into one digest, or review a day's sessions",
        description=(
            f"Without --day: one digest of every entry under `{REPORT.hand_back_part}` in the\n"
            f"sessions' {REPORT_NAME}s: each session with entries, its title, status,\n"
            "priority, report status, and report, and its entries as written. A report that is\n"
            "not a short hand-back is in it too, entries or not, marked `failed\n"
            "hand-back`, with why, and so is a session not complete that looks finished or\n"
            "abandoned, marked `concerns`. Queued sessions are left out; a complete session\n"
            "is in only when it has entries or a failed hand-back. A short hand-back is\n"
            f"a {REPORT_NAME} with a Status that equals its plan's and, only when it needs\n"
            f"someone's decision, at most {REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`, each the\n"
            "question, its options, and the one it recommends.\n"
            "\n"
            "With --day: the review, for when the owner asks to \"review today's sessions\n"
            "with me and close the ones I confirm\". Every session not queued that changed on that day\n"
            "(its folder's latest change, in the local day), one by one: title, status,\n"
            "report status, priority, flags, what its report's Result says, its entries, and the\n"
            "command that closes it. Read each with the owner; for each the owner\n"
            "confirms finished, run that `memar session close --session-id ID` (the\n"
            "folder goes to the recycle bin). Close none the owner has not confirmed,\n"
            "and none of a project that keeps its sessions (its preferences set\n"
            "`sessions`): that is the project's record. The review closes nothing itself.\n"
            "\n"
            "After the sessions it lists the open entries of the handoffs, as `memar\n"
            "content questions` does: blocking first, then oldest Asked; with --day only\n"
            "those asked that day; none with --conversation. An entry a Decisions needed\n"
            "line already points to is not listed twice, and a pointer to a handoff or\n"
            "line that holds no open question is a failed hand-back.\n"
            "\n"
            "Memar's own sessions, or with --project a project's wherever they lie (a\n"
            "project's sessions are by default in its own temp/sessions/), or with\n"
            "--conversation one conversation's: the coordinator passes the id of a\n"
            "session of its own conversation."
        ),
    )
    add_project_flags(digester, "read the sessions of the project")
    digester.add_argument(
        "--day",
        default=None,
        metavar="DAY",
        help=f"review the sessions that changed on DAY: {DAY_NAMES}",
    )
    digester.add_argument(
        "--conversation",
        default=None,
        metavar="ID",
        help="gather only the sessions of the conversation the session ID belongs to",
    )
    return run


def run(args: argparse.Namespace) -> None:
    print_digest(args.conversation, project_from_args(args), args.day)
