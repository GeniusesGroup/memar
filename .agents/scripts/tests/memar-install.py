#!/usr/bin/env python3
"""Tests for the installer, the modules it is split into, and the bootstrap.

    python .agents/scripts/tests/memar-install.py

Nothing here writes to the machine. The scratch folder is inside this folder and
is removed again, every subprocess runs a path that stops before any write, and
the platform's own record of MEMAR_ROOT is read but never written.

What is pinned, and what each pin is for:

  RecordOverSession  The record decides where Memar lives; the process
                     environment is only the copy a program started with. A
                     session opened before the value was written reads nothing
                     and installs again over a record that is already there.
  ProfileRoundTrip  What writes the record on POSIX is what reads it back, so
                     "read and write agree" is a fact and not an intention.
  RecordReadWrite   The Windows pair names one key, not two.
  TemporaryRefusal  Every refusal names the directory the check actually used,
                     and one function decides, so the check and its message
                     cannot read different directories.
  CheckAsksNothing  `--check` asks the check a question and stops there: the
                     refusal it prints is the refusal an install would print,
                     and the machine is untouched.
SiblingSurface    Each sibling imports the module that owns the concern it needs,
                      and no file in this folder is both run and imported — the
                      condition that makes every name here legal. The test
                      resolves each import to a path, because
                      `memar-session.py` and `memar_session.py` differ by one
                      separator and comparing the strings would call the
                      sanctioned pair a violation of the rule it satisfies.
  ObtainsTheArchitecture
                      The bootstrap's own job is the checkout, and it is the
                      whole of it: the steps it prints are the steps its own
                      help declares, in that order, the one clone happens inside
                      the step that says it does, and no file of the
                      architecture is fetched over the network or run from
                      memory to stand in for a checkout.
  StartsFromTheCheckout
                      The installer is started one way only, as a file inside
                      the checkout, so the run has the siblings on disk that it
                      imports; and the folder the bootstrap obtains and the
                      folder the installer records are named by one rule.
  FirstRunInterface  A first-time user's first command: no arguments installs,
                      the documented ways of naming a folder are still accepted,
                      --check still asks its question and writes nothing, and
                      the help says what to run and what is owed afterwards
                      rather than walking through which step clones. A
                      successful run also prints the one command this program
                      runs next; that command is the run's own output.
  PathStaysIdempotent  PATH is read from the record and the session, duplicates
                      and empty parts do not duplicate the entry, and a second
                      run adds nothing.
  EnclosingRepository  A path inside a Memar repository resolves to its nearest
                      ancestor repository, or to None outside one; the caller
                      errors rather than guessing.
  HelpUnchanged     The refactoring changed no consumer's interface: the options
                     and their order, and what each help says to the person
                     running it. The installer's help is the text meant for a
                     caller and carries none of the module docstring, because
                     the docstring is the implementer's and printing it to every
                     installer is how the mechanism reached the help output in
                     the first place.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import memar_repository
import machine.fs_target as target

# The installer is a command, so its name carries a hyphen and no import can
# reach it. The loader is named rather than inferred: a spec inferred from the
# suffix declines a file whose suffix it does not recognize, and a test that
# could not load its own subject would be a test of nothing.
_spec = importlib.util.spec_from_loader(
    "memar_install", SourceFileLoader("memar_install", str(SCRIPTS / "memar-install.py"))
)
memar_install = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(memar_install)

# memar-install.py's own options, in the order argparse prints them, with the
# argument each one takes. Obtaining the checkout is the bootstrap's, so what is
# left here is the recording of one, the check that asks about a folder, the root
# a program asks for, and the two switches that narrow which layers run.
INSTALLER_OPTIONS = (
    ("--register", "PATH"),
    ("--check", "PATH"),
    ("--root", ""),
    ("--machine-only", ""),
    ("--dry-run", ""),
)
# The two layers a bare run asks, by the files it asks. They are child processes
# rather than imports, and this is the pin for that: a hyphenated name is not a
# legal module name, so an import would have forced one of them to be renamed out
# of the form that names its domain first.
INTO_PROJECT = "memar-install-agents.py"
INTO_APPS = "memar-install-apps.py"
IMPORTED_MODULE = re.compile(r"^from ([a-z_][a-z_0-9]*) import ", re.MULTILINE)
# Every name a file imports from a module of this folder, as (module, symbol)
# pairs. The module may carry a dot, since a shelf is a package: what a
# consumer of this folder has to agree on is the dotted path, not a spelling
# without one.
IMPORT_LINE = re.compile(
    r"^from ([a-z_][a-z_0-9.]*) import ([^\n(]+)$", re.MULTILINE
)
# A name with no file beside it is the standard library, and the question below
# is about the names that are this folder's own.
STDLIB = frozenset(sys.stdlib_module_names) | {"__future__"}
BOOTSTRAPS = ("install.sh", "install.ps1")
# A step the header of a bootstrap declares: "  1. Prerequisites — git and ...".
# The shell states its header in `#` comments and PowerShell in a `<# #>` block,
# so the marker is either.
DOCUMENTED_STEP = re.compile(r"^(?:#\s+|\s+)(\d+)\. (.+?)\s*(?:—|-)\s", re.MULTILINE)
# A step the body of a bootstrap prints.
EXECUTED_STEP = re.compile(r'^(?:step|Write-Step) "([^"]+)"$', re.MULTILINE)
# Where the installer lives inside a checkout, which both bootstraps name once.
ARCHITECTURE_ENTRY = ".agents/scripts/memar-install.py"
# The one command that reaches the network: a shallow clone of the repository.
# Anchored to a command of its own, so a header or a refusal that names the
# command is not counted as one.
CLONE = re.compile(r"^(?:\s*&\s*|\s*)git clone[^\n]*$", re.MULTILINE)
# The ways a program used to be handed files over the network and run without a
# folder of its own. Neither belongs in a bootstrap any more.
NETWORK_FETCH = re.compile(r"urlopen|urllib|Invoke-WebRequest|Invoke-RestMethod|\birm\b|\bcurl\b|\bwget\b")
IN_MEMORY = re.compile(r"sys\.modules|ModuleType|exec\(compile")
# The one line in each bootstrap that starts the architecture. PowerShell reads
# names without regard to case, so its line is matched the way PowerShell reads
# it; the shell's is not, because a shell does.
SH_RUN = re.compile(
    r'^"\$PYTHON" "\$checkout/\$ARCHITECTURE_ENTRY" "\$@" \|\| code=\$\?$',
    re.MULTILINE,
)
# Printed once, by a successful run, and not written into a consuming project.
# The program that ran the bootstrap can execute the next line at once; a copy
# of that instruction in the project would keep the old one after it changed.
CONTINUATION = (
    "This program can go on without a restart. "
    "Load the skill by running the next line on its own:"
)
PS_RUN = re.compile(
    r"^& \$python \(Join-Path \$checkout \$ArchitectureEntry\) @forwarded$",
    re.MULTILINE | re.IGNORECASE,
)
# The path rule the bootstrap asks for rather than keeping a second copy of: the
# installer expands `~` and `$NAME` in `machine/fs_target.py`'s `full_path`, so the folder this
# script obtains and the folder the installer records cannot differ.
EXPANSION = re.compile(
    r"'(import os,sys;from pathlib import Path;"
    r"print\(Path\(os\.path\.expandvars\(sys\.argv\[1\]\)\)\.expanduser\(\)\.absolute\(\)\))'"
)


def run_script(name: str, *arguments: str, temp: str | None = None) -> subprocess.CompletedProcess:
    """Run one script with a fixed console width, encoding, and byte-code policy.

    COLUMNS is fixed because argparse wraps its help to the terminal width, and
    an environment variable in the child is fixed because that width is the one
    thing that would make a byte-for-byte comparison of --help meaningless.
    """
    environment = dict(
        os.environ,
        COLUMNS="80",
        PYTHONIOENCODING="utf-8",
        PYTHONDONTWRITEBYTECODE="1",
    )
    if temp is not None:
        environment["TEMP"] = temp
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        capture_output=True,
        env=environment,
    )


def printed(completed: subprocess.CompletedProcess, stream: str = "stdout") -> str:
    """What a run said, as text.

    A Windows console writes CRLF whatever the text says, so the line ending is
    normalized here rather than becoming a difference nobody can read.
    """
    return getattr(completed, stream).decode("utf-8").replace("\r\n", "\n")


class EnclosingRepository(unittest.TestCase):
    """A path inside a repository resolves inward; outside resolves to None."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        # The scratch sits inside this checkout, so a walk past it would reach
        # the real repository; isolated to the scratch, outside resolves None.
        saved = memar_repository.is_memar_repository
        root = self.root.resolve()

        def isolated(path: Path) -> bool:
            try:
                Path(path).resolve().relative_to(root)
            except ValueError:
                return False
            return saved(path)

        memar_repository.is_memar_repository = isolated
        self.addCleanup(setattr, memar_repository, "is_memar_repository", saved)

    def make_repo(self, where: Path) -> Path:
        where.mkdir(parents=True, exist_ok=True)
        (where / "README.md").write_text("# Memar\n", encoding="utf-8")
        (where / "docs").mkdir(exist_ok=True)
        skill = where / ".agents" / "skills" / "memar" / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("# Memar\n", encoding="utf-8")
        return where

    def test_a_file_inside_returns_the_repository(self):
        repo = self.make_repo(self.root / "Memar")
        inner = repo / "docs" / "cognition.md"
        inner.write_text("# Cognition\n", encoding="utf-8")
        self.assertEqual(memar_repository.enclosing_repository(inner), repo)

    def test_a_directory_inside_returns_the_repository(self):
        repo = self.make_repo(self.root / "Memar")
        self.assertEqual(
            memar_repository.enclosing_repository(repo / "docs"), repo
        )

    def test_the_repository_root_returns_itself(self):
        repo = self.make_repo(self.root / "Memar")
        self.assertEqual(memar_repository.enclosing_repository(repo), repo)

    def test_outside_any_repository_returns_none(self):
        plain = self.root / "plain"
        plain.mkdir()
        target = plain / "notes.md"
        target.write_text("# Notes\n", encoding="utf-8")
        self.assertIsNone(memar_repository.enclosing_repository(target))

    def test_a_nested_repository_resolves_to_the_inner_one(self):
        outer = self.make_repo(self.root / "outer")
        inner = self.make_repo(outer / "inner")
        leaf = inner / "docs" / "leaf.md"
        leaf.write_text("# Leaf\n", encoding="utf-8")
        self.assertEqual(memar_repository.enclosing_repository(leaf), inner)

    def test_a_folder_missing_the_skill_is_not_a_repository(self):
        partial = self.root / "partial"
        partial.mkdir()
        (partial / "README.md").write_text("# Memar\n", encoding="utf-8")
        (partial / "docs").mkdir()
        target = partial / "docs" / "note.md"
        target.write_text("# Note\n", encoding="utf-8")
        self.assertIsNone(memar_repository.enclosing_repository(target))

