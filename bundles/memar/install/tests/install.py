#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the installer, `memar install` in `bundles/memar/install/install.py`, the modules it is split into, and the bootstrap.

    python bundles/memar/install/tests/install.py

Nothing here writes outside its scratch folder. The scratch folder is made
under the one `machine/fs_test_scratch.py` names, and is removed again; every
subprocess runs a path that stops before any write, and
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
SiblingSurface    Each layer imports the module that owns the concern it needs,
                      and no file in this folder is both run and imported — the
                      condition that makes every name here legal. The test
                      resolves each import to a path, because a run file and
                      a module may differ by one separator and comparing the
                      strings would call that sanctioned pair a violation of
                      the rule it satisfies.
  ObtainsTheArchitecture
                      The bootstrap's own job is the checkout, and it is the
                      whole of it: the steps it prints are the steps its own
                      help declares, in that order, the one clone happens inside
                      the step that says it does, and no file of the
                      architecture is fetched over the network or run from
                      memory to stand in for a checkout.
  StartsFromTheCheckout
                      The installer is started one way only, as `memar install`
                      through the launcher inside the checkout, so the run has
                      the siblings on disk that it imports, and with the daily
                      update kept from starting under it; and the folder the
                      bootstrap obtains and the folder the installer records
                      are named by one rule.
  FirstRunInterface  A first-time user's first command: no arguments installs,
                      the documented ways of naming a folder are still accepted,
                      a check through either bootstrap reaches `memar install`,
                      which asks its question and writes nothing, and
                      the help says what to run and what is owed afterwards
                      rather than walking through which step clones. A
                      successful run also prints the one command this program
                      runs next; that command is the run's own output.
  PathStaysIdempotent  PATH is read from the record and the session, duplicates
                      and empty parts do not duplicate the entry, and a second
                      run adds nothing.
  DeveloperIsMarked  `--developer` marks the recorded checkout as a development
                      checkout in its own git configuration, leaves its working
                      tree as it was, says how to undo it, and refuses a folder
                      that is not a Memar repository.
  HelpUnchanged     The refactoring changed no consumer's interface: the options
                     and their order, and what each help says to the person
                     running it. The installer's help is the text meant for a
                     caller and carries none of the module docstring, because
                     the docstring is the implementer's and printing it to every
                     installer is how the mechanism reached the help output in
                     the first place.
  InstallingRegistersTheProject
                      Installing into a project registers it with Memar under
                      its folder's name, once; one already registered is left
                      as it is, a name another project holds is reported and
                      nothing is renamed, and a dry run writes no registry.
  BareRunInstallsEveryLayer
                      The machine layer, then the project, then the agent apps,
                      each asked in this process; a layer that stops does not
                      stop the ones after it, and a dry run reaches the two
                      that write into a project and the apps.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
TOP = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.env_location as location
import machine.fs_target as target
import bundles.memar.install.install as memar_install
import bundles.memar.install.services.apps as apps_layer
import bundles.memar.install.services.machine as machine_layer
import bundles.memar.install.services.project as project_layer
import bundles.memar.update.services.checkout as update_checkout
from machine.fs_memar_repository import SKILL_MARKER

