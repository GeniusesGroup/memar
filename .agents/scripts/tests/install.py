#!/usr/bin/env python3
"""Tests for the installer, the modules it is split into, and the bootstrap.

    python .agents/scripts/tests/install.py

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
  SiblingSurface    `import install` still offers what install-agents.py and
                      install-apps.py import; a file in this folder may assume
                      its neighbour is on disk beside it.
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
                      and --check still asks its question and writes nothing.
  HelpUnchanged     The refactoring changed no consumer's interface.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import hashlib
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
SCRIPTS = TESTS.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import install
import sys_env_location
import sys_fs_target

VARIABLE = sys_env_location.VARIABLE
# install-agents.py and install-apps.py import exactly these four, by those names.
SIBLING_SURFACE = ("use_utf8_stdio", "is_memar_repository", "resolve_root", "NEVER_COPIED")
# A script run that has a sibling on disk beside it: the sha256 of its exact
# --help bytes, at a fixed 80-column width, under a fixed encoding. One of those
# bytes is the program's own name — argparse takes it from argv — so a rename
# moves this pin with the file rather than leaving it to fail.
UNCHANGED_HELP = {
    "install-apps.py": "d40610366c74da88f88d405b9c259669deb2b0c048380570eea46a7fd3b40c1a",
    "install-agents.py": "6f1024de7ccb48ac96975b3aa0452a2a61d02b19db74d18f9e536ec86fa32200",
    "memar-documentation.py": "88b1bb7957c811d3489a6f796c24d7fec4eac68038aef48b3efdd3ffc30f006e",
}
# install.py's own options, in the order argparse prints them, with the argument
# each one takes. Obtaining the checkout is the bootstrap's, so what is left here
# is the recording of one and the check that asks about a folder.
INSTALLER_OPTIONS = (
    ("--register", "PATH"),
    ("--check", "PATH"),
)
IMPORTED_MODULE = re.compile(r"^from ([a-z_][a-z_0-9]*) import ", re.MULTILINE)
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
ARCHITECTURE_ENTRY = ".agents/scripts/install.py"
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
SH_RUN = re.compile(r'^exec "\$PYTHON" "\$checkout/\$ARCHITECTURE_ENTRY" "\$@"$', re.MULTILINE)
PS_RUN = re.compile(
    r"^& \$python \(Join-Path \$checkout \$ArchitectureEntry\) @forwarded$",
    re.MULTILINE | re.IGNORECASE,
)
# The path rule the bootstrap asks for rather than keeping a second copy of: the
# installer expands `~` and `$NAME` in sys_fs_target.full_path, so the folder this
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


class RecordOverSession(unittest.TestCase):
    """The record is the value; the process environment is a cache of it."""

    def setUp(self) -> None:
        self.saved = os.environ.get(VARIABLE)
        self.saved_notice = sys_env_location.NOTICE_REPORTED
        self.saved_persisted = sys_env_location.persisted_value
        sys_env_location.NOTICE_REPORTED = False

    def tearDown(self) -> None:
        if self.saved is None:
            os.environ.pop(VARIABLE, None)
        else:
            os.environ[VARIABLE] = self.saved
        sys_env_location.NOTICE_REPORTED = self.saved_notice
        sys_env_location.persisted_value = self.saved_persisted

    def ask(self, record: str, session: str) -> str:
        """What a program sees when the record holds RECORD and its own copy holds SESSION."""
        sys_env_location.persisted_value = lambda: record
        if session:
            os.environ[VARIABLE] = session
        else:
            os.environ.pop(VARIABLE, None)
        with contextlib.redirect_stdout(io.StringIO()):
            return sys_env_location.recorded_value()

    def test_the_record_answers_when_the_session_reads_nothing(self):
        # The accident: the session that opened before the value was written.
        self.assertEqual(self.ask(r"C:\Users\you\Memar", ""), r"C:\Users\you\Memar")

    def test_the_record_answers_when_the_session_holds_another_value(self):
        # A cache is a copy of the record, so two different values is a stale
        # copy, not a decision. The record is the value.
        self.assertEqual(self.ask(r"C:\Users\you\Memar", r"D:\elsewhere"), r"C:\Users\you\Memar")

    def test_the_session_answers_when_the_record_is_silent(self):
        # Setting it for one session is a record for that session, and the
        # README makes it equivalent to writing it.
        self.assertEqual(self.ask("", r"D:\elsewhere"), r"D:\elsewhere")

    def test_a_stale_session_is_reported_rather_than_ignored(self):
        sys_env_location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ.pop(VARIABLE, None)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            sys_env_location.recorded_value()
        text = printed.getvalue()
        self.assertIn("disagrees with the record", text)
        self.assertIn("the record is used", text)
        self.assertIn(r"C:\Users\you\Memar", text)
        self.assertIn("unset", text)

    def test_a_stale_session_is_reported_once_not_once_per_read(self):
        sys_env_location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ.pop(VARIABLE, None)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            for _ in range(3):
                sys_env_location.recorded_value()
        self.assertEqual(printed.getvalue().count("disagrees with the record"), 1)

    def test_a_session_that_agrees_with_the_record_says_nothing(self):
        # The common case, every ordinary run: no line is added to the output.
        sys_env_location.persisted_value = lambda: r"C:\Users\you\Memar"
        os.environ[VARIABLE] = r"C:\Users\you\Memar"
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            sys_env_location.recorded_value()
        self.assertEqual(printed.getvalue(), "")

    def test_a_session_only_value_is_not_reported_as_stale(self):
        # A value the person set for this run is newer than the record, not
        # older, so the output does not gain a line on every such run.
        sys_env_location.persisted_value = lambda: ""
        os.environ[VARIABLE] = r"D:\elsewhere"
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            sys_env_location.recorded_value()
        self.assertEqual(printed.getvalue(), "")


class ProfileRoundTrip(unittest.TestCase):
    """What writes the record on POSIX is what reads it back."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.profile = Path(self.scratch.name) / ".bashrc"
        # Patched for the whole test, write included: a write that reached the
        # real profile would edit a file outside this repository.
        saved = sys_env_location.shell_profile
        sys_env_location.shell_profile = lambda: self.profile
        self.addCleanup(setattr, sys_env_location, "shell_profile", saved)

    def ask(self) -> str:
        return sys_env_location.profile_value()

    def test_what_written_is_what_read(self):
        sys_env_location.write_profile_variable("/home/you/Memar")
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_rewriting_replaces_the_value_rather_than_appending_a_second(self):
        sys_env_location.write_profile_variable("/home/you/Memar")
        sys_env_location.write_profile_variable("/home/you/Other")
        self.assertEqual(self.ask(), "/home/you/Other")
        self.assertEqual(
            self.profile.read_text(encoding="utf-8").count(f"export {VARIABLE}="), 1
        )

    def test_a_value_written_by_hand_is_read_too(self):
        # The README makes setting the variable by hand equivalent.
        self.profile.write_text(
            f'# a line\nexport {VARIABLE}="/home/you/Memar"\n', encoding="utf-8"
        )
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_a_commented_assignment_is_not_a_value(self):
        self.profile.write_text(
            f'# export {VARIABLE}="/home/you/Memar"\n', encoding="utf-8"
        )
        self.assertEqual(self.ask(), "")

    def test_the_last_assignment_is_the_one_a_new_shell_gets(self):
        self.profile.write_text(
            f'export {VARIABLE}="/home/you/First"\n'
            f'export {VARIABLE}="/home/you/Memar"\n',
            encoding="utf-8",
        )
        self.assertEqual(self.ask(), "/home/you/Memar")

    def test_a_profile_that_is_not_there_reads_as_nothing(self):
        self.profile.unlink(missing_ok=True)
        self.assertEqual(self.ask(), "")


