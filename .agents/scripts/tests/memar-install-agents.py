#!/usr/bin/env python3
"""Tests for what memar-install-agents.py writes into a consuming project.

    python .agents/scripts/tests/memar-install-agents.py

The README it writes is pinned whole, because it is fixed text: a wording
change is an edit of two files, never a drift one of them absorbs alone. Inside
that text three things are pinned by name, each load-bearing for the agent that
reads it —

  the skill command, which is the only way a consuming project reaches a skill
      no copy of which sits beside this README;
  one fenced block per platform, holding one command and nothing after it,
      because a block is what a reader copies: both platforms in one block
      paste the wrong one into the other platform's shell, and a comment
      pasted with a command is not a comment on every shell that reads it;
  the bootstrap offered only where the command is missing. What this
      program does after that command finishes is the bootstrap's own output,
      not a sentence written into the project: that sentence is allowed to
      change, and a copy of it in every project would keep the old one.

The location is read through the module that owns it, so a session opened
before the value was written does not send this project to the bootstrap a
second time.

The dry run happens in a scratch folder of its own — given a `.git` so that it
is a project root wherever it sits, and placed by `MEMAR_TEST_SCRATCH` when
that variable is set (a folder that already exists) — and only what it printed
is read: a scratch inside this repository would be installed into this
repository, which deliberately keeps its own hand-written `.agents/memar/README.md`
rather than the text written for a project that has to fetch Memar first. The
update test is the one exception: it installs for real inside that scratch and
reads the README back off disk.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
sys.dont_write_bytecode = True

DRY_RUN_WRITE = re.compile(r"^dry-run: write (.+)$")
CONSUMER_README = ".agents/memar/README.md"
AGENTS_FILE = "AGENTS.md"
EXPECTED_README = """# Memar
This project is developed within Memar's framework.

Load the Memar skill at the start of every session: run `memar content path .agents/skills/memar/SKILL.md`, then load and follow the file it prints.

If `memar` is not on PATH, Memar is not available to this program yet. Run the bootstrap for your platform:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1)))"
```

macOS or Linux:

```sh
sh -c 'c=$(curl -fsSL https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh); test -n "$c" && exec sh -c "$c" install.sh'
```
"""


class ReachedByTheCommand(unittest.TestCase):
    """What a consuming project is left holding, as the installer's own run says."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=os.environ.get("MEMAR_TEST_SCRATCH"))
        self.addCleanup(self.scratch.cleanup)
        (Path(self.scratch.name) / ".git").mkdir()
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "memar-install-agents.py"), "--dry-run"],
            cwd=self.scratch.name,
            capture_output=True,
            env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("utf-8", "replace"))
        self.writes = self.parse(completed.stdout.decode("utf-8").replace("\r\n", "\n"))

    def parse(self, output: str) -> list[tuple[str, str]]:
        """Each announced write and the text of it, in the order printed."""
        writes: list[tuple[str, list[str]]] = []
        for line in output.splitlines():
            match = DRY_RUN_WRITE.match(line)
            if match:
                writes.append((match.group(1).replace("\\", "/"), []))
            elif writes:
                writes[-1][1].append(line)
        return [(path, "\n".join(lines).strip("\n")) for path, lines in writes]

    def written(self, tail: str) -> str:
        """What was written to the file whose path ends with TAIL."""
        for path, text in self.writes:
            if path.endswith(tail):
                return text
        self.fail(f"nothing was written to {tail}; these were: {[path for path, _ in self.writes]}")

    def test_the_readme_is_pinned_whole(self):
        self.assertEqual(self.written(CONSUMER_README), EXPECTED_README.rstrip("\n"))

    def test_the_pointer_in_the_agent_file_names_no_path_into_the_scripts_folder(self):
        section = self.written(AGENTS_FILE)
        self.assertIn("## Memar", section)
        self.assertIn(CONSUMER_README, section)
        self.assertNotIn(".py", section)

    def test_the_skill_location_is_loaded_every_session(self):
        body = self.written(CONSUMER_README)
        self.assertIn("every session", body)
        self.assertIn("`memar content path .agents/skills/memar/SKILL.md`", body)
        self.assertIn("then load and follow the file it prints", body)

    def test_each_platform_is_its_own_block_of_exactly_one_command(self):
        # A fenced block is what a reader copies, so a block holding both
        # platforms pastes the wrong one into the other platform's shell, and a
        # comment carried past the end of a command is not a comment on every
        # shell that is asked to read it. Each block is also the one its own
        # label announces: two correct commands under swapped labels are still
        # the wrong command for the reader who believed the label.
        body = self.written(CONSUMER_README)
        blocks = re.findall(r"```[a-z]*\n(.*?)```", body, re.S)
        self.assertEqual(len(blocks), 2, body)
        self.assertEqual(body.count("```"), 4, body)
        for block in blocks:
            lines = [line for line in block.splitlines() if line.strip()]
            self.assertEqual(len(lines), 1, block)
            self.assertNotIn("#", block)
        windows = body.partition("Windows:")[2].partition("macOS or Linux:")[0]
        self.assertIn("install.ps1", windows)
        self.assertNotIn("install.sh", windows)
        posix = body.partition("macOS or Linux:")[2]
        self.assertIn("install.sh", posix)
        self.assertNotIn("install.ps1", posix)

    def test_the_location_is_read_through_the_module_that_owns_it(self):
        # Not through `os.environ`, which is the copy a session opened before
        # the value was written may not hold: that is how a project gets told
        # Memar is not on this machine when it is.
        source = (SCRIPTS / "memar-install-agents.py").read_text(encoding="utf-8")
        self.assertNotIn("os.environ.get", source)
        self.assertIn("recorded_value()", source)

    def test_a_machine_without_the_command_gets_the_bootstrap(self):
        body = self.written(CONSUMER_README)
        self.assertIn("If `memar` is not on PATH, Memar is not available to this program yet.", body)
        # A failed fetch must not look like success: `sh -c "$(curl …)"` runs
        # an empty script and exits 0 when curl fails. The command stops unless
        # the fetch produced a script.
        self.assertIn('test -n "$c"', body)
        # What to do after the bootstrap finishes is printed by the bootstrap.
        # A sentence here would be copied into every project and would stay
        # there after the sentence changed.
        self.assertNotIn("restart", body)
        self.assertNotIn("MEMAR_ROOT", body)
        self.assertNotIn("--help", body)

    def test_update_rewrites_an_already_installed_readme(self):
        command = [sys.executable, str(SCRIPTS / "memar-install-agents.py")]
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        installed = subprocess.run(command, cwd=self.scratch.name, capture_output=True, env=env)
        self.assertEqual(installed.returncode, 0, installed.stderr.decode("utf-8", "replace"))
        readme = Path(self.scratch.name) / CONSUMER_README
        readme.write_text("# Stale\n", encoding="utf-8", newline="\n")
        updated = subprocess.run(command + ["update"], cwd=self.scratch.name, capture_output=True, env=env)
        self.assertEqual(updated.returncode, 0, updated.stderr.decode("utf-8", "replace"))
        expected = self.written(CONSUMER_README)
        actual = (Path(self.scratch.name) / CONSUMER_README).read_text(encoding="utf-8")
        self.assertEqual(actual, EXPECTED_README)
        self.assertEqual(actual.rstrip("\n"), expected)
        self.assertIn("README.md", updated.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
