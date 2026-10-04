#!/usr/bin/env python3
"""Tests for `memar`'s routing.

    python .agents/scripts/tests/memar.py

The subject is the `memar` launcher, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here runs the documentation set or writes to the machine: the routing is
a pure function, and a test that executed a tool to learn where an argument went
would be testing that tool instead.

What is pinned, and what each pin is for:

  VerbIsRouted        `memar install` goes to the installer and nothing else
                      does. The word is the only thing separating the two tools,
                      and a second spelling of it would be a second interface.
  EverythingElse      Every other invocation reaches the documentation tool,
                      including no arguments at all. A caller who types `memar`
                      and nothing else is asking for help, not for the installer,
                      and guessing on their behalf would run a machine change.
  ArgumentsAreForwarded  The tool receives the invocation with the routing word
                      removed and nothing else added, so a verb's own interface
                      is exactly what the caller wrote.
  HelpIsTheRouters   `memar --help` answers from this file, because it is the
                      routing that needs describing; a verb's interface belongs
                      to the verb, reached by asking that verb.
  LauncherBesideTools  Both launchers must sit beside the tools they route to.
                      A launcher that has drifted away is a command that reports
                      a missing file instead of doing the work.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

# The launcher has no extension, which is the point of it, so the loader is named
# rather than inferred: `spec_from_file_location` declines a file whose suffix it
# does not recognize, and a test that could not import its own subject would be a
# test of nothing.
_spec = importlib.util.spec_from_loader(
    "memar_launcher", SourceFileLoader("memar_launcher", str(SCRIPTS / "memar"))
)
memar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memar)


class VerbIsRouted(unittest.TestCase):
    def test_install_goes_to_the_installer(self) -> None:
        target, forwarded = memar.route(["install"])
        self.assertEqual(target, memar.INSTALLER)
        self.assertEqual(forwarded, [])

    def test_install_forwards_what_follows_it(self) -> None:
        target, forwarded = memar.route(["install", "--check", "/tmp/x"])
        self.assertEqual(target, memar.INSTALLER)
        self.assertEqual(forwarded, ["--check", "/tmp/x"])

    def test_install_is_the_only_routing_word(self) -> None:
        # The installer's own arguments are flags, so a positional word is the
        # only shape a router can read without guessing.
        for argv in (["installer"], ["Install"], ["--install"], ["install-agents"]):
            with self.subTest(argv=argv):
                target, _ = memar.route(argv)
                self.assertEqual(target, memar.DOCUMENTATION)


class EverythingElse(unittest.TestCase):
    def test_a_documentation_verb_reaches_the_documentation_tool(self) -> None:
        for argv in (["search", "Task"], ["section", "a.md", "b"], ["check", "docs"]):
            with self.subTest(argv=argv):
                target, _ = memar.route(argv)
                self.assertEqual(target, memar.DOCUMENTATION)

    def test_no_arguments_reaches_the_documentation_tool(self) -> None:
        # `memar` alone must not install anything. A caller who typed one word
        # has not asked for a machine change.
        target, forwarded = memar.route([])
        self.assertEqual(target, memar.DOCUMENTATION)
        self.assertEqual(forwarded, [])


class ArgumentsAreForwarded(unittest.TestCase):
    def test_the_documentation_tool_receives_the_invocation_unchanged(self) -> None:
        _, forwarded = memar.route(["search", "a", "b", "--from", "x.md"])
        self.assertEqual(forwarded, ["search", "a", "b", "--from", "x.md"])

    def test_the_router_adds_nothing_to_the_arguments(self) -> None:
        # A router that injected a flag would make the tool's declared
        # interface untrue for every caller that came through it.
        argv = ["check", "docs"]
        _, forwarded = memar.route(argv)
        self.assertEqual(forwarded, argv)

    def test_the_forwarded_list_is_not_the_callers_list(self) -> None:
        # Mutating the caller's list would be a side effect of routing, which is
        # the one thing a router must not have.
        argv = ["install", "x"]
        memar.route(argv)
        self.assertEqual(argv, ["install", "x"])


class HelpIsTheRouters(unittest.TestCase):
    def test_help_words_are_answered_here(self) -> None:
        for word in ("--help", "-h", "help"):
            with self.subTest(word=word):
                # The help goes to stdout, so it is captured: a test that prints
                # the thing it is testing makes the run's output unreadable.
                with contextlib.redirect_stdout(io.StringIO()) as printed:
                    code = memar.main([word])
                self.assertEqual(code, 0)
                self.assertIn(memar.INSTALL_VERB, printed.getvalue())

    def test_a_verb_asking_for_help_is_routed_not_answered(self) -> None:
        # `memar install --help` must reach the installer, or a caller cannot
        # read the interface of the thing they are about to run.
        target, _ = memar.route(["install", "--help"])
        self.assertEqual(target, memar.INSTALLER)

    def test_the_help_text_names_the_routing_word(self) -> None:
        self.assertIn(memar.INSTALL_VERB, memar.USAGE)


class LauncherBesideTools(unittest.TestCase):
    def test_both_tools_are_beside_the_launcher(self) -> None:
        for target in (memar.DOCUMENTATION, memar.INSTALLER):
            with self.subTest(target=target.name):
                self.assertTrue(target.is_file(), target)
                self.assertEqual(target.parent, SCRIPTS)

    def test_the_windows_shim_sits_beside_the_launcher(self) -> None:
        # Without it, a Windows shell cannot type the name at all, which would
        # make the command POSIX-only in a project that supports both.
        self.assertTrue((SCRIPTS / "memar.cmd").is_file())

    def test_the_shim_names_the_launcher_relative_to_itself(self) -> None:
        # `%~dp0` rather than a recorded path: the pair has to keep working when
        # the checkout moves, which is the normal case for a fetched repository.
        shim = (SCRIPTS / "memar.cmd").read_text(encoding="utf-8")
        self.assertIn("%~dp0memar", shim)


if __name__ == "__main__":
    unittest.main()