class RecordReadWrite(unittest.TestCase):
    """The Windows pair names one key, not two, and the read follows the platform."""

    def test_read_and_write_name_the_same_key(self):
        # The registry read cannot be executed here without writing the user's
        # real HKCU\\Environment, so what is pinned is the one thing that made
        # the two disagree in the first place: the key they name.
        self.assertEqual(sys_env_location.VARIABLE, "MEMAR_ROOT")
        self.assertEqual(sys_env_location.WINDOWS_ENVIRONMENT_KEY, "Environment")
        for function in (sys_env_location.user_environment_value, sys_env_location.write_user_variable):
            names = function.__code__.co_names
            self.assertIn("WINDOWS_ENVIRONMENT_KEY", names, function.__name__)
            self.assertIn("VARIABLE", names, function.__name__)

    def test_the_windows_read_finds_what_the_registry_actually_holds(self):
        # The only way to read the record is to ask for it, and asking wrongly
        # — a predefined key and a backslash in a value name, which is not the
        # same thing — reports no value at all and is exactly the failure this
        # fix exists to remove. It is read here, never written.
        if os.name != "nt":
            self.skipTest("the registry-backed user environment is a Windows record")
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_QUERY_VALUE
            ) as key:
                expected, _ = winreg.QueryValueEx(key, "MEMAR_ROOT")
        except OSError:
            self.skipTest("this machine records no MEMAR_ROOT")
        self.assertEqual(sys_env_location.user_environment_value(), sys_env_location.expand_recorded(str(expected)))

    def test_the_windows_read_expands_what_the_windows_write_can_hold(self):
        # A value written as REG_EXPAND_SZ is expanded by Windows when it builds
        # a new process's environment, so reading it back expands it too: the
        # record and the copy agree by construction.
        self.assertEqual(sys_env_location.expand_recorded(r"%USERPROFILE%\Memar"), str(Path.home() / "Memar"))

    def test_the_read_asks_the_platform_the_write_uses(self):
        # Two reads would be two answers, and a wrong one is the defect: the read
        # that never asked the registry is what concluded Memar was not
        # installed on a machine where it was.
        answered = []

        def registry() -> str:
            answered.append("registry")
            return r"C:\Users\you\Memar"

        def profile() -> str:
            answered.append("profile")
            return "/home/you/Memar"

        saved_registry = sys_env_location.user_environment_value
        saved_profile = sys_env_location.profile_value
        sys_env_location.user_environment_value = registry
        sys_env_location.profile_value = profile
        self.addCleanup(setattr, sys_env_location, "user_environment_value", saved_registry)
        self.addCleanup(setattr, sys_env_location, "profile_value", saved_profile)
        with unittest.mock.patch.object(os, "name", "nt"):
            self.assertEqual(sys_env_location.persisted_value(), r"C:\Users\you\Memar")
        with unittest.mock.patch.object(os, "name", "posix"):
            self.assertEqual(sys_env_location.persisted_value(), "/home/you/Memar")
        self.assertEqual(answered, ["registry", "profile"])


