#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the one digest of decisions sessions hand back, in `services/session_digest.py`.

    python .agents/scripts/services/tests/session_digest.py

The subject is the digest — every `Decisions needed` entry across the
sessions' reports gathered into one text the owner reads — named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The design it holds is the parent plan's, session 20261012T134849Z-25068-0,
"Design": `memar session digest` gathers every `Decisions needed` entry across
reports into one digest.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  OneDigest          Every session whose report has entries under `Decisions
                     needed` is in the one digest, with its id, title, Stop,
                     and report path, and its entries as written; a session
                     with none is left out; the digest says how many sessions
                     and entries it holds; with none anywhere it says so;
                     `--conversation` narrows it to one conversation. Each
                     session shows its priority, and one whose report is not
                     a hand-back — no Stop, more than ten lines, or a Stop its
                     plan's status disagrees with — is in it marked as a failed
                     hand-back, with entries or without. A done session is
                     left out, its task over, and so is a queued one, which
                     has handed nothing back yet.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.session_digest as session_digest
import services.session_plan as session_plan
import services.session_report as session_report


class OneDigest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)

    def session(
        self, sid: str, title: str, stop: str, decisions: list[str], conversation: str = "", status: str = ""
    ) -> Path:
        """A session whose report has STOP and DECISIONS; its plan's STATUS agrees with STOP unless given."""
        status = status or session_report.STOP_STATUS.get(stop, "open")
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        linked = f"parent: {conversation}\nconversation: {conversation}\n" if conversation else ""
        (folder / session_plan.PLAN_NAME).write_text(
            f"---\ntitle: {title}\nopened: 2026-10-12T00:00:00Z\nproject: P\n{linked}---\n# {title}\nStatus: {status}\n\n## Request\nx\n",
            encoding="utf-8",
        )
        heading = "\n## Decisions needed\n" + "\n".join(decisions) + "\n" if decisions else ""
        (folder / session_report.REPORT_NAME).write_text(
            f"# Report\nStop: {stop}\n{heading}\n## What ran\nx\n", encoding="utf-8"
        )
        return folder

    def digest(self, conversation: str | None = None) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_digest.print_digest(conversation)
        return out.getvalue()

    def test_every_sessions_decisions_are_in_one_digest(self) -> None:
        first = self.session("20261012T050000Z-1-0", "First task", "approval-required",
                             ["- Rename X? Options: keep, rename. Recommend rename."])
        second = self.session("20261012T050001Z-1-0", "Second task", "blocked",
                              ["- Which module owns Y? Options: a, b. Recommend a.", "- Delete Z? Recommend no."])
        quiet = self.session("20261012T050002Z-1-0", "Quiet task", "success", [])
        text = self.digest()
        self.assertEqual(text.count("Decisions needed"), 1)
        self.assertIn("2 sessions, 3 entries", text)
        for folder, title, stop in ((first, "First task", "approval-required"), (second, "Second task", "blocked")):
            self.assertIn(f"{folder.name}  {title}", text)
            self.assertIn(f"stop: {stop}", text)
            self.assertIn(str(folder / session_report.REPORT_NAME), text)
        self.assertIn("- Which module owns Y? Options: a, b. Recommend a.", text)
        self.assertIn("- Delete Z? Recommend no.", text)
        self.assertNotIn(quiet.name, text)

    def test_each_session_shows_its_priority(self) -> None:
        folder = self.session("20261012T050007Z-1-0", "Ranked", "blocked", ["- Q?"])
        plan = folder / session_plan.PLAN_NAME
        session_plan.set_priority(plan, 8)
        self.assertIn("priority: 8", self.digest())

    def test_a_report_that_is_not_a_hand_back_is_marked(self) -> None:
        self.session("20261012T050008Z-1-0", "Long", "blocked", [f"- Q{index}?" for index in range(11)])
        self.session("20261012T050009Z-1-0", "Disagrees", "success", ["- Q?"], status="blocked")
        text = self.digest()
        self.assertIn("failed hand-back: 11 lines under Decisions needed, more than 10", text)
        self.assertIn("failed hand-back: report.md Stop success means status done, the plan says blocked", text)

    def test_a_failed_hand_back_with_no_decisions_is_in_it(self) -> None:
        silent = self.session("20261012T050010Z-1-0", "No stop", "", [], status="blocked")
        wrong = self.session("20261012T050011Z-1-0", "Disagrees quietly", "success", [], status="blocked")
        text = self.digest()
        self.assertIn(f"{silent.name}  No stop", text)
        self.assertIn("failed hand-back: report.md has no Stop", text)
        self.assertIn(f"{wrong.name}  Disagrees quietly", text)
        self.assertIn("failed hand-back: report.md Stop success means status done, the plan says blocked", text)

    def test_done_and_queued_sessions_are_left_out(self) -> None:
        done = self.session("20261012T050012Z-1-0", "Done", "success", ["- Settled?"])
        queued = self.session("20261012T050013Z-1-0", "Waiting", "", [], status="queued")
        text = self.digest()
        self.assertNotIn(done.name, text)
        self.assertNotIn(queued.name, text)

    def test_with_no_decisions_anywhere_it_says_so(self) -> None:
        self.session("20261012T050003Z-1-0", "Quiet", "success", [])
        self.assertIn("no decisions needed", self.digest())

    def test_conversation_narrows_it(self) -> None:
        root = self.session("20261012T050004Z-1-0", "Root", "success", [])
        inside = self.session("20261012T050005Z-1-0", "Inside", "blocked", ["- In?"], conversation=root.name)
        self.session("20261012T050006Z-1-0", "Outside", "blocked", ["- Out?"])
        text = self.digest(root.name)
        self.assertIn(inside.name, text)
        self.assertNotIn("- Out?", text)


if __name__ == "__main__":
    unittest.main()