LAUNCHER = SCRIPTS / "memar"
# `memar install`'s own options, in the order argparse prints them, with the
# argument each one takes. Obtaining the checkout is the bootstrap's, so what is
# left here is the recording of one, the check that asks about a folder, the root
# a program asks for, and the two switches that narrow which layers run.
INSTALLER_OPTIONS = (
    ("--register", "PATH"),
    ("--check", "PATH"),
    ("--root", ""),
    ("--developer", ""),
    ("--project", "NAME"),
    ("--project-path", "PATH"),
    ("--machine-only", ""),
    ("--dry-run", ""),
)
# The two layers a bare run asks after the machine layer, by the services that
# hold them. They are imported and asked in this process, so neither declares a
# command line of its own.
INTO_PROJECT = "bundles/memar/install/services/project.py"
INTO_APPS = "bundles/memar/install/services/apps.py"
# An import anywhere in a file, a run's local imports included.
IMPORTED_MODULE = re.compile(r"^\s*from ([a-z_][a-z_0-9.]*) import ", re.MULTILINE)
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
# Where the launcher the installer is reached through lives inside a checkout,
# which both bootstraps name once.
ARCHITECTURE_ENTRY = ".agents/scripts/memar"
# The one command that reaches the network: a shallow clone of the repository.
# Anchored to a command of its own, so a header or a refusal that names the
# command is not counted as one.
CLONE = re.compile(r"^(?:\s*&\s*|\s*)git clone[^\n]*$", re.MULTILINE)
# The ways a program used to be handed files over the network and run without a
# folder of its own. Neither belongs in a bootstrap any more.
NETWORK_FETCH = re.compile(r"urlopen|urllib|Invoke-WebRequest|Invoke-RestMethod|\birm\b|\bcurl\b|\bwget\b")
IN_MEMORY = re.compile(r"sys\.modules|ModuleType|exec\(compile")
# The one line in each bootstrap that starts the architecture: `memar install`,
# through the checkout's launcher, with the daily update kept from starting
# under the install. PowerShell reads names without regard to case, so its line
# is matched the way PowerShell reads it; the shell's is not, because a shell
# does.
SH_RUN = re.compile(
    r'^MEMAR_NO_AUTO_UPDATE=1 "\$PYTHON" "\$checkout/\$ARCHITECTURE_ENTRY" install "\$@" \|\| code=\$\?$',
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
    r"^\$env:MEMAR_NO_AUTO_UPDATE = \"1\"\ntry \{\n"
    r"    & \$python \(Join-Path \$checkout \$ArchitectureEntry\) install @forwarded\n"
    r"(?:.*\n)*?\} finally \{\n    \$env:MEMAR_NO_AUTO_UPDATE = \$autoUpdate\n\}$",
    re.MULTILINE | re.IGNORECASE,
)
# What the installer prints when a check reaches it, and only it: a bootstrap
# that printed this reached `memar install`.
REACHED_THE_INSTALLER = "==> Checking a target"
# The path rule the bootstrap asks for rather than keeping a second copy of: the
# installer expands `~` and `$NAME` in `machine/fs_target.py`'s `full_path`, so the folder this
# script obtains and the folder the installer records cannot differ.
EXPANSION = re.compile(
    r"'(import os,sys;from pathlib import Path;"
    r"print\(Path\(os\.path\.expandvars\(sys\.argv\[1\]\)\)\.expanduser\(\)\.absolute\(\)\))'"
)


