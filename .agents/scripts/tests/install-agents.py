#!/usr/bin/env python3
"""Tests for what install-agents.py writes into a consuming project.

    python .agents/scripts/tests/install-agents.py

What is pinned, and what each pin is for:

  ReachedByTheCommand  A project is given the entry point this repository uses.
                      A path into a scripts folder is another shape of the same
                      framework, so what a project is left holding names the
                      command first, and names no path ahead of it.
  ReadmeNamesBothForms  The command is not on every machine's PATH, so the text
                      says both — the command, and the script under the recorded
                      location — and says which machine has which.
  KeptReachable         Reaching Memar by a command does not retire the way a
                      machine with neither the command nor the variable gets it:
                      the variable, the bootstrap, and the restart it asks for
                      all stay.

The run is a dry run in a scratch folder outside this checkout, and only what it
printed is read: a scratch inside this repository would be installed into this
repository, which deliberately keeps its own hand-written `.agents/memar/README.md`
rather than the text written for a project that has to fetch Memar first.

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
# The one place a machine with no checkout of its own is told to get one from.
BOOTSTRAP_SOURCE = "raw.githubusercontent.com/GeniusesGroup/memar"


class ReachedByTheCommand(unittest.TestCase):
    """What a consuming project is left holding, as the installer's own run says."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "install-agents.py"), "--dry-run"],
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

    def test_the_project_is_given_the_command_first(self):
        # The first thing said, before the variable and before any path.
        heading, _, rest = self.written(CONSUMER_README).partition("\n")
        self.assertEqual(heading, "# Memar")
        lead = rest.partition("\n\n")[0]
        self.assertTrue(lead.startswith("`memar`"), lead)
        self.assertNotIn(".py", lead)
        self.assertNotIn("MEMAR_ROOT", lead)

    def test_the_pointer_in_the_agent_file_names_no_path_into_the_scripts_folder(self):
        section = self.written(AGENTS_FILE)
        self.assertIn("## Memar", section)
        self.assertIn(CONSUMER_README, section)
        self.assertNotIn(".py", section)

    def test_the_text_states_the_command_and_the_path_beside_it(self):
        body = self.written(CONSUMER_README)
        self.assertLess(body.index("`memar`"), body.index("$MEMAR_ROOT"))
        self.assertIn("$MEMAR_ROOT/.agents/scripts/memar-documentation.py", body)

    def test_a_machine_with_neither_the_command_nor_the_variable_is_still_answered(self):
        body = self.written(CONSUMER_README)
        self.assertIn("`MEMAR_ROOT`", body)
        self.assertIn(BOOTSTRAP_SOURCE, body)
        self.assertIn("restart", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
