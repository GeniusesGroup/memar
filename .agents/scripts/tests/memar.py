#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar`'s routing.

    python .agents/scripts/tests/memar.py

The subject is the `memar` launcher, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here runs a verb's work or writes to the machine. The contract is
pinned with fake services handed to `assemble`, because a test that ran a real
tool to learn how the router composes would be testing that tool instead; what
the real services declare is reached only through `--help` and usage errors,
which do no work, and each child launcher is a test run, so the daily update's
hook does nothing in it.

What is pinned, and what each pin is for:

  ContractComposes    A domain module's verb becomes a `memar` verb and a
                      capability module's verb a sub-verb under it, each with
                      its summary in the parent's list and its overview in its
                      own --help, under a usage argparse names itself. A
                      domain's run runs before its sub-verb's, so what every
                      verb of a domain owes is said once, and a non-zero status
                      stops the chain. A module that registers nothing and
                      returns a callable runs before every verb, --help too,
                      given the arguments as typed. A module without
                      `describe` is no part of the command line. A module that
                      fails to import is named on stderr and left out, and
                      every other verb, --help included, still answers.
  DomainsFirst        The shelf is read domain modules first, then
                      capabilities, each alphabetically, `_`-prefixed files
                      skipped: a capability's verbs go under a domain verb that
                      must already exist.
  RouterNamesNoVerb   No verb or sub-verb word the services declare appears
                      in the router as routing data. A verb named here as well
                      as in its service would be a second interface for one
                      behavior, and the two would drift.
  HelpListsTheServices
                      `memar --help` lists exactly the verbs the real services
                      declare, each with the summary it declared.
  EveryHelpAnswers    Every real verb's and sub-verb's --help exits 0 through
                      the launcher, under its own `memar` usage, so a caller
                      can always read the interface of what they are about to
                      run.
  UsageErrorsExit2    `memar` alone, an unknown verb, and a domain verb without
                      the sub-verb it needs exit 2 with a usage line. A caller
                      who typed one word has asked for nothing, and guessing on
                      their behalf would run something.
  HelpWordIsHelp      `memar help` prints exactly what `memar --help` prints:
                      one help, two spellings a person types.
  HelpCarriesMemarNotTheRouter
                      `memar --help` says what Memar is and carries none of the
                      router's mechanism, which is pinned to the docstring the
                      implementer reads; help that explains the implementation
                      is a non-answer printed confidently.
  ShimBesideLauncher  `memar.cmd` sits beside `memar`, names it relative to
                      itself, and hands it the same arguments, so a Windows
                      shell types the same command and gets the same answer.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import types
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

LAUNCHER = SCRIPTS / "memar"
SHIM = SCRIPTS / "memar.cmd"

# The launcher has no extension, which is the point of it, so the loader is named
# rather than inferred: `spec_from_file_location` declines a file whose suffix it
# does not recognize, and a test that could not import its own subject would be a
# test of nothing.
_spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(LAUNCHER)))
memar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memar)


def subparsers(parser: argparse.ArgumentParser) -> argparse._SubParsersAction | None:
    return next((action for action in parser._actions if isinstance(action, argparse._SubParsersAction)), None)


def declared() -> dict[tuple[str, ...], str]:
    """Every verb path the real services declare, with its one-line summary."""
    top, _ = memar.assemble(memar.services())
    found: dict[tuple[str, ...], str] = {}

    def walk(parser: argparse.ArgumentParser, path: tuple[str, ...]) -> None:
        group = subparsers(parser)
        if group is None:
            return
        summaries = {action.dest: action.help for action in group._choices_actions}
        for name, child in group.choices.items():
            found[(*path, name)] = summaries.get(name, "")
            walk(child, (*path, name))

    walk(top, ())
    return found


