#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what the project layer, `services/install_project.py`, writes into a consuming project.

    python .agents/scripts/services/tests/install_project.py

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

Beside the README sits the project's preferences file, and it is the opposite
case: written once, when absent, with an empty `sessions` key and a paragraph
saying whose it is, and never again — in the Memar repository too, whose README
is skipped. The README points at it, since the README is what gets rewritten.
Those runs are real, inside the scratch project, because a second run over a
file the project changed is the whole of what is pinned.

The layer is asked in this process, as `memar install` asks it, from inside a
scratch folder of its own — given a `.git` so that it is a project root wherever
it sits, and made under the folder `machine/fs_test_scratch.py` names. The
dry run writes nothing, and only what it printed is read: a scratch inside this repository would be installed into this
repository, which deliberately keeps its own hand-written `.agents/memar/README.md`
rather than the text written for a project that has to fetch Memar first.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import re
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
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import services.install_project as project
import services.project_preferences as project_preferences

DRY_RUN_WRITE = re.compile(r"^dry-run: write (.+)$")
CONSUMER_README = ".agents/memar/README.md"
PREFERENCES = Path(".agents/memar/preferences.md")
AGENTS_FILE = "AGENTS.md"
EXPECTED_README = """# Memar
This project is developed within Memar's framework.

Load the Memar skill at the start of every session: run `memar content path .agents/skills/memar/SKILL.md`, then load and follow the file it prints.

This project's preferences for Memar go in [`preferences.md`](preferences.md) beside this file, not here: this README is rewritten on every install, and that file never is.

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
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        (Path(self.scratch.name) / ".git").mkdir()
        self.writes = self.parse(self.into_project(dry_run=True))

    def into_project(self, **options: bool) -> str:
        """What the layer printed, asked from inside the scratch project."""
        out = io.StringIO()
        with contextlib.chdir(self.scratch.name), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(io.StringIO()):
            project.into_project(**options)
        return out.getvalue()

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
        source = Path(project.__file__).read_text(encoding="utf-8")
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


class SectionUpserted(unittest.TestCase):
    """The Memar section in AGENTS.md is replaced in place; the project's own sections keep their spacing."""

    def test_a_blank_line_still_parts_the_section_from_the_projects_next_one(self):
        own = "## Source\nRead the practice first.\n"
        before = f"{project.AGENTS_H1}\n\n## Memar\nAn older pointer.\n\n{own}"
        after = project.upsert_memar_section(before)
        self.assertEqual(after, f"{project.AGENTS_H1}\n\n{project.memar_section_markdown()}\n{own}")
        self.assertEqual(project.upsert_memar_section(after), after)


class PreferencesKept(unittest.TestCase):
    """The project's preferences file: made when absent, never written again."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.project = Path(self.scratch.name)
        (self.project / ".git").mkdir()
        self.preferences = self.project / PREFERENCES

    def into_project(self, **options: bool) -> str:
        out = io.StringIO()
        with contextlib.chdir(self.project), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(io.StringIO()):
            project.into_project(**options)
        return out.getvalue()

    def test_its_first_text_is_an_empty_sessions_key_and_a_paragraph_saying_whose_it_is(self):
        self.into_project()
        text = self.preferences.read_text(encoding="utf-8")
        self.assertEqual(text, project_preferences.PREFERENCES_TEXT)
        self.assertTrue(text.startswith("---\nsessions:\n---\n# Memar preferences\n"))
        for phrase in ("never rewrites it", "relative to the project's top folder, or an absolute one",
                       "neither that top folder itself nor a drive or filesystem root", "temp/sessions/",
                       "never touches a session folder made in the `sessions` folder",
                       "write any preference agents should follow"):
            self.assertIn(phrase, text)
        self.assertEqual(project_preferences.read_preferences(self.project), {})

    def test_a_second_install_leaves_the_projects_file_as_it_is(self):
        self.into_project()
        own = "---\nsessions: work/sessions\n---\n# Memar preferences\nOurs.\n"
        self.preferences.write_text(own, encoding="utf-8", newline="\n")
        printed = self.into_project()
        self.assertEqual(self.preferences.read_text(encoding="utf-8"), own)
        self.assertNotIn(str(self.preferences), printed)
        self.assertEqual(project_preferences.sessions_location(self.project), self.project / "work" / "sessions")

    def test_the_memar_repository_gets_one_too_though_its_readme_is_skipped(self):
        with unittest.mock.patch.object(project, "is_memar_repository", return_value=True):
            self.into_project()
        self.assertTrue(self.preferences.is_file())
        self.assertFalse((self.project / CONSUMER_README).exists())

    def test_the_readme_links_the_preferences_file_beside_it(self):
        self.assertIn(f"]({PREFERENCES.name})", project.README_BODY)
        self.assertEqual((self.project / PREFERENCES).parent, (self.project / CONSUMER_README).parent)


if __name__ == "__main__":
    unittest.main(verbosity=2)