class CheckAsksNothing(unittest.TestCase):
    """`--check` asks the check a question and stops there."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        # A folder that is not under the scratch, so it is not temporary, and is
        # never created: naming it is the whole of what a check does.
        self.kept = SCRIPTS / "a-folder-that-is-not-temporary"
        self.assertFalse(self.kept.exists())

    def scratch_entries(self) -> list[str]:
        return sorted(entry.name for entry in Path(self.scratch.name).iterdir())

    def test_asking_about_a_temporary_folder_refuses_naming_the_same_folder(self):
        # The refusal a check prints and the refusal the mode that records a
        # folder prints come from one check, so both name the folder asked about
        # and the directory the decision was made against. The sentence that
        # follows is the caller's, because what it was about to do differs.
        below = Path(self.scratch.name) / "Memar"
        asked = run_script("memar-install.py", "--check", str(below), temp=self.scratch.name)
        refused = run_script("memar-install.py", "--register", str(below), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 1)
        self.assertEqual(refused.returncode, 1)
        for outcome in (printed(asked, "stderr"), printed(refused, "stderr")):
            self.assertIn(str(below), outcome)
            self.assertIn(str(Path(self.scratch.name).resolve()), outcome)
            self.assertIn("is under the temporary directory", outcome)

    def test_asking_about_a_folder_that_would_be_kept_answers_and_creates_nothing(self):
        asked = run_script("memar-install.py", "--check", str(self.kept), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 0)
        self.assertIn(self.scratch.name, printed(asked))
        self.assertIn("not refused", printed(asked))
        self.assertFalse(self.kept.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_asking_writes_nothing_even_when_the_answer_is_refusal(self):
        below = Path(self.scratch.name) / "Memar"
        run_script("memar-install.py", "--check", str(below), temp=self.scratch.name)
        self.assertFalse(below.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_checking_needs_no_temporary_directory_variable_at_all(self):
        environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8")
        environment.pop("TEMP", None)
        environment.pop("TMPDIR", None)
        asked = subprocess.run(
            [sys.executable, str(SCRIPTS / "memar-install.py"), "--check", str(self.kept)],
            capture_output=True,
            env=environment,
        )
        self.assertEqual(asked.returncode, 0)
        self.assertFalse(self.kept.exists())

class SiblingSurface(unittest.TestCase):
    """A file in this folder may assume its neighbour is on disk beside it.

    The two "into" layers no longer import the installer for a name it happens
    to re-export; each asks the module that owns the concern. What replaced the
    re-export is the pin below: the naming rule's claim that no file is both run
    and imported, which is the condition that makes every name in this folder
    legal.
    """

    def test_the_siblings_import_the_module_that_owns_each_concern(self):
        # Re-exporting a name from the entry point so a sibling can import it
        # from one place is how a file ends up both run and imported, which is
        # the case the naming rule cannot spell. Each asks its owner instead, so
        # what is asserted is which module each name arrives from.
        expected = {
            INTO_PROJECT: {
                "use_utf8_stdio": "memar_console",
                "is_memar_repository": "memar_repository",
                "recorded_value": "machine.env_location",
            },
            INTO_APPS: {
                "use_utf8_stdio": "memar_console",
                "NEVER_COPIED": "memar_copy_excluded",
                "resolve_root": "machine.env_location",
            },
        }
        for name, wanted in expected.items():
            text = (SCRIPTS / name).read_text(encoding="utf-8")
            imports = [
                (owner, symbol.strip())
                for owner, line in IMPORT_LINE.findall(text)
                for symbol in line.split(",")
            ]
            for symbol, owner in wanted.items():
                with self.subTest(name=name, symbol=symbol):
                    # The owner may be one module or a dotted path into a shelf,
                    # so the question is which import carries the symbol — not
                    # that the module happens to be spelled without a dot.
                    self.assertIn(
                        (owner, symbol),
                        imports,
                        f"{symbol} must arrive from {owner}; these are the "
                        f"imports the file has: {imports}",
                    )
            self.assertNotIn("install", [owner for owner, _ in imports])

    def test_no_sibling_reaches_through_the_entry_point_anymore(self):
        for name in (INTO_PROJECT, INTO_APPS):
            with self.subTest(name=name):
                self.assertNotIn(
                    "memar_install.",
                    (SCRIPTS / name).read_text(encoding="utf-8"),
                )

    def test_a_file_with_a_command_line_is_hyphenated_and_one_without_is_imported(self):
        # The condition the naming rule rests on, and what decides which form a
        # name takes: a file that declares a command line is reached by running
        # it, and a file that declares none is reached by importing it. A file
        # that was both would have no legal spelling — a hyphen is not a legal
        # module name — so it would either be renamed into the wrong form or need
        # a defended exception.
        for path in sorted(SCRIPTS.rglob("*.py")):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            has_command_line = 'if __name__ == "__main__"' in text
            with self.subTest(path=path.name):
                if has_command_line:
                    self.assertNotIn(
                        "_",
                        path.stem,
                        f"{path.name} declares a command line, so its name carries "
                        "the hyphen that separates its domain from its subject",
                    )
                else:
                    self.assertNotIn(
                        "-",
                        path.stem,
                        f"{path.name} declares no command line, so it is reached by "
                        "an import and cannot carry a hyphen",
                    )

    def test_no_file_here_is_both_run_and_imported(self):
        for path in sorted(SCRIPTS.rglob("*.py")):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if 'if __name__ == "__main__"' not in text:
                continue
            # Resolved to a path, not compared as a name: `memar-session.py` and
            # `memar_session.py` differ by one separator, and `from memar_session
            # import ...` reaches the second file, not the first. Comparing the
            # strings would report the sanctioned pair as a violation of the rule
            # the pair exists to satisfy.
            with self.subTest(path=path.name):
                self.assertFalse(
                    any(self.resolves_to(other, path) for other in SCRIPTS.rglob("*.py") if other != path),
                    f"{path.name} is both run and imported, so its name has no legal form",
                )

    def resolves_to(self, source: Path, target: Path) -> bool:
        """Whether an import in `source` names `target` on disk.

        An import of a dotted path from the top of this folder resolves to
        `<scripts>/<first part>/<rest>.py`; a bare name resolves beside this
        folder's root. Either way the answer is a path, and a file whose name
        carries a hyphen is named by no import at all — which is the property
        the rule leans on rather than a coincidence.
        """
        text = source.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^\s*(?:import ([A-Za-z_][\w.]*)|from ([A-Za-z_][\w.]*) import )",
            text,
            re.MULTILINE,
        ):
            dotted = match.group(1) or match.group(2)
            parts = dotted.split(".")
            resolved = SCRIPTS.joinpath(*parts).with_suffix(".py")
            if resolved.resolve() == target.resolve():
                return True
        return False

    def test_every_module_the_entry_point_imports_is_a_file_beside_it(self):
        # The architecture is run from a checkout, so an import of a sibling is
        # answered from the disk beside the entry point. A name with no file
        # beside it is the standard library, and the question is about the rest.
        for module in IMPORTED_MODULE.findall((SCRIPTS / "memar-install.py").read_text(encoding="utf-8")):
            if module in STDLIB:
                continue
            self.assertTrue((SCRIPTS / f"{module}.py").is_file(), module)

class ObtainsTheArchitecture(unittest.TestCase):
    """The bootstrap's own job is the checkout, and it is the whole of it."""

    def source(self, bootstrap: str) -> str:
        return (SCRIPTS / bootstrap).read_text(encoding="utf-8")

    def test_the_steps_it_prints_are_the_steps_its_help_declares(self):
        for bootstrap in BOOTSTRAPS:
            documented = DOCUMENTED_STEP.findall(self.source(bootstrap))
            executed = EXECUTED_STEP.findall(self.source(bootstrap))
            self.assertTrue(documented, f"{bootstrap} declares its steps")
            self.assertEqual([name for _, name in documented], executed, bootstrap)
            numbers = [number for number, _ in documented]
            self.assertEqual(numbers, [str(n) for n in range(1, len(numbers) + 1)], bootstrap)

    def test_both_bootstraps_declare_and_print_the_same_steps(self):
        declared = {
            bootstrap: [name for _, name in DOCUMENTED_STEP.findall(self.source(bootstrap))]
            for bootstrap in BOOTSTRAPS
        }
        self.assertEqual(declared["install.sh"], declared["install.ps1"])
        self.assertEqual(declared["install.sh"], [name for name in EXECUTED_STEP.findall(self.source("install.ps1"))])

    def test_the_clone_happens_inside_the_step_that_says_it_does(self):
        # What it does, in order: prerequisites, then the architecture, then the
        # run. A clone anywhere else would be a step the help does not declare.
        for bootstrap, pattern in (
            ("install.sh", r'^step "(.*?)"$'),
            ("install.ps1", r'^Write-Step "(.*?)"$'),
        ):
            text = self.source(bootstrap)
            labels = re.findall(pattern, text, re.MULTILINE)
            self.assertEqual(
                labels, ["Prerequisites", "The architecture", "The installer"], bootstrap
            )
            clone = CLONE.search(text)
            self.assertIsNotNone(clone, bootstrap)
            self.assertLess(text.index('"The architecture"'), clone.start(), bootstrap)
            self.assertLess(clone.start(), text.index('"The installer"'), bootstrap)

    def test_a_first_run_reaches_the_network_once_and_fetches_no_file(self):
        # One clone, and no other way of reaching the network at all: a file of
        # the architecture is never fetched, so a run with nothing on disk costs
        # the clone and nothing else. The one program a bootstrap runs that it
        # did not fetch is the path rule, which asks the installer rather than
        # keeping a second copy of it.
        for bootstrap in BOOTSTRAPS:
            text = self.source(bootstrap)
            self.assertIsNone(NETWORK_FETCH.search(text), f"{bootstrap} fetches a file")
            self.assertIsNone(IN_MEMORY.search(text), f"{bootstrap} runs a fetched file")
            self.assertEqual(len(CLONE.findall(text)), 1, f"{bootstrap} clones once")
            self.assertEqual(
                re.findall(r"-c '([^']*)'", text),
                EXPANSION.findall(text),
                f"{bootstrap} runs only the path rule inline",
            )

    def test_a_run_that_named_no_folder_only_fetches_when_it_has_no_checkout(self):
        # The folder a run was told about is the one it pulls or refuses. A run
        # that named none is handed to the installer with nothing to fetch,
        # because whether Memar is already here is the installer's question, and
        # asking it from a shell would mean answering it from this session's copy
        # of the variable rather than from the record.
        for bootstrap, guards in (
            ("install.sh", ('if [ -n "$obtain_it" ]; then', 'if [ -n "$at_hand" ] && [ -z "$recorded" ]; then')),
            ("install.ps1", ("if ($ObtainIt) {", "if ($AtHand -and -not $Recorded) {")),
        ):
            text = self.source(bootstrap)
            for guard in guards:
                self.assertTrue(guard in text, f"{bootstrap} has no guard {guard}")

    def test_a_run_that_named_no_folder_hands_the_installer_nothing(self):
        # The installer's arguments are rebuilt from the mode, so a mode that
        # names no folder reaches it with no argument at all: the installer is
        # the one that answers whether Memar is already here, and this shell's
        # copy of the variable is never handed to it as an answer.
        shell = self.source("install.sh").split('set --\ncase "$mode" in', 1)
        self.assertEqual(len(shell), 2, "install.sh rebuilds the installer's arguments")
        self.assertNotIn("*)", shell[1].split("esac", 1)[0])
        powershell = self.source("install.ps1").split("$forwarded = @()", 1)
        self.assertEqual(len(powershell), 2, "install.ps1 rebuilds the installer's arguments")
        self.assertNotIn("default", powershell[1])
        for bootstrap in BOOTSTRAPS:
            self.assertNotIn('"--register" "$recorded"', self.source(bootstrap), bootstrap)

    def test_the_clone_is_shallow_and_of_the_repository_the_manifest_names(self):
        manifest = (SCRIPTS.parents[1] / "manifest.yaml").read_text(encoding="utf-8")
        named = re.search(r"^codeRepository: (\S+)$", manifest, re.MULTILINE)
        self.assertIsNotNone(named, "manifest.yaml names the repository")
        for bootstrap, pattern in (
            ("install.sh", r'^REPOSITORY_URL="([^"]*)"$'),
            ("install.ps1", r'^\$RepositoryUrl = "([^"]*)"$'),
        ):
            text = self.source(bootstrap)
            self.assertEqual(
                re.findall(pattern, text, re.MULTILINE), [f"{named.group(1)}.git"], bootstrap
            )
            clone = CLONE.search(text)
            self.assertIsNotNone(clone, bootstrap)
            self.assertIn("--depth 1", clone.group(0), bootstrap)

    def test_both_bootstraps_name_the_installers_place_in_a_checkout_the_same_way(self):
        for bootstrap, pattern in (
            ("install.sh", r'^(?:ARCHITECTURE_ENTRY|INSTALL_DIRNAME)="([^"]*)"$'),
            ("install.ps1", r"^\$(?:ArchitectureEntry|InstallDirname) = \"([^\"]*)\"$"),
        ):
            declared = re.findall(pattern, self.source(bootstrap), re.MULTILINE)
            self.assertEqual(declared, [ARCHITECTURE_ENTRY, "Memar"], bootstrap)