def launch(*arguments: str, command: list[str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*(command or [sys.executable, str(LAUNCHER)]), *arguments],
        capture_output=True,
        env=dict(os.environ, COLUMNS="1000", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"),
    )


def flat(text: bytes | str) -> str:
    return " ".join((text.decode("utf-8") if isinstance(text, bytes) else text).split())


class FakeShelf:
    """Services as the contract describes them, recording what runs."""

    NAMES = ["alpha", "gamma", "alpha_beta", "alpha_hook", "alpha_plain"]

    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self.status = {"alpha": None, "beta": None, "gamma": None}
        self.modules = {
            "alpha": types.SimpleNamespace(describe=self.describe_alpha),
            "gamma": types.SimpleNamespace(describe=self.describe_gamma),
            "alpha_beta": types.SimpleNamespace(describe=self.describe_beta),
            "alpha_hook": types.SimpleNamespace(describe=self.describe_hook),
            "alpha_plain": types.SimpleNamespace(),
        }

    def describe_alpha(self, verbs):
        parser = verbs.add_parser("alpha", help="the alpha summary", description="the alpha overview")
        parser.add_argument("--loud", action="store_true")
        return lambda args: self.ran("alpha", args.loud)

    def describe_gamma(self, verbs):
        verbs.add_parser("gamma", help="the gamma summary", description="the gamma overview")
        return lambda args: self.ran("gamma")

    def describe_beta(self, verbs):
        parser = verbs.add_parser("beta", help="the beta summary", description="the beta overview")
        parser.add_argument("word")
        return lambda args: self.ran("beta", args.word)

    def describe_hook(self, verbs):
        return lambda argv: self.calls.append(("hook", list(argv)))

    def ran(self, name: str, *seen) -> int | None:
        self.calls.append((name, *seen))
        return self.status[name]

    def assemble(self, names=None):
        return memar.assemble(self.NAMES if names is None else names, load=self.modules.__getitem__)

    def main(self, argv: list[str]) -> tuple[int, str, str]:
        """`memar.main` over this shelf: its status, stdout, and stderr; SystemExit's code when it exits."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(unittest.mock.patch.object(memar, "services", lambda: list(self.NAMES)))
            original = memar.assemble
            stack.enter_context(unittest.mock.patch.object(
                memar, "assemble", lambda names: original(names, load=self.modules.__getitem__),
            ))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            try:
                code = memar.main(argv)
            except SystemExit as exited:
                code = exited.code or 0
        return code, out.getvalue(), err.getvalue()


class ContractComposes(unittest.TestCase):
    def setUp(self) -> None:
        self.shelf = FakeShelf()

    def test_a_domain_verb_and_its_sub_verb_are_declared(self) -> None:
        top, before = self.shelf.assemble()
        self.assertEqual(set(subparsers(top).choices), {"alpha", "gamma"})
        alpha = subparsers(top).choices["alpha"]
        self.assertEqual(set(subparsers(alpha).choices), {"beta"})
        self.assertEqual(len(before), 1)

    def test_summaries_list_and_overviews_answer_under_argparses_own_usage(self) -> None:
        code, out, _ = self.shelf.main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("the alpha summary", out)
        self.assertIn("the gamma summary", out)
        code, out, _ = self.shelf.main(["alpha", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("usage: memar alpha", out)
        self.assertIn("the alpha overview", out)
        self.assertIn("the beta summary", out)
        code, out, _ = self.shelf.main(["alpha", "beta", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("usage: memar alpha beta", out)
        self.assertIn("the beta overview", out)

    def test_the_domains_run_runs_before_its_sub_verbs(self) -> None:
        code, _, _ = self.shelf.main(["alpha", "--loud", "beta", "word"])
        self.assertEqual(code, 0)
        self.assertEqual(
            self.shelf.calls,
            [("hook", ["alpha", "--loud", "beta", "word"]), ("alpha", True), ("beta", "word")],
        )

    def test_a_non_zero_status_stops_the_chain(self) -> None:
        self.shelf.status["alpha"] = 3
        code, _, _ = self.shelf.main(["alpha", "beta", "word"])
        self.assertEqual(code, 3)
        self.assertNotIn("beta", [call[0] for call in self.shelf.calls])
        self.shelf.status.update(alpha=None, beta=5)
        self.assertEqual(self.shelf.main(["alpha", "beta", "word"])[0], 5)

    def test_a_domain_verb_with_no_sub_verbs_runs_itself(self) -> None:
        self.assertEqual(self.shelf.main(["gamma"])[0], 0)
        self.assertEqual(self.shelf.calls[-1], ("gamma",))

    def test_a_module_registering_nothing_runs_before_every_verb_help_too(self) -> None:
        for argv in (["--help"], ["help"], ["gamma"], ["alpha", "beta", "--help"]):
            with self.subTest(argv=argv):
                self.shelf.calls.clear()
                self.shelf.main(argv)
                self.assertEqual(self.shelf.calls[0], ("hook", argv))

    def test_a_module_without_describe_is_no_part_of_the_command_line(self) -> None:
        with_plain = self.shelf.assemble(["alpha", "alpha_plain"])
        without = self.shelf.assemble(["alpha"])
        self.assertEqual(with_plain[1], without[1])
        self.assertEqual(with_plain[0].format_help(), without[0].format_help())

    def test_a_module_that_fails_to_import_is_named_and_the_rest_still_answer(self) -> None:
        modules = self.shelf.modules

        class Broken(dict):
            def __getitem__(self, name):
                if name == "gamma":
                    raise SyntaxError("broken on purpose")
                return modules[name]

        self.shelf.modules = Broken()
        code, out, err = self.shelf.main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("the alpha summary", out)
        self.assertNotIn("the gamma summary", out)
        self.assertIn("services/gamma.py", err)
        self.assertIn("broken on purpose", err)
        code, _, _ = self.shelf.main(["alpha", "beta", "word"])
        self.assertEqual(code, 0)
        self.assertIn(("beta", "word"), self.shelf.calls)

    def test_a_domain_verb_missing_its_sub_verb_is_a_usage_error(self) -> None:
        code, _, err = self.shelf.main(["alpha"])
        self.assertEqual(code, 2)
        self.assertIn("usage: memar alpha", err)
        self.assertNotIn(("alpha", False), self.shelf.calls)


class DomainsFirst(unittest.TestCase):
    def test_domains_come_before_capabilities_and_private_files_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            shelf = Path(folder)
            for name in ("zeta_a", "alpha_beta", "zeta", "_shared", "alpha", "alpha_aa"):
                (shelf / f"{name}.py").write_text("", encoding="utf-8")
            (shelf / "notes.md").write_text("", encoding="utf-8")
            self.assertEqual(memar.services(shelf), ["alpha", "zeta", "alpha_aa", "alpha_beta", "zeta_a"])

    def test_the_real_shelf_is_read_the_same_way(self) -> None:
        names = memar.services()
        domains = [name for name in names if memar.DOMAIN_SEPARATOR not in name]
        self.assertEqual(names[: len(domains)], sorted(domains))
        self.assertEqual(names[len(domains):], sorted(names[len(domains):]))


class RouterNamesNoVerb(unittest.TestCase):
    """The docstring may name a service as an example of the contract; that is
    the design being explained. What must not name one is a string the router
    holds, nor a name it gives a constant or function — and a sub-verb word such
    as `list` or `path` is checked in strings only, being also Python's own.
    """

    def test_no_declared_verb_word_is_routing_data_in_the_router(self) -> None:
        paths = declared()
        verbs = {path[0] for path in paths}
        words = {word for path in paths for word in path}
        self.assertTrue({"content", "install", "session", "update"} <= verbs, verbs)
        tree = ast.parse(LAUNCHER.read_text(encoding="utf-8"))
        docstring = tree.body[0].value if isinstance(tree.body[0], ast.Expr) else None
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and node is not docstring:
                for word in words & set(re.findall(r"[a-z][a-z-]*", node.value)):
                    with self.subTest(text=node.value[:40], word=word):
                        self.fail(f"the router's text names the verb {word!r}")
            name = getattr(node, "id", None) or getattr(node, "attr", None) or getattr(node, "name", None)
            if isinstance(name, str):
                for word in verbs & set(name.lower().split("_")):
                    with self.subTest(name=name, word=word):
                        self.fail(f"the router's identifier {name!r} names the verb {word!r}")


class HelpListsTheServices(unittest.TestCase):
    def test_memar_help_lists_exactly_the_declared_verbs_with_their_summaries(self) -> None:
        completed = launch("--help")
        self.assertEqual(completed.returncode, 0)
        out = completed.stdout.decode("utf-8")
        listed = dict(re.findall(r"^ {4}(\S+) +(.+)$", out, flags=re.MULTILINE))
        verbs = {path[0]: summary for path, summary in declared().items() if len(path) == 1}
        self.assertEqual(set(listed), set(verbs))
        for verb, summary in verbs.items():
            with self.subTest(verb=verb):
                self.assertTrue(summary)
                self.assertEqual(flat(listed[verb]), flat(summary))


class EveryHelpAnswers(unittest.TestCase):
    def test_every_verb_and_sub_verb_answers_its_help(self) -> None:
        paths = list(declared())
        self.assertTrue(any(len(path) == 2 for path in paths))
        for path in paths:
            with self.subTest(verb=" ".join(path)):
                completed = launch(*path, "--help")
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(f"usage: memar {' '.join(path)}", flat(completed.stdout))


class UsageErrorsExit2(unittest.TestCase):
    def assert_usage_error(self, *arguments: str) -> None:
        completed = launch(*arguments)
        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertIn("usage: memar", flat(completed.stderr))
        self.assertEqual(completed.stdout, b"")

    def test_memar_alone_is_a_usage_error(self) -> None:
        self.assert_usage_error()

    def test_an_unknown_verb_is_a_usage_error(self) -> None:
        self.assert_usage_error("no-such-verb")

    def test_a_domain_verb_missing_its_sub_verb_is_a_usage_error(self) -> None:
        domains = sorted({path[0] for path in declared() if len(path) == 2})
        self.assertTrue(domains)
        for domain in domains:
            with self.subTest(domain=domain):
                self.assert_usage_error(domain)


class HelpWordIsHelp(unittest.TestCase):
    def test_memar_help_prints_what_memar_dash_help_prints(self) -> None:
        word, flag = launch("help"), launch("--help")
        self.assertEqual((word.returncode, flag.returncode), (0, 0))
        self.assertEqual(word.stdout, flag.stdout)
        self.assertTrue(flag.stdout)


class HelpCarriesMemarNotTheRouter(unittest.TestCase):
    """`memar --help` is addressed to a person with Memar, not to an implementer.

    The two are different documents: the first says what the thing is and does,
    the second how it is built. The mechanism is pinned to the module docstring
    instead, which is the one text addressed to whoever opens the file.
    """

    MECHANISM = ("memar.cmd", "describe", "services/", "subprocess", "argparse", "route")

    def setUp(self) -> None:
        self.text = flat(launch("--help").stdout)

    def test_the_help_says_what_memar_is(self) -> None:
        for phrase in ("framework", "documents", "--help"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_the_help_does_not_carry_the_routers_implementation(self) -> None:
        for phrase in self.MECHANISM:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text)

    def test_the_mechanism_is_in_the_docstring_the_implementer_reads(self) -> None:
        for phrase in ("memar.cmd", "routes and nothing else", "describe(verbs)"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, memar.__doc__)


class ShimBesideLauncher(unittest.TestCase):
    def test_the_shim_sits_beside_the_launcher_and_names_it_relative_to_itself(self) -> None:
        # `%~dp0` rather than a recorded path: the pair has to keep working when
        # the checkout moves, which is the normal case for a fetched repository.
        self.assertTrue(LAUNCHER.is_file())
        self.assertEqual(SHIM.parent, LAUNCHER.parent)
        shim = SHIM.read_text(encoding="utf-8")
        self.assertIn("%~dp0memar", shim)
        self.assertRegex(shim, r'(?m)^python "%MEMAR_LAUNCHER%" %\*$')

    @unittest.skipUnless(os.name == "nt", "a .cmd shim runs only under a Windows shell")
    def test_the_shim_hands_the_launcher_the_same_arguments(self) -> None:
        shim = ["cmd", "/d", "/c", str(SHIM)]
        for arguments in (("update", "--help"), ("help",), ("no-such-verb",)):
            with self.subTest(arguments=arguments):
                through, direct = launch(*arguments, command=shim), launch(*arguments)
                self.assertEqual(through.returncode, direct.returncode)
                self.assertEqual(through.stdout, direct.stdout)


if __name__ == "__main__":
    unittest.main()
