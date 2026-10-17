#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar commands`, in `services/commands.py`.

    python .agents/scripts/services/tests/commands.py

What is pinned, and what each pin is for:

  CardIsGenerated  The card lists a command the services declare, with its
                   call shape and its summary, and holds a command no service
                   declares only if one does: it is read from the parsers, so
                   a verb added later is on it with nothing written.
  CardIsShort      Every command is two lines and the card stays under a bound,
                   because a card longer than that is the `--help` it replaces.
  HelpIsShort      No command's own `--help` passes a bound: what a caller needs
                   to call it is the help, and the reasons are the file's
                   opening comment (the owner's ruling, 2026-10-16).
  NoHelpFlag       The help flag is not part of a call's shape.
  Running          `memar commands` prints the card and exits 0.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import services.commands as commands

# Well under what the command line's own help costs to descend, and far over what the card now is.
MOST_CHARACTERS = 9_000
# A command's own help; the longest today is a recipe the owner asked to keep whole.
MOST_HELP_CHARACTERS = 4_500


def sample() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="memar")
    verbs = top.add_subparsers(dest="verb")
    domain = verbs.add_parser("thing", help="a domain")
    inner = domain.add_subparsers(dest="sub")
    inner.add_parser("make", help="make a thing. It also does more that is long.").add_argument("name")
    verbs.add_parser("bare", help="no arguments")
    return top


class CardIsGenerated(unittest.TestCase):
    def test_a_declared_command_is_on_the_card_with_its_shape_and_summary(self) -> None:
        card = commands.card_text(sample())
        self.assertIn("memar thing make name\n    make a thing.\n", card)
        self.assertIn("memar bare\n    no arguments\n", card)

    def test_the_real_card_lists_the_commands_every_session_uses(self) -> None:
        card = commands.card_text()
        for line in ("memar session start --session-id ID", "memar content write", "memar commands"):
            self.assertIn(line, card)

    def test_the_card_names_where_the_rest_is(self) -> None:
        self.assertIn("`memar WORDS --help`", commands.card_text(sample()))


class CardIsShort(unittest.TestCase):
    def test_the_real_card_is_under_the_bound(self) -> None:
        self.assertLessEqual(len(commands.card_text()), MOST_CHARACTERS)

    def test_a_summary_is_cut_at_its_first_sentence(self) -> None:
        self.assertNotIn("long", commands.card_text(sample()))


def leaves(parser: argparse.ArgumentParser, words: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], argparse.ArgumentParser]]:
    children = commands._children(parser)
    if not children:
        return [(words, parser)]
    return [leaf for name, (child, _) in children.items() for leaf in leaves(child, (*words, name))]


class HelpIsShort(unittest.TestCase):
    def test_no_command_help_passes_the_bound(self) -> None:
        router = commands._router()
        parser, _ = router.assemble(router.services())
        long = {" ".join(words): len(leaf.format_help()) for words, leaf in leaves(parser) if len(leaf.format_help()) > MOST_HELP_CHARACTERS}
        self.assertEqual(long, {}, "move the reasons into the file's opening comment; the help keeps what a caller needs")


class NoHelpFlag(unittest.TestCase):
    def test_the_help_flag_is_not_in_a_shape(self) -> None:
        self.assertNotIn("[-h]", commands.card_text())


class Running(unittest.TestCase):
    def test_the_command_prints_the_card(self) -> None:
        environment = dict(os.environ, PYTHONIOENCODING="utf-8", MEMAR_NO_AUTO_UPDATE="1")
        done = subprocess.run([sys.executable, str(SCRIPTS / "memar"), "commands"], capture_output=True, env=environment)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("memar commands", done.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