class TemporaryRefusal(unittest.TestCase):
    """Every refusal names the directory the check actually used."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=TESTS)
        self.addCleanup(self.scratch.cleanup)
        self.saved_temp = os.environ.get("TEMP")
        os.environ["TEMP"] = self.scratch.name

    def tearDown(self) -> None:
        if self.saved_temp is None:
            os.environ.pop("TEMP", None)
        else:
            os.environ["TEMP"] = self.saved_temp

    def refused(self, path: Path, consequence: str) -> str:
        with self.assertRaises(SystemExit) as raised:
            sys_fs_target.refuse_temporary(path, consequence)
        return str(raised.exception.code)

    def test_the_refusal_names_the_directory_the_check_used(self):
        below = Path(self.scratch.name) / "Memar"
        message = self.refused(below, "because it does not survive.")
        self.assertIn(str(Path(self.scratch.name).resolve()), message)
        self.assertIn(str(below), message)

    def test_a_folder_outside_it_is_not_refused(self):
        outside = SCRIPTS / "not-a-temp-folder"
        self.assertIsNone(sys_fs_target.refuse_temporary(outside, "unused"))

    def test_the_directory_is_asked_once_and_used_for_both(self):
        # A check that reads the directory and a message that reads it again can
        # print a directory the decision was not made against.
        asked = []
        saved = sys_fs_target.temporary_directory

        def counted() -> Path:
            asked.append(1)
            return saved()

        sys_fs_target.temporary_directory = counted
        self.addCleanup(setattr, sys_fs_target, "temporary_directory", saved)
        with self.assertRaises(SystemExit):
            sys_fs_target.refuse_temporary(Path(self.scratch.name) / "Memar", "because.")
        self.assertEqual(len(asked), 1)

    def test_every_mode_refuses_through_the_same_decision(self):
        # The refusal a record prints and the refusal a check prints come from
        # one check, so neither can drift from the other. Both are called with
        # the refusal itself stubbed out, which is the only way to ask what each
        # one would have decided.
        decided = []

        def recorder(path: Path, consequence: str) -> None:
            decided.append((str(path), consequence))
            raise RuntimeError("refused")

        saved = install.refuse_temporary
        install.refuse_temporary = recorder
        self.addCleanup(setattr, install, "refuse_temporary", saved)
        with self.assertRaises(RuntimeError):
            install.register(str(Path(self.scratch.name) / "Memar"))
        with self.assertRaises(RuntimeError):
            install.check(str(Path(self.scratch.name) / "Memar"))
        self.assertEqual(len(decided), 2)
        self.assertEqual({path for path, _ in decided}, {str(Path(self.scratch.name) / "Memar")})
        for _, consequence in decided:
            self.assertTrue(consequence)

    def test_the_register_refusal_names_the_directory_it_kept_quiet_about(self):
        below = Path(self.scratch.name) / "Memar"
        message = self.refused(below, "unused")
        self.assertIn(str(Path(self.scratch.name).resolve()), message)


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
        asked = run_script("install.py", "--check", str(below), temp=self.scratch.name)
        refused = run_script("install.py", "--register", str(below), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 1)
        self.assertEqual(refused.returncode, 1)
        for outcome in (printed(asked, "stderr"), printed(refused, "stderr")):
            self.assertIn(str(below), outcome)
            self.assertIn(str(Path(self.scratch.name).resolve()), outcome)
            self.assertIn("is under the temporary directory", outcome)

    def test_asking_about_a_folder_that_would_be_kept_answers_and_creates_nothing(self):
        asked = run_script("install.py", "--check", str(self.kept), temp=self.scratch.name)
        self.assertEqual(asked.returncode, 0)
        self.assertIn(self.scratch.name, printed(asked))
        self.assertIn("not refused", printed(asked))
        self.assertFalse(self.kept.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_asking_writes_nothing_even_when_the_answer_is_refusal(self):
        below = Path(self.scratch.name) / "Memar"
        run_script("install.py", "--check", str(below), temp=self.scratch.name)
        self.assertFalse(below.exists())
        self.assertEqual(self.scratch_entries(), [])

    def test_checking_needs_no_temporary_directory_variable_at_all(self):
        environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8")
        environment.pop("TEMP", None)
        environment.pop("TMPDIR", None)
        asked = subprocess.run(
            [sys.executable, str(SCRIPTS / "install.py"), "--check", str(self.kept)],
            capture_output=True,
            env=environment,
        )
        self.assertEqual(asked.returncode, 0)
        self.assertFalse(self.kept.exists())


class SiblingSurface(unittest.TestCase):
    """A file in this folder may assume its neighbour is on disk beside it."""

    def test_the_module_the_siblings_import_offers_what_they_import(self):
        for name in SIBLING_SURFACE:
            self.assertTrue(callable(getattr(install, name)), f"install.{name}")

    def test_every_module_the_entry_point_imports_is_a_file_beside_it(self):
        # The architecture is run from a checkout, so an import of a sibling is
        # answered from the disk beside the entry point. A name with no file
        # beside it is the standard library, and the question is about the rest.
        for module in IMPORTED_MODULE.findall((SCRIPTS / "install.py").read_text(encoding="utf-8")):
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
                answered.stdout.decode("utf-8").strip(), str(sys_fs_target.full_path(value)), value
            )

    def test_the_bootstrap_and_the_installer_default_to_the_same_folder(self):
        self.assertEqual(sys_fs_target.default_target(), Path.home() / sys_fs_target.INSTALL_DIRNAME)
        self.assertEqual(sys_fs_target.INSTALL_DIRNAME, "Memar")
        for bootstrap, pattern in (
            ("install.sh", r'^INSTALL_DIRNAME="([^"]*)"$'),
            ("install.ps1", r'^\$InstallDirname = "([^"]*)"$'),
        ):
            self.assertEqual(
                re.findall(pattern, self.source(bootstrap), re.MULTILINE),
                [sys_fs_target.INSTALL_DIRNAME],
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

    def test_help_prints_the_three_steps_and_the_documented_ways_of_naming_a_folder(self):
        shown = printed(self.sh("--help"))
        self.assertIn("Prerequisites", shown)
        self.assertIn("The architecture", shown)
        self.assertIn("The installer", shown)
        for option in ("--path", "--register", "--check"):
            self.assertIn(option, shown)

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
        self.assertFalse(kept.exists())


class HelpUnchanged(unittest.TestCase):
    """The refactoring changed no consumer's interface."""

    def test_help_is_byte_identical_for_the_scripts_this_change_does_not_touch(self):
        for name, expected in UNCHANGED_HELP.items():
            printed = run_script(name, "--help")
            self.assertEqual(printed.returncode, 0, name)
            self.assertEqual(hashlib.sha256(printed.stdout).hexdigest(), expected, name)

    def test_the_installer_still_takes_the_same_arguments_in_the_same_order(self):
        shown = printed(run_script("install.py", "--help"))
        options = re.findall(r"^  (--\S+)( \S+)?  ", shown, re.MULTILINE)
        self.assertEqual(
            tuple((option, (argument or "").strip()) for option, argument in options),
            INSTALLER_OPTIONS,
        )

    def test_the_installer_documents_what_its_help_prints(self):
        # --help prints the module docstring, so an option nobody wrote down
        # would be an option with no interface.
        shown = printed(run_script("install.py", "--help"))
        self.assertIn(install.__doc__.strip(), shown)
        self.assertIn("--check", shown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