class StartsFromTheCheckout(unittest.TestCase):
    """The run is the checkout's own file, with its siblings on disk."""

    def source(self, bootstrap: str) -> str:
        return (SCRIPTS / bootstrap).read_text(encoding="utf-8")

    def test_a_successful_run_prints_how_this_program_goes_on(self):
        # One sentence, the same in both files, and one command after it. The
        # command names the checkout this run settled and the interpreter it
        # used, so this program can load the skill without waiting for a
        # restart to put `memar` on PATH. It is printed here rather than
        # written into a consuming project, because the command is allowed to
        # change and a project would keep the old one.
        for bootstrap in BOOTSTRAPS:
            text = self.source(bootstrap)
            self.assertEqual(text.count(CONTINUATION), 1, bootstrap)
            self.assertIn("memar-content.py", text)
            self.assertIn("path .agents/skills/memar/SKILL.md", text)
            command = text.split(CONTINUATION, 1)[1].lstrip("\n")
            command = command.split("\n", 1)[0]
            self.assertIn("memar-content.py", command, bootstrap)
            self.assertNotIn("\n", command)

    def test_the_installer_is_started_one_way_and_from_the_checkout(self):
        for bootstrap, pattern in (("install.sh", SH_RUN), ("install.ps1", PS_RUN)):
            self.assertEqual(len(pattern.findall(self.source(bootstrap))), 1, bootstrap)

    def test_nothing_stands_in_for_the_siblings_on_disk(self):
        for bootstrap in BOOTSTRAPS:
            self.assertIsNone(IN_MEMORY.search(self.source(bootstrap)), bootstrap)

    def test_the_bootstrap_and_the_installer_name_a_folder_the_same_way(self):
        # One rule for `~` and `$NAME`, asked of the same interpreter: the folder
        # the bootstrap obtains and the folder the installer records are one.
        asked = EXPANSION.findall(self.source("install.sh"))
        self.assertEqual(len(asked), 1, "install.sh")
        self.assertEqual(EXPANSION.findall(self.source("install.ps1")), asked, "install.ps1")
        for value in ("~", str(Path.home() / "Memar"), "folder/below/here"):
            answered = subprocess.run(
                [sys.executable, "-c", asked[0], value], capture_output=True
            )
            self.assertEqual(answered.returncode, 0, value)
            self.assertEqual(
                answered.stdout.decode("utf-8").strip(), str(target.full_path(value)), value
            )

    def test_the_bootstrap_and_the_installer_default_to_the_same_folder(self):
        self.assertEqual(target.default_target(), Path.home() / target.INSTALL_DIRNAME)
        self.assertEqual(target.INSTALL_DIRNAME, "Memar")
        for bootstrap, pattern in (
            ("install.sh", r'^INSTALL_DIRNAME="([^"]*)"$'),
            ("install.ps1", r'^\$InstallDirname = "([^"]*)"$'),
        ):
            self.assertEqual(
                re.findall(pattern, self.source(bootstrap), re.MULTILINE),
                [target.INSTALL_DIRNAME],
                bootstrap,
            )

