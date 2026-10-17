#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/command/command.py — `memar commands`: every command and what it takes, as one short card.

An agent that does not know which commands exist, or how to call them, learns
it by asking `--help` of the router, then of a domain, then of each verb: a
round trip per level, each answer written for a person and carrying the
reasons beside the usage. What an agent needs before it acts is the other half
of that: which commands there are, what each is for in a line, and the shape
of the call. This prints exactly that, one command per two lines, for the whole
tree; the reasons and the definitions stay in each command's own `--help`,
which the card sends the reader to for the one command it needs.

**Nothing here is a second copy of an interface.** The card is generated, at
the moment it is printed, from the command line the services declare
(`assemble` in the router), so a verb added, renamed or given another argument
is on the card without anyone writing a line, and the card cannot disagree with
`--help` because it reads the same parsers. `session start` prints it in the
text it hands an agent, so an agent that took up a session already knows what
exists; any other agent runs `memar commands`.
"""
from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import re
from pathlib import Path
from typing import Callable

SCRIPTS = Path(__file__).resolve().parents[3] / ".agents" / "scripts"
ROUTER = SCRIPTS / "memar"
COMMANDS_COMMAND = "commands"
USAGE_PREFIX = re.compile(r"^usage:\s*")
HELP_FLAG = re.compile(r"\s*\[-h\]")
FIRST_SENTENCE = re.compile(r"^(.*?[.])(?:\s|$)")
INDENT = "    "
CLOSING = "Take one command's reasons, words and every option from `memar WORDS --help`."


def _router():
    """The router module, loaded from its file, which has no `.py` name to import."""
    loader = importlib.machinery.SourceFileLoader("memar_router", str(ROUTER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def _children(parser: argparse.ArgumentParser) -> dict[str, tuple[argparse.ArgumentParser, str]]:
    """The sub-verbs of PARSER, each with its parser and its one-line summary, in the order declared."""
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            summaries = {item.dest: (item.help or "") for item in action._choices_actions}
            return {name: (child, summaries.get(name, "")) for name, child in action.choices.items()}
    return {}


def _usage(parser: argparse.ArgumentParser) -> str:
    """The call's shape on one line: `memar WORDS` and the arguments, without the help flag."""
    return HELP_FLAG.sub("", " ".join(USAGE_PREFIX.sub("", parser.format_usage()).split()))


def _first_line(summary: str) -> str:
    """SUMMARY up to its first sentence, so one long summary does not stand for the card."""
    text = " ".join(summary.split())
    found = FIRST_SENTENCE.match(text)
    return found.group(1) if found else text


def _lines(parser: argparse.ArgumentParser, summary: str, out: list[str]) -> None:
    children = _children(parser)
    if not children:
        out.append(_usage(parser))
        out.append(INDENT + _first_line(summary))
        return
    for child, text in children.values():
        _lines(child, text, out)


def card_text(parser: argparse.ArgumentParser | None = None) -> str:
    """The card of PARSER, or of the whole command line the services declare."""
    if parser is None:
        router = _router()
        parser, _ = router.assemble(router.services())
    out: list[str] = []
    _lines(parser, "", out)
    return "\n".join([*out, "", CLOSING]) + "\n"


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar commands`."""
    verbs.add_parser(
        COMMANDS_COMMAND,
        help="print every command with its call shape and a line on what it is for",
        description=(
            "Print the whole command line as a card: each command's call shape and, under it, one line\n"
            "on what it is for. It is generated from the commands as they are declared, so it is\n"
            "current. Read it once before choosing a command; the reasons and the words of one\n"
            "command are in its own `--help`."
        ),
    )
    return run


def run(args: argparse.Namespace) -> None:
    print(card_text(), end="")
