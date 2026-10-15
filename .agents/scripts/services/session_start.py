#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_start.py — `memar session start`: everything a sub-agent needs in its context, in one output.

A sub-agent starts with none of its delegator's context, and what it had to do
to get its footing was a sequence of commands — load the skill, open the
session, read the plan, read the session help, find and read the governing
documents, read the help of each command — each one a round trip that costs the
owner time and tokens, and the route was invisible to the owner, who could not
see which of them were needed. This service is that route as one command: it
prints, in marked parts and in one order, what the Memar skill requires a
sub-agent to have read before it acts on its plan, so it runs one command and
starts. The brief that hands a session over (`session_brief`) is the same fixed
sentence for every task and says only to run this; whatever else a task needs
is in the session's plan, and this reads the plan to know what to print.

The parts, in order, each opened by a mark line `=== NAME ===`:

    session    the id and the paths; starting a session is `new --session-id`, so the report and the role folders are there
    model      the strongest model for a plan whose Kind is judgment, a cheaper one for a mechanical Kind; what to do on a weaker one
    plan.md    the plan, whole
    folder     the session folder's listing
    skill      the Memar skill, whole
    documents  the Cognition Abstract; for judgment the other passages the skill names for it; and each document the plan's Steps name
    help       `session` and `content write`, which every session needs, and each command the plan names
    ending     how the sub-agent ends

**Nothing here is a second copy of a rule.** The passages the skill requires are
read off the skill's own two bullets (`required_reading`), so a change to the
skill's list is a change here with no edit; the plan's Steps decide the rest,
by the paths of the documents they name, read at the section a link names or at
the Abstract when it names none (`content_section`, `content_meta`). The
model tier is the plan's Kind (`session_plan`); a plan with none leaves it to
the Request, and a Request that ideates, designs, or critiques then ends the
sub-agent Blocked, because a guess at the tier is the failure it prevents.

**Why the skill is printed whole.** The skill is the one thing every sub-agent
must hold and a route through a runtime's skill loader is not the same on every
runtime; one output with the skill in it is, and it saves the two commands that
located and read it.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, NamedTuple

from machine.console import fail
from machine.fs_memar import SKILL_RELATIVE
from services.content_meta import abstract
from services.content_reference import content_root, read_text
from services.content_section import by_anchor
from services.session_folder import folder_of, is_session_folder
from services.session_temp import TEMP_SENTENCE
from services.session_ensure import ensure_session
from services.session_plan import PLAN_NAME, part_text, read_plan
from services.session_plan_kind import CHEAPER_KINDS, KINDS, STRONG_KINDS, kind_of
from services.session_report import REPORT_NAME

START_COMMAND = "start"
SKILL_FILE = (SKILL_RELATIVE / "SKILL.md").as_posix()
SCRIPTS = Path(__file__).resolve().parent.parent
MEMAR = SCRIPTS / "memar"
MARK = "==="
# The commands every session needs the help of, as the words after `memar`.
ALWAYS_HELP = (("session",), ("content", "write"))
# At most this many commands the plan names get their help printed, so one long plan does not print the whole interface.
MOST_NAMED_COMMANDS = 8
HELP_TIMEOUT_SECONDS = 60
# The skill's bullets that name what is read, found by how each begins.
COGNITION_BULLET = "- Thinking runs in every step"
IDEATION_BULLET = "- Ideation, design, and critique"
# A link into the documents with an anchor, and the range the skill may follow it with ("from A through B").
SKILL_LINK = re.compile(r"\]\(/(docs/[^)#\s]+\.md)#([^)\s]+)\)(?:\s+from\s+[^;]+?\s+through\s+([^;]+))?")
# A document a plan's Steps name, with the section it may name.
STEP_DOCUMENT = re.compile(r"(?<![\w.-])/?(docs/[\w./-]+?\.md)(?:#([\w-]+))?")
# A command a plan names: what is between backticks after `memar `.
NAMED_COMMAND = re.compile(r"`memar ([^`]+)`")
COMMAND_WORD = re.compile(r"[a-z][a-z-]*$")
MOST_COMMAND_WORDS = 3