class FirstRunInterface(unittest.TestCase):
    """A first-time user's first command, on this machine."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.saved_temp = os.environ.get("TEMP")
        self.addCleanup(self.restore_temp)
        os.environ["TEMP"] = self.scratch.name

    def restore_temp(self) -> None:
        if self.saved_temp is None:
            os.environ.pop("TEMP", None)
        else:
            os.environ["TEMP"] = self.saved_temp

    def sh(self, *arguments: str) -> subprocess.CompletedProcess:
        shell = shutil.which("sh") or r"C:\Program Files\Git\bin\sh.exe"
        if not Path(shell).is_file():
            self.skipTest("no POSIX shell on this machine")
        return subprocess.run(
            [shell, str(SCRIPTS / "install.sh"), *arguments],
            capture_output=True,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )

    def test_the_posix_bootstrap_parses(self):
        shell = shutil.which("sh") or r"C:\Program Files\Git\bin\sh.exe"
        if not Path(shell).is_file():
            self.skipTest("no POSIX shell on this machine")
        parsed = subprocess.run([shell, "-n", str(SCRIPTS / "install.sh")], capture_output=True)
        self.assertEqual(parsed.returncode, 0, parsed.stderr.decode("utf-8", "replace"))

    def test_the_windows_bootstrap_parses(self):
        shell = shutil.which("powershell") or shutil.which("pwsh")
        if not shell:
            self.skipTest("no PowerShell on this machine")
        # Parse only: the file is read, never run and never written.
        command = (
            "$errors = $null; "
            f"[System.Management.Automation.Language.Parser]::ParseFile("
            f"'{SCRIPTS / 'install.ps1'}', [ref]$null, [ref]$errors) | Out-Null; "
            "if ($errors.Count) { $errors | ForEach-Object { $_.Message }; exit 1 }"
        )
        parsed = subprocess.run([shell, "-NoProfile", "-Command", command], capture_output=True)
        self.assertEqual(parsed.returncode, 0, parsed.stdout.decode("utf-8", "replace"))

    def test_help_names_the_ways_of_naming_a_folder_and_not_the_mechanism(self):
        # A person running the bootstrap for the first time needs the invocations
        # and needs to know a restart is owed. The three-step walkthrough is the
        # implementer's: it names which step clones and which hands off, and a
        # reader who cannot act on that has been shown the inside of the run.
        shown = printed(self.sh("--help"))
        for option in ("--path", "--register", "--check"):
            self.assertIn(option, shown)
        self.assertIn("restart your shell", shown)
        # The command this program runs next is the run's output, not the help.
        # Help still says a shell and an editor that are already open restart.
        self.assertNotIn(CONTINUATION, shown)

    def test_the_help_does_not_carry_the_runs_mechanism(self):
        shown = printed(self.sh("--help"))
        for phrase in (
            "Prerequisites",
            "The architecture",
            "One mechanism decides where Memar lives",
            "git clone --depth 1",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, shown)

    def test_the_mechanism_is_still_in_the_file_for_whoever_opens_it(self):
        # Not a second copy: the step-by-step the run prints, declared once in
        # the file. Removing it from the help must not have removed it at all.
        text = (SCRIPTS / "install.sh").read_text(encoding="utf-8")
        for phrase in ("Prerequisites", "The architecture", "One mechanism decides"):
            self.assertIn(phrase, text)

    def test_an_unknown_argument_is_refused_before_anything_is_obtained(self):
        refused = self.sh("--not-an-option")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("unknown argument", printed(refused, "stderr"))
        self.assertNotIn("git clone", printed(refused))

    def test_an_option_without_its_folder_is_refused(self):
        refused = self.sh("--path")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("need a path", printed(refused, "stderr"))
        self.assertNotIn("git clone", printed(refused))

    def test_a_check_asks_the_architecture_and_writes_nothing(self):
        # The whole chain, without an install: the script finds the checkout it
        # is in, runs the installer from it, and the installer answers the check
        # and stops. Nothing is cloned, so the answer arrives with no network.
        below = Path(self.scratch.name) / "Memar"
        asked = self.sh("--check", str(below))
        self.assertEqual(asked.returncode, 1)
        self.assertIn(str(Path(self.scratch.name).resolve()), printed(asked, "stderr"))
        self.assertIn("temporary directory", printed(asked))
        self.assertNotIn("git clone", printed(asked))
        self.assertFalse(below.exists())
        self.assertEqual(sorted(entry.name for entry in Path(self.scratch.name).iterdir()), [])

    def test_a_check_of_a_folder_that_would_be_kept_answers_and_creates_nothing(self):
        kept = SCRIPTS / "a-folder-that-is-not-temporary"
        self.assertFalse(kept.exists())
        asked = self.sh("--check", str(kept))
        self.assertEqual(asked.returncode, 0, printed(asked, "stderr"))
        self.assertIn("not refused", printed(asked))
        self.assertNotIn(CONTINUATION, printed(asked))
        self.assertFalse(kept.exists())

class HelpUnchanged(unittest.TestCase):
    """The refactoring changed no consumer's interface.

    Not by pinning the bytes of a `--help`. A byte pin over a file this change
    edits is a pin that has to be refreshed by the same change that should have
    made a reader stop, which is why the earlier one was refreshed three times in
    two sessions and then trusted on neither platform: argparse wraps help to the
    terminal width, so the bytes are a property of the machine as much as of the
    file. What is pinned here is the interface a consumer names — the options and
    their order — and each tool's own subject, in whatever wording it uses.
    """

    def test_each_installed_tool_answers_a_help_request(self):
        for name in (INTO_PROJECT, INTO_APPS):
            with self.subTest(name=name):
                answered = printed(run_script(name, "--help"))
                self.assertIn("usage:", answered)

    def test_the_installer_still_takes_the_same_arguments_in_the_same_order(self):
        shown = printed(run_script("memar-install.py", "--help"))
        options = re.findall(r"^  (--\S+)( \S+)?  ", shown, re.MULTILINE)
        self.assertEqual(
            tuple((option, (argument or "").strip()) for option, argument in options),
            INSTALLER_OPTIONS,
        )

    def test_the_installer_help_is_the_text_meant_for_a_caller(self):
        # The help is `DESCRIPTION`, not the module docstring: the docstring is
        # addressed to whoever opens the file and is the reasoning behind the run.
        # Pinning the docstring here is what made the two the same text, which is
        # how the mechanism ended up printed to every person installing Memar.
        shown = printed(run_script("memar-install.py", "--help"))
        self.assertIn(memar_install.DESCRIPTION.strip(), shown)
        self.assertNotIn(memar_install.__doc__.strip(), shown)

    def test_the_installer_help_carries_no_mechanism(self):
        shown = printed(run_script("memar-install.py", "--help"))
        for phrase in (
            "memar_repository.py",
            "machine/env_location.py",
            "machine/fs_lock.py",
            "advisory",
            "idempotent",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, shown)

    def test_the_installer_help_says_what_the_person_must_do_afterwards(self):
        # The UserActionNote. A run that writes an environment variable and says
        # nothing about the restart leaves every caller with a `memar` that is not
        # found until they happen to open a new terminal.
        shown = printed(run_script("memar-install.py", "--help"))
        self.assertIn("restart", shown)
        self.assertIn("--check", shown)

class BareRunInstallsEveryLayer(unittest.TestCase):
    """One bare run settles the machine, this project, and the agent apps.

    The order is the dependency rather than a preference: the app layer needs the
    location the machine layer records, so it is asked second and says so itself
    when there is no location. What it must never do is go past installing, so a
    layer that cannot apply reports and returns rather than failing the run.
    """

    def setUp(self) -> None:
        self.children: list[tuple[Path, list[str]]] = []

        def record(script: Path, arguments: list[str], label: str) -> subprocess.CompletedProcess:
            self.children.append((script, list(arguments)))
            return subprocess.CompletedProcess([], 0, b"", b"")

        self.record = record

    def collect(self) -> None:
        saved = memar_install.run_child
        memar_install.run_child = self.record
        self.addCleanup(setattr, memar_install, "run_child", saved)

    def test_both_layers_are_asked_and_in_that_order(self):
        self.collect()
        memar_install.into_project_and_apps()
        self.assertEqual(
            [script.name for script, _ in self.children],
            [INTO_PROJECT, INTO_APPS],
        )

    def test_a_layer_is_asked_by_the_file_the_naming_rule_admits(self):
        # Both are hyphenated, which is why they are run rather than imported.
        for script in (memar_install.INTO_PROJECT, memar_install.INTO_APPS):
            with self.subTest(script=script.name):
                self.assertEqual(script.suffix, ".py")
                self.assertEqual(script.name, script.name.replace("_", "-"))
                self.assertTrue(script.is_file())

    def test_a_dry_run_is_forwarded_to_the_layers(self):
        # The machine layer writes a value, so it is never a dry run; what a
        # dry run previews is what the project and app layers would write.
        self.collect()
        memar_install.into_project_and_apps(["--dry-run"])
        self.assertEqual([arguments for _, arguments in self.children], [["--dry-run"], ["--dry-run"]])

    def test_a_layer_that_does_not_apply_does_not_stop_the_run(self):
        self.collect()
        # The app layer's dependency is the machine layer, not the project
        # layer, so a project that refused must not cost the skill its copies.
        memar_install.into_project_and_apps()
        self.assertEqual(len(self.children), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