def run_install(*arguments: str, temp: str | None = None) -> subprocess.CompletedProcess:
    """Run `memar install` with a fixed console width, encoding, and byte-code policy.

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
        [sys.executable, str(LAUNCHER), "install", *arguments],
        capture_output=True,
        env=environment,
    )


def printed(completed: subprocess.CompletedProcess, stream: str = "stdout") -> str:
    """What a run said, as text.

    A Windows console writes CRLF whatever the text says, so the line ending is
    normalized here rather than becoming a difference nobody can read.
    """
    return getattr(completed, stream).decode("utf-8").replace("\r\n", "\n")


class CheckAsksNothing(unittest.TestCase):
    """`--check` asks the check a question and stops there."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
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
        asked = run_install("--check", str(below), temp=self.scratch.name)
        refused = run_install("--register", str(below), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 1)
        self.assertEqual(refused.returncode, 1)
        for outcome in (printed(asked, "stderr"), printed(refused, "stderr")):
            self.assertIn(str(below), outcome)
            self.assertIn(str(Path(self.scratch.name).resolve()), outcome)
            self.assertIn("is under the temporary directory", outcome)

    def test_asking_about_a_folder_that_would_be_kept_answers_and_creates_nothing(self):
        asked = run_install("--check", str(self.kept), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 0)
        self.assertIn(str(Path(self.scratch.name).resolve()), printed(asked))
        self.assertIn("not refused", printed(asked))
        self.assertFalse(self.kept.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_asking_writes_nothing_even_when_the_answer_is_refusal(self):
        below = Path(self.scratch.name) / "Memar"
        run_install("--check", str(below), temp=self.scratch.name)
        self.assertFalse(below.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_checking_needs_no_temporary_directory_variable_at_all(self):
        environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8")
        environment.pop("TEMP", None)
        environment.pop("TMPDIR", None)
        asked = subprocess.run(
            [sys.executable, str(LAUNCHER), "install", "--check", str(self.kept)],
            capture_output=True,
            env=environment,
        )
        self.assertEqual(asked.returncode, 0)
        self.assertFalse(self.kept.exists())

class SiblingSurface(unittest.TestCase):
    """A file in this folder may assume its neighbour is on disk beside it.

    The two "into" layers do not import the installer for a name it happens to
    re-export; each asks the module that owns the concern. What replaced the
    re-export is the pin below: the naming rule's claim that no file is both run
    and imported, which is the condition that makes every name in this folder
    legal.
    """

    def test_the_siblings_import_the_module_that_owns_each_concern(self):
        # Re-exporting a name from the entry point so a sibling can import it
        # from one place makes the entry point a second owner of the name. Each
        # asks its owner instead, so what is asserted is which module each name
        # arrives from.
        expected = {
            INTO_PROJECT: {
                "is_memar_repository": "machine.fs_memar_repository",
                "recorded_value": "machine.env_location",
            },
            INTO_APPS: {
                "soft_delete": "machine.fs_trash",
                "WINDOWS_BOOTSTRAP": "bundles.memar.install.services.project",
                "POSIX_BOOTSTRAP": "bundles.memar.install.services.project",
                "resolve_root": "machine.env_location",
            },
        }
        for name, wanted in expected.items():
            text = (TOP / name).read_text(encoding="utf-8")
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
            self.assertNotIn("bundles.memar.install.install", [owner for owner, _ in imports])

    def test_no_sibling_reaches_through_the_entry_point_anymore(self):
        for name in (INTO_PROJECT, INTO_APPS):
            with self.subTest(name=name):
                self.assertIsNone(
                    re.search(r"services\.install\b(?!_)|import install\b", (TOP / name).read_text(encoding="utf-8")),
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
            # Resolved to a path, not compared as a name: a run file `memar-x.py`
            # and a module `memar_x.py` differ by one separator, and `from memar_x
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

    def test_every_module_the_installer_imports_is_a_file_in_this_folder(self):
        # The architecture is run from a checkout, so an import of a sibling is
        # answered from the disk the launcher sits on. A name with no file in
        # this folder is the standard library, and the question is about the rest.
        for name in ("bundles/memar/install/install.py", "bundles/memar/install/services/machine.py", INTO_PROJECT, INTO_APPS):
            for module in IMPORTED_MODULE.findall((TOP / name).read_text(encoding="utf-8")):
                if module.partition(".")[0] in STDLIB:
                    continue
                with self.subTest(name=name, module=module):
                    found = (TOP if module.partition(".")[0] in ("bundles", "modules") else SCRIPTS).joinpath(*module.split("."))
                    self.assertTrue(found.with_suffix(".py").is_file() or found.is_dir(), module)

    def test_the_verb_imports_nothing_heavy_until_it_runs(self):
        # Every `memar` invocation imports every service to learn what each verb
        # accepts, so the verb's own module keeps the machine and the layers out
        # of its top level; its run imports them.
        text = (TOP / "bundles/memar/install/install.py").read_text(encoding="utf-8")
        top_level = re.findall(r"^(?:from ([\w.]+) import|import ([\w.]+))", text, re.MULTILINE)
        self.assertEqual(
            [module for pair in top_level for module in pair if module and module.partition(".")[0] not in STDLIB],
            [],
        )

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
            command = text.split(CONTINUATION, 1)[1].lstrip("\n")
            command = command.split("\n", 1)[0]
            self.assertRegex(command, r'scripts[/\\]memar" content path \.agents/skills/memar/SKILL\.md$', bootstrap)
            self.assertNotIn(".py", command, bootstrap)

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
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
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

    def ps(self, *arguments: str) -> subprocess.CompletedProcess:
        shell = shutil.which("powershell") or shutil.which("pwsh")
        if not shell:
            self.skipTest("no PowerShell on this machine")
        return subprocess.run(
            [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPTS / "install.ps1"), *arguments],
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

    def test_the_windows_help_is_its_help_block_from_the_synopsis_to_the_notes(self):
        # The block is found, not counted to: a header above it, such as the
        # license line, must not reach the output nor cut it short.
        shell = shutil.which("powershell") or shutil.which("pwsh")
        if not shell:
            self.skipTest("no PowerShell on this machine")
        asked = subprocess.run(
            [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPTS / "install.ps1"), "-Help"],
            capture_output=True,
        )
        self.assertEqual(asked.returncode, 0, asked.stderr.decode("utf-8", "replace"))
        shown = asked.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
        self.assertTrue(shown.startswith(".SYNOPSIS\n"), shown[:80])
        for option in ("-Path", "-Register", "-Check", "restart your shell"):
            with self.subTest(option=option):
                self.assertIn(option, shown)
        for phrase in ("LEGAL", "<#", "#>", ".NOTES", "Prerequisites", "One mechanism decides"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, shown)

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
        # is in, hands the check to `memar install` through its launcher, and the
        # installer answers the check and stops. Nothing is cloned, so the answer
        # arrives with no network.
        below = Path(self.scratch.name) / "Memar"
        for bootstrap, asked in (("install.sh", lambda: self.sh("--check", str(below))),
                                 ("install.ps1", lambda: self.ps("-Check", str(below)))):
            with self.subTest(bootstrap=bootstrap):
                asked = asked()
                self.assertEqual(asked.returncode, 1, printed(asked, "stderr"))
                self.assertIn(REACHED_THE_INSTALLER, printed(asked))
                self.assertIn(str(Path(self.scratch.name).resolve()), printed(asked, "stderr"))
                self.assertIn("temporary directory", printed(asked))
                self.assertNotIn("git clone", printed(asked))
                self.assertFalse(below.exists())
                self.assertEqual(sorted(entry.name for entry in Path(self.scratch.name).iterdir()), [])

    def test_a_check_of_a_folder_that_would_be_kept_answers_and_creates_nothing(self):
        kept = SCRIPTS / "a-folder-that-is-not-temporary"
        self.assertFalse(kept.exists())
        for bootstrap, asked in (("install.sh", lambda: self.sh("--check", str(kept))),
                                 ("install.ps1", lambda: self.ps("-Check", str(kept)))):
            with self.subTest(bootstrap=bootstrap):
                asked = asked()
                self.assertEqual(asked.returncode, 0, printed(asked, "stderr"))
                self.assertIn(REACHED_THE_INSTALLER, printed(asked))
                self.assertIn("not refused", printed(asked))
                self.assertNotIn(CONTINUATION, printed(asked))
                self.assertFalse(kept.exists())

class BootstrapNamesTheProject(unittest.TestCase):
    """The installer never reads the folder it runs in, so the bootstrap names the project it was started for."""

    def source(self, bootstrap: str) -> str:
        return (SCRIPTS / bootstrap).read_text(encoding="utf-8")

    def test_each_bootstrap_documents_and_takes_a_project(self):
        for bootstrap, option in (("install.sh", "--project-path"), ("install.ps1", "-ProjectPath")):
            with self.subTest(bootstrap=bootstrap):
                text = self.source(bootstrap)
                self.assertGreater(text.count(option), 2, bootstrap)
                self.assertNotIn("into the project you are in", text, bootstrap)

    def test_the_project_is_forwarded_to_the_installer_as_a_path(self):
        shell = self.source("install.sh").split("set --" + chr(10) + 'case "$mode" in', 1)[1]
        self.assertIn('--project-path "$(absolute_path "$project")"', shell)
        powershell = self.source("install.ps1").split("$forwarded = @()", 1)[1]
        self.assertIn('"--project-path"', powershell)
        self.assertIn("ConvertTo-AbsolutePath $ProjectPath", powershell)

    def test_a_project_is_never_taken_from_the_folder_the_script_runs_in(self):
        for bootstrap in BOOTSTRAPS:
            with self.subTest(bootstrap=bootstrap):
                text = self.source(bootstrap)
                self.assertNotRegex(text, r"\$PWD|Get-Location", bootstrap)

    def test_a_project_option_without_its_folder_is_refused(self):
        refused = FirstRunInterface("test_a_check_asks_the_architecture_and_writes_nothing")
        refused.setUp()
        self.addCleanup(refused.tearDown)
        asked = refused.sh("--project-path")
        self.assertEqual(asked.returncode, 1)
        self.assertIn("need a path", printed(asked, "stderr"))
        self.assertNotIn("git clone", printed(asked))

    def test_the_old_single_project_option_is_refused_with_the_one_to_use(self):
        refused = FirstRunInterface("test_a_check_asks_the_architecture_and_writes_nothing")
        refused.setUp()
        self.addCleanup(refused.tearDown)
        for argv in (("--project", "x"), ("--project=x",)):
            with self.subTest(argv=argv):
                asked = refused.sh(*argv)
                self.assertEqual(asked.returncode, 1)
                self.assertIn("--project-path", printed(asked, "stderr"))
                self.assertNotIn("git clone", printed(asked))

    def test_the_help_of_each_bootstrap_names_the_project_option(self):
        helper = FirstRunInterface("test_a_check_asks_the_architecture_and_writes_nothing")
        helper.setUp()
        self.addCleanup(helper.tearDown)
        self.assertIn("--project-path", printed(helper.sh("--help")))
        shell = shutil.which("powershell") or shutil.which("pwsh")
        if shell:
            asked = subprocess.run(
                [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPTS / "install.ps1"), "-Help"],
                capture_output=True,
            )
            self.assertIn("-ProjectPath", asked.stdout.decode("utf-8", "replace"))


class DeveloperIsMarked(unittest.TestCase):
    """`--developer` marks the recorded checkout in its own git configuration and changes nothing else."""

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch(), ignore_cleanup_errors=True)
        self.addCleanup(scratch.cleanup)
        self.checkout = Path(scratch.name) / "memar"
        (self.checkout / "docs").mkdir(parents=True)
        (self.checkout / "README.md").write_text("# Memar\n", encoding="utf-8")
        (self.checkout / SKILL_MARKER).parent.mkdir(parents=True)
        (self.checkout / SKILL_MARKER).write_text("skill\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(self.checkout)], check=True)

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.checkout), *arguments], capture_output=True, text=True
        ).stdout.strip()

    def test_the_recorded_checkout_is_marked_and_its_tree_is_unchanged(self) -> None:
        before = self.git("status", "--porcelain")
        with unittest.mock.patch.object(machine_layer, "recorded_root", return_value=self.checkout):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                machine_layer.mark_developer()
        self.assertTrue(update_checkout.is_marked_development(self.checkout))
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertIn("marked as a development checkout", out.getvalue())
        self.assertIn(f"config --unset {update_checkout.DEVELOPMENT_KEY}", out.getvalue())

    def test_a_folder_that_is_not_a_memar_repository_is_refused(self) -> None:
        (self.checkout / "README.md").unlink()
        with unittest.mock.patch.object(machine_layer, "recorded_root", return_value=None), \
                unittest.mock.patch.object(machine_layer, "checkout_root", return_value=self.checkout):
            with self.assertRaises(SystemExit) as refused:
                machine_layer.mark_developer()
        self.assertIn("nothing was marked", str(refused.exception))
        self.assertFalse(update_checkout.is_marked_development(self.checkout))


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

    def test_the_installer_answers_a_help_request_as_a_memar_verb(self):
        shown = printed(run_install("--help"))
        self.assertTrue(shown.startswith("usage: memar install "), shown[:80])

    def test_the_layers_declare_no_command_line_of_their_own(self):
        # The router lists a verb for each service that describes one, and a
        # layer is asked by the installer, not by a person: none describes a verb
        # and none is run.
        for layer in (machine_layer, project_layer, apps_layer):
            with self.subTest(layer=layer.__name__):
                self.assertFalse(hasattr(layer, "describe"))
                self.assertNotIn('if __name__ == "__main__"', Path(layer.__file__).read_text(encoding="utf-8"))

    def test_the_installer_still_takes_the_same_arguments_in_the_same_order(self):
        shown = printed(run_install("--help"))
        options = re.findall(r"^  (--\S+)( \S+)?  ", shown, re.MULTILINE)
        self.assertEqual(
            tuple((option, (argument or "").strip()) for option, argument in options),
            INSTALLER_OPTIONS,
        )

    def test_the_installer_help_is_the_text_meant_for_a_caller(self):
        # The help is `description()`, not the module docstring: the docstring is
        # addressed to whoever opens the file and is the reasoning behind the run.
        # Pinning the docstring here is what made the two the same text, which is
        # how the mechanism ended up printed to every person installing Memar.
        shown = printed(run_install("--help"))
        self.assertIn(memar_install.description().strip(), shown)
        self.assertNotIn(memar_install.__doc__.strip(), shown)

    def test_the_installer_help_carries_no_mechanism(self):
        shown = printed(run_install("--help"))
        for phrase in (
            "machine/fs_memar_repository.py",
            "bundles/memar/update/services/checkout.py",
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
        shown = printed(run_install("--help"))
        self.assertIn("restart", shown)
        self.assertIn("--check", shown)

class InstallingRegistersTheProject(unittest.TestCase):
    """Installing Memar into a project is declaring that it follows Memar, so the registry learns it then.

    The name is the project's folder name, which a person changes later with
    `memar project add --alias`. A project already registered is left as it is,
    not an error and not given a second name; a name another project holds is
    reported and nothing is renamed. The registry is the scratch Memar's.
    """

    def setUp(self) -> None:
        import machine.fs_memar as memar_fs
        import modules.process.project.services.registry as registry

        self.registry = registry
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name).resolve()
        self.memar = self.base / "memar"
        (self.memar / "temp").mkdir(parents=True)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.memar)
        patched.start()
        self.addCleanup(patched.stop)

    def project(self, name: str = "work-app", parent: Path | None = None) -> Path:
        folder = (parent or self.base) / name
        (folder / ".git").mkdir(parents=True)
        return folder

    def install(self, folder: Path, **options) -> tuple[str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            project_layer.into_project(folder, **options)
        return out.getvalue(), err.getvalue()

    def entry_of(self, folder: Path):
        mine = self.registry.path_key(folder)
        found = [entry for entry in self.registry.read_entries() if self.registry.path_key(entry.path) == mine]
        return found[0] if found else None

    def test_the_project_is_registered_under_its_folder_name(self) -> None:
        folder = self.project()
        out, _ = self.install(folder)
        entry = self.entry_of(folder)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.names, ("work-app",))
        self.assertIn("work-app", out)
        self.assertIn("--alias", out)

    def test_a_subfolder_registers_the_project_root_under_the_roots_name(self) -> None:
        folder = self.project()
        inside = folder / "src"
        inside.mkdir()
        self.install(inside)
        self.assertEqual(self.entry_of(folder).names, ("work-app",))
        self.assertIsNone(self.entry_of(inside))

    def test_memars_own_entry_is_there_as_a_project_add_would_leave_it(self) -> None:
        self.install(self.project())
        self.assertIsNotNone(self.entry_of(self.memar))

    def test_a_project_already_registered_is_not_an_error_and_gets_no_second_name(self) -> None:
        folder = self.project()
        self.registry.add_project("the-app", folder, ["app"])
        out, err = self.install(folder)
        self.assertEqual(self.entry_of(folder).names, ("the-app", "app"))
        self.assertIn("the-app", out)
        self.assertNotIn("error", err.lower())
        self.install(folder)
        self.assertEqual(self.entry_of(folder).names, ("the-app", "app"))

    def test_a_second_install_changes_nothing(self) -> None:
        folder = self.project()
        self.install(folder)
        before = self.registry.read_entries()
        self.install(folder)
        self.assertEqual(self.registry.read_entries(), before)

    def test_a_name_another_project_holds_is_reported_and_nothing_is_renamed(self) -> None:
        holder = self.project("holder", parent=self.base)
        self.registry.add_project("work-app", holder)
        other = self.project("work-app", parent=self.base / "elsewhere")
        out, err = self.install(other)
        self.assertIsNone(self.entry_of(other))
        self.assertEqual(self.entry_of(holder).names, ("work-app",))
        self.assertIn("work-app", err)
        self.assertIn(str(holder), err)
        self.assertIn("memar project add", err)
        self.assertTrue((other / "AGENTS.md").is_file(), "the install itself still ran")

    def test_a_dry_run_says_what_it_would_register_and_writes_no_registry(self) -> None:
        import machine.fs_memar as memar_fs

        folder = self.project()
        out, _ = self.install(folder, dry_run=True)
        self.assertIn("work-app", out)
        self.assertIn("dry-run", out)
        self.assertFalse(memar_fs.projects_log().exists())

    def test_no_project_named_touches_no_registry(self) -> None:
        import machine.fs_memar as memar_fs

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            project_layer.into_project(None)
        self.assertFalse(memar_fs.projects_log().exists())

    def test_the_installer_run_by_a_folder_registers_it_through_the_project_layer(self) -> None:
        folder = self.project()
        parser = argparse.ArgumentParser()
        command = memar_install.describe(parser.add_subparsers())
        with unittest.mock.patch.object(location, "recorded_root", return_value=SCRIPTS), \
                unittest.mock.patch.object(machine_layer, "report_installed"), \
                unittest.mock.patch.object(apps_layer, "into_apps"), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(command(parser.parse_args(["install", "--project-path", str(folder)])), 0)
        self.assertEqual(self.entry_of(folder).names, ("work-app",))