ENDING = (
    f"Put nothing at the session folder's top but {PLAN_NAME} and {REPORT_NAME}: anything else you make goes in the role "
    "folder of its kind, as `memar session --help` (above) says. Do what the plan's Request says, without rewriting that Request.\n"
    f"End with its {REPORT_NAME} and Status as `memar session --help` says. Where you may write files, write the report "
    "through `memar content write --create FILE --content-file SCRATCHFILE`, SCRATCHFILE a file in the session's own folder. "
    f"Where you may only return text, return the report as your final text, and the delegating session writes it as "
    f"{REPORT_NAME} before its next step.\n"
    f"{TEMP_SENTENCE}"
)


class Ref(NamedTuple):
    """A passage of a document: its path under the checkout, the anchor of its heading, and the heading its range runs through."""

    path: str
    anchor: str
    through: str | None = None

    @property
    def link(self) -> str:
        return f"{self.path}#{self.anchor}"


class Reading(NamedTuple):
    """What the skill requires a sub-agent to have read: always, and when its task is judgment."""

    always: list[Ref]
    judgment: list[Ref]


def _bullet(skill: str, start: str) -> str:
    for line in skill.splitlines():
        if line.startswith(start):
            return line
    fail(f"the skill has no bullet beginning {start!r}, so what it requires a sub-agent to read cannot be found")


def _links(bullet: str) -> list[Ref]:
    return [Ref(path, anchor, (through or "").strip(" .") or None) for path, anchor, through in SKILL_LINK.findall(bullet)]


def required_reading(skill: str) -> Reading:
    """The passages the SKILL's text requires, read off its two bullets.

    The first anchored link of the Cognition bullet is the Abstract every
    sub-agent reads; the rest of that bullet, and every link of the bullet on
    ideation, design, and critique, are read when the task is judgment.
    """
    cognition = _links(_bullet(skill, COGNITION_BULLET))
    return Reading(cognition[:1], [*cognition[1:], *_links(_bullet(skill, IDEATION_BULLET))])


def _part(name: str, body: str) -> str:
    return f"{MARK} {name} {MARK}\n{body.strip()}\n"


def _session_part(session_id: str, folder: Path) -> str:
    return _part(
        "session",
        f"session_id: {session_id}\npath: {folder}\nplan: {folder / PLAN_NAME}\nreport: {folder / REPORT_NAME}",
    )


def _model_part(kind: str) -> str:
    if kind in STRONG_KINDS:
        body = (
            f"kind: {kind}\nThis task is judgment and needs the strongest model the runtime offers. If you run on a "
            "weaker one, or cannot tell, end Blocked saying which model you run on, and do nothing else."
        )
    elif kind in CHEAPER_KINDS:
        body = f"kind: {kind}\nThis task is mechanical: a cheaper model than the session's own suffices."
    elif kind:
        body = (
            f"kind: {kind}\n{kind!r} is not a kind; the kinds are {', '.join(KINDS)}. End Blocked saying so, "
            "for the session that handed you the task to correct it."
        )
    else:
        body = (
            "kind: the plan states no kind.\nIf its Request ideates, designs, or critiques, end Blocked saying the plan "
            "states no kind: the strongest model is needed and the delegator states it. Otherwise a cheaper model suffices."
        )
    return _part("model", body)


def _folder_part(folder: Path) -> str:
    entries = sorted(folder.rglob("*"), key=lambda path: path.relative_to(folder).as_posix().lower())
    lines = [path.relative_to(folder).as_posix() + ("/" if path.is_dir() else "") for path in entries]
    return _part("folder", "\n".join(lines))


def _passage(root: Path, ref: Ref) -> str:
    """REF's text under a line saying where it comes from; a document or section that is not there is said, not skipped."""
    file = root / ref.path
    if not file.is_file():
        return f"--- {ref.link} ---\nthe document {ref.path} is not there in this checkout"
    found = by_anchor(read_text(file), ref.anchor, ref.through) if ref.anchor else abstract(read_text(file))
    if found is None:
        return f"--- {ref.link} ---\nno section answers to #{ref.anchor} in {ref.path}"
    return f"--- {ref.link if ref.anchor else ref.path + ' (Abstract)'} ---\n{found}"


