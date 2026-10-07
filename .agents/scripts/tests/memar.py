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
  SessionIsRouted     `memar session` goes to the session tool, which
                      opens and closes one session folder under temp/; new
                      needs attach under the tool's own --help, never here
                      as new routing words.
  EverythingElse      Every other invocation reaches the content tool,
                      including no arguments at all. A caller who types `memar`
                      and nothing else is asking for help, not for the installer,
                      and guessing on their behalf would run a machine change.
  OnlyMemarsOwnActs   What the router routes to is what Memar itself does:
                      installing, a session's folder, and its content. A tool
                      that constrains a host tool the framework makes no claim to
                      is reached by path and not by a `memar` word, because a
                      command carrying it would read as Memar offering that tool.
  ArgumentsAreForwarded  The tool receives the invocation with the routing word
                      removed and nothing else added, so a verb's own interface
                      is exactly what the caller wrote.
  HelpIsTheRouters   `memar --help` answers from this file, because it is the
                      routing that needs describing; a verb's interface belongs
                      to the verb, reached by asking that verb.
  HelpCarriesMemarNotTheRouter
                      `memar --help` says what Memar is and what a person does
                      with it, and carries none of the router's mechanism. A
                      verb list with no next step is an index, not help, and
                      help that explains the implementation is a non-answer
                      printed confidently.
  LauncherBesideTools  Both launchers must sit beside the tools they route to.
                      A launcher that has drifted away is a command that reports
                      a missing file instead of doing the work.
  MissingToolIsAnError  A tool file not beside the launcher errors exit 2
                      rather than guessing another script; re-fetch, never
                      work around.
  RootIsTheInstallers  Where Memar lives is not a question about content, so it
                      is not a content verb: it is the installer's own question
                      and reached as `memar install --root`.
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
                self.assertEqual(target, memar.CONTENT)


class SessionIsRouted(unittest.TestCase):
    def test_session_goes_to_the_session_tool_with_the_rest_forwarded(self) -> None:
        # One routing word for the whole session lifecycle: new needs attach
        # under the tool's own --help, never as new words in this file.
        for argv in (["session", "new"], ["session", "close", "--session-id", "s-1"]):
            with self.subTest(argv=argv):
                target, forwarded = memar.route(argv)
                self.assertEqual(target, memar.SESSION)
                self.assertEqual(forwarded, argv[1:])

    def test_session_help_is_routed_not_answered(self) -> None:
        target, _ = memar.route(["session", "--help"])
        self.assertEqual(target, memar.SESSION)

    def test_the_help_text_names_the_session_word(self) -> None:
        self.assertIn(memar.SESSION_VERB, memar.USAGE)


class OnlyMemarsOwnActs(unittest.TestCase):
    """What `memar` routes to is what Memar itself does.

    A host-tool wrapper is deliberately absent: a command carrying it would read
    as Memar offering that tool, which is a claim the framework makes nowhere and
    — where its critique of version control is concerned — must not appear to
    make. The shelf says so in its own words; what is pinned here is that nothing
    in it became a `memar` verb.
    """

    HOST_SHELF = ("fs.py", "git.py")

    def test_no_host_wrapper_is_a_routing_word(self) -> None:
        for name in self.HOST_SHELF:
            with self.subTest(name=name):
                target, forwarded = memar.route([Path(name).stem])
                self.assertEqual(target, memar.CONTENT)
                self.assertNotIn(Path(name).stem, memar.USAGE)

    def test_the_router_names_only_the_three_acts(self) -> None:
        for verb in (memar.INSTALL_VERB, memar.SESSION_VERB, memar.CONTENT_VERB):
            with self.subTest(verb=verb):
                self.assertIn(verb, memar.USAGE)
        self.assertEqual(memar.CONTENT_VERB, "content")


class EverythingElse(unittest.TestCase):
    def test_a_content_verb_reaches_the_content_tool(self) -> None:
        for argv in (
            ["content", "search", "Task"],
            ["content", "section", "a.md", "b"],
            ["content", "check", "docs"],
            ["content", "write", "a.md"],
        ):
            with self.subTest(argv=argv):
                target, _ = memar.route(argv)
                self.assertEqual(target, memar.CONTENT)

    def test_no_arguments_reaches_the_content_tool(self) -> None:
        # `memar` alone must not install anything. A caller who typed one word
        # has not asked for a machine change.
        target, forwarded = memar.route([])
        self.assertEqual(target, memar.CONTENT)
        self.assertEqual(forwarded, [])