class BareRunInstallsEveryLayer(unittest.TestCase):
    """One bare run settles the machine, this project, and the agent apps.

    The order is the dependency rather than a preference: the app layer needs the
    location the machine layer records, so it is asked second and says so itself
    when there is no location. What it must never do is go past installing, so a
    layer that cannot apply reports and returns rather than failing the run.
    """

    def setUp(self) -> None:
        # Every layer stubbed, each recording what it was asked, so the order a
        # run asks them in is what is observed and nothing reaches the machine.
        self.asked: list[tuple[str, dict]] = []
        for module, name in (
            (machine_layer, "register"),
            (machine_layer, "report_installed"),
            (project_layer, "into_project"),
            (apps_layer, "into_apps"),
        ):
            patched = unittest.mock.patch.object(
                module, name, side_effect=lambda *args, _name=name, **kwargs: self.asked.append((_name, kwargs))
            )
            patched.start()
            self.addCleanup(patched.stop)

    def run_verb(self, *arguments: str, recorded: Path | None = None) -> tuple[int, str, str]:
        """`memar install ARGUMENTS` as the router runs it, with RECORDED as the recorded root."""
        parser = argparse.ArgumentParser()
        command = memar_install.describe(parser.add_subparsers())
        out, err = io.StringIO(), io.StringIO()
        with unittest.mock.patch.object(location, "recorded_root", return_value=recorded), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = command(parser.parse_args(["install", *arguments]))
        return code, out.getvalue(), err.getvalue()

    def test_both_layers_are_asked_and_in_that_order(self):
        memar_install.into_project_and_apps()
        self.assertEqual([name for name, _ in self.asked], ["into_project", "into_apps"])

    def test_a_dry_run_is_forwarded_to_the_layers(self):
        # The machine layer writes a value, so it is never a dry run; what a
        # dry run previews is what the project and app layers would write.
        self.run_verb("--dry-run", recorded=SCRIPTS)
        self.assertEqual(
            self.asked,
            [("report_installed", {}), ("into_project", {"dry_run": True}), ("into_apps", {"dry_run": True})],
        )

    def test_a_layer_that_does_not_apply_does_not_stop_the_run(self):
        # The app layer's dependency is the machine layer, not the project
        # layer, so a project that refused must not cost the skill its copies.
        refusal = "error: /home is not a project directory"
        project_layer.into_project.side_effect = SystemExit(refusal)
        code, out, err = self.run_verb(recorded=SCRIPTS)
        self.assertEqual(code, 0)
        self.assertEqual(self.asked[-1], ("into_apps", {"dry_run": False}))
        self.assertIn(refusal, err)
        self.assertLess(out.index("==> Into this project"), out.index("==> Into the agent apps"))

    def test_a_named_project_is_resolved_and_passed_to_the_project_layer_only(self):
        named = SCRIPTS
        passed: list = []
        project_layer.into_project.side_effect = lambda project=None, **kwargs: passed.append(project)
        self.run_verb("--project-path", str(named), recorded=SCRIPTS)
        self.assertEqual(passed, [named.resolve()])

    def test_a_named_project_is_looked_up_by_name_and_a_path_in_its_place_is_refused(self):
        passed: list = []
        project_layer.into_project.side_effect = lambda project=None, **kwargs: passed.append(project)
        with unittest.mock.patch("modules.process.project.services.find.resolve_project", return_value=SCRIPTS) as found:
            self.run_verb("--project", "khayyam", recorded=SCRIPTS)
        found.assert_called_once_with("khayyam")
        self.assertEqual(passed, [SCRIPTS])
        with self.assertRaises(SystemExit) as refused:
            self.run_verb("--project", str(SCRIPTS), recorded=SCRIPTS)
        self.assertIn("--project-path", str(refused.exception.code))

    def test_no_project_named_passes_none_not_the_working_folder(self):
        passed: list = []
        project_layer.into_project.side_effect = lambda project=None, **kwargs: passed.append(project)
        self.run_verb(recorded=SCRIPTS)
        self.assertEqual(passed, [None])

    def test_a_machine_only_run_skips_the_project_and_the_apps(self):
        self.run_verb("--machine-only", recorded=SCRIPTS)
        self.assertEqual([name for name, _ in self.asked], ["report_installed"])

    def test_nothing_recorded_registers_this_checkout_and_then_asks_the_layers(self):
        self.run_verb()
        self.assertEqual([name for name, _ in self.asked], ["register", "into_project", "into_apps"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