def step_documents(steps: str) -> list[Ref]:
    """The documents the plan's STEPS text names, each at the section it names or none, once, in the order named."""
    found: list[Ref] = []
    for path, anchor in STEP_DOCUMENT.findall(steps):
        ref = Ref(path, anchor)
        if ref not in found:
            found.append(ref)
    return found


def _documents_part(root: Path, kind: str, reading: Reading, steps: str) -> str:
    wanted = [*reading.always, *(reading.judgment if kind in STRONG_KINDS else []), *step_documents(steps)]
    refs = list(dict.fromkeys(wanted))
    return _part("documents", "\n\n".join(_passage(root, ref) for ref in refs))


def named_commands(plan: str) -> list[tuple[str, ...]]:
    """The commands the PLAN's text names in backticks, as the words after `memar`, once each, and none that every session reads."""
    found: list[tuple[str, ...]] = []
    for text in NAMED_COMMAND.findall(plan):
        words: list[str] = []
        for word in text.split():
            if not COMMAND_WORD.match(word) or len(words) == MOST_COMMAND_WORDS:
                break
            words.append(word)
        command = tuple(words)
        if command and command not in found and command not in ALWAYS_HELP:
            found.append(command)
    return found


def _help_of(words: tuple[str, ...]) -> str | None:
    """`memar WORDS --help`'s output, or None when WORDS name no command."""
    try:
        done = subprocess.run(
            [sys.executable, str(MEMAR), *words, "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=HELP_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else None


def _help_part(plan: str) -> str:
    named = named_commands(plan)
    shown, left = named[:MOST_NAMED_COMMANDS], named[MOST_NAMED_COMMANDS:]
    blocks = []
    for words in (*ALWAYS_HELP, *shown):
        command = "memar " + " ".join(words)
        found = _help_of(words)
        blocks.append(f"--- `{command} --help` ---\n" + (found if found is not None else f"no such command: `{command}`"))
    if left:
        blocks.append("--- not printed ---\n" + "\n".join(f"`memar {' '.join(words)}`: ask `--help` of it" for words in left))
    return _part("help", "\n\n".join(blocks))


def start_text(session_id: str) -> str:
    """The text that starts the session SESSION_ID: its parts, once its folder and its plan are there."""
    folder = folder_of(session_id)
    if not is_session_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(
            f"no task to start in {session_id}: it has no session folder with a {PLAN_NAME}. "
            "Open it with `memar session new --title T --parent ID --project NAME` (or `--project-path PATH`), ID the session handing it over, "
            f"and write the task into its {PLAN_NAME} first"
        )
    _, folder = ensure_session(session_id)
    plan_file = folder / PLAN_NAME
    plan = plan_file.read_text(encoding="utf-8-sig")
    kind = kind_of(read_plan(plan_file).front)
    root = content_root()
    skill = read_text(root / SKILL_FILE)
    return "\n".join(
        [
            _session_part(session_id, folder),
            _model_part(kind),
            _part(PLAN_NAME, plan),
            _folder_part(folder),
            _part("skill", skill),
            _documents_part(root, kind, required_reading(skill), part_text(plan_file, "Steps")),
            _help_part(plan),
            _part("ending", ENDING),
        ]
    )


def print_start(session_id: str) -> None:
    """`start`: print SESSION_ID's start text."""
    print(start_text(session_id))


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session start`."""
    starter = verbs.add_parser(
        START_COMMAND,
        help="print, in one output, everything a sub-agent needs in its context for its session",
        description=(
            "For the agent handed a session. Print, in parts each opened by a line `=== NAME ===`, and in\n"
            f"this order: the session's id and paths, the model its Kind needs, its {PLAN_NAME}, the folder's\n"
            "listing, the Memar skill, the documents the skill requires and the plan's Steps name, the\n"
            "help of the commands every session uses and those the plan names, and how to end. Run it\n"
            "first, once, and read nothing else before acting on the plan: it is what the skill requires\n"
            "read before the plan's steps, in one command.\n"
            "\n"
            "It is `new --session-id ID` as well, so the report and the role folders are there after it;\n"
            "it opens no new session, and refuses an ID that has no folder with a plan."
        ),
    )
    starter.add_argument("--session-id", required=True, metavar="ID", help="the session handed to you")
    return run


def run(args: argparse.Namespace) -> None:
    print_start(args.session_id)