class ArgumentsAreForwarded(unittest.TestCase):
    def test_the_content_tool_receives_the_invocation_unchanged(self) -> None:
        _, forwarded = memar.route(["content", "search", "a", "b", "--from", "x.md"])
        self.assertEqual(forwarded, ["content", "search", "a", "b", "--from", "x.md"])

    def test_the_router_adds_nothing_to_the_arguments(self) -> None:
        # A router that injected a flag would make the tool's declared
        # interface untrue for every caller that came through it.
        argv = ["content", "check", "docs"]
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


class HelpCarriesMemarNotTheRouter(unittest.TestCase):
    """`memar --help` is addressed to a person with Memar, not to an implementer.

    The two are different documents and the difference is the whole of the
    distinction the architect draws between an Overview and a DevActionNote: the
    first says what the thing is and does, the second says how it is built. A
    person who typed `memar --help` has asked what Memar is, and answering with
    how the router dispatches subprocesses — or which shell can run which
    launcher file — is a non-answer printed confidently, which is worse than no
    answer because it looks like one.

    The mechanism is pinned to the module docstring instead, which is the one
    text addressed to whoever opens the file. A second copy of it in the help
    output is the drift this rejects, not a redundancy.
    """

    MECHANISM = (
        "memar.cmd",
        "routes and adds nothing",
        "declared by the tool that implements it",
        "subprocess",
        "extension",
    )

    def test_the_help_says_what_memar_is_and_what_it_does(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            memar.main(["--help"])
        text = printed.getvalue()
        for phrase in ("framework", "documents", "install", "session", "content"):
            self.assertIn(phrase, text)

    def test_the_help_names_a_next_step_rather_than_only_the_verbs(self) -> None:
        # A list of verbs is an index, not help. What the person does next —
        # where to look, how to ask — is the UserActionNote, and its absence is
        # what makes a verb list feel like a dead end.
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            memar.main(["--help"])
        self.assertIn("memar content path", printed.getvalue())

    def test_the_help_does_not_carry_the_routers_implementation(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            memar.main(["--help"])
        text = printed.getvalue()
        for phrase in self.MECHANISM:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_the_mechanism_is_in_the_docstring_the_implementer_reads(self) -> None:
        for phrase in ("memar.cmd", "routes and nothing else"):
            self.assertIn(phrase, memar.__doc__)


class LauncherBesideTools(unittest.TestCase):
    def test_both_tools_are_beside_the_launcher(self) -> None:
        for target in (memar.CONTENT, memar.INSTALLER, memar.SESSION):
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


class MissingToolIsAnError(unittest.TestCase):
    def test_missing_documentation_tool_errors_exit_2(self) -> None:
        saved = memar.CONTENT
        memar.CONTENT = SCRIPTS / "no-such-tool.py"
        self.addCleanup(setattr, memar, "DOCUMENTATION", saved)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = memar.main(["content", "search", "x"])
        self.assertEqual(code, 2)
        self.assertIn("not beside", err.getvalue())
        self.assertIn("Re-fetch", err.getvalue())

    def test_missing_installer_errors_exit_2(self) -> None:
        saved = memar.INSTALLER
        memar.INSTALLER = SCRIPTS / "no-such-installer.py"
        self.addCleanup(setattr, memar, "INSTALLER", saved)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = memar.main(["install"])
        self.assertEqual(code, 2)
        self.assertIn("not beside", err.getvalue())

    def test_missing_session_tool_errors_exit_2(self) -> None:
        saved = memar.SESSION
        memar.SESSION = SCRIPTS / "no-such-session.py"
        self.addCleanup(setattr, memar, "SESSION", saved)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = memar.main(["session", "new"])
        self.assertEqual(code, 2)
        self.assertIn("not beside", err.getvalue())

    def test_missing_tool_names_the_file_it_expected(self) -> None:
        saved = memar.CONTENT
        missing = SCRIPTS / "no-such-tool.py"
        memar.CONTENT = missing
        self.addCleanup(setattr, memar, "DOCUMENTATION", saved)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            memar.main([])
        self.assertIn(missing.name, err.getvalue())


class RootIsTheInstallers(unittest.TestCase):
    def test_asking_where_memar_lives_reaches_the_installer(self) -> None:
        target, forwarded = memar.route(["install", "--root"])
        self.assertEqual(target, memar.INSTALLER)
        self.assertEqual(forwarded, ["--root"])

    def test_a_bare_root_is_not_an_interfaces_of_its_own(self) -> None:
        # It was a content verb once, then a router word, and each was one more
        # spelling. Where Memar lives is the installer's own question, so it is
        # asked there and the router forwards it verbatim.
        target, forwarded = memar.route(["root"])
        self.assertEqual(target, memar.CONTENT)
        self.assertNotIn("root", memar.USAGE)


if __name__ == "__main__":
    unittest.main()
