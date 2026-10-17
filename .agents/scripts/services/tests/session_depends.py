#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what a session's dependencies do to it, in `services/session_depends.py` and `services/session_depends_on.py`.

    python .agents/scripts/services/tests/session_depends.py

The subject is the session-dependency design of session 20261016-T122241Z-23960
with the owner's rulings of 2026-10-16, carried out by session
20261016-T191644Z-14044: a session with an unmet `Depends_on` is Blocked, with
the unmet ids as the reason; it cannot be claimed or started; when every cited
session is Complete it is queued again if Memar blocked it, and is then an
ordinary queued session; `claims`, `list`, `digest` and `show` respect and show
it, and `ask-for-new-chats` reads what blocks a coordinator from its plan. Named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one made under the folder `machine/fs_test_scratch.py`
names, which is also the project, a git repository; the records branch is
replaced by a dictionary.

What is pinned, and what each pin is for:

  Status      A queued session with an unmet dependency becomes Blocked and the
              log says Memar did it; a Blocked one whose dependencies are met
              becomes queued only if Memar blocked it; an Active one, and one
              blocked by hand, are never changed.
  Claiming    `claim` and `start` refuse an unmet dependency naming it, and a
              dependency that cannot be found until it is dropped; once met, the
              blocked session is claimed as an ordinary queued one and goes
              Active; `claims` passes a waiting session over, says why, and
              takes it once it is free.
  Writing     `depends-on` and `new --depends-on` add and drop references, refuse
              itself, an unknown id, an unresolvable project and a cycle, and
              leave the other lines of the plan as they were.
  Showing     `list`, `digest` and `show` print each dependency and where it
              stands, who depends on a session, and a blocked session that can
              resume.
  Prompt      `ask-for-new-chats --coordinator` marks as blocking the sessions
              the coordinator's plan cites.
"""
from __future__ import annotations

import contextlib
import io
import subprocess
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
import services.depends_on as depends_on
import services.project_registry as registry
import services.prompts_new_chats as new_chats
import services.session_claim as session_claim
import services.session_claims as session_claims
import services.session_depends as session_depends
import services.session_depends_on as session_depends_on
import services.session_digest as session_digest
import services.session_ensure as session_ensure
import services.session_find as session_find
import services.session_log as session_log
import services.session_plan as session_plan
import services.session_show as session_show
import services.session_start as session_start
from services.session_folder import read_session
from services.claim import Claim


def plan_text(status: str, project: Path, depends: str | None = None, title: str = "T", other: str = "") -> str:
    given = f"Depends_on: {depends}\n" if depends else ""
    return (
        f"---\nTitle: {title}\nStatus: {status.capitalize()}\nOpened: 2026-10-12T00:00:00Z\nProject: {project}\n{other}{given}---\n# {title}\n"
        "\n## Request\nDo it.\n\n## Why\nBecause.\n\n## Steps\n\n## Next\n"
    )


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        subprocess.run(["git", "init", "-q", str(self.fake_root)], check=True, capture_output=True)
        self.project = self.fake_root
        for patched in (
            unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root),
            unittest.mock.patch.object(session_ensure, "project_root", return_value=self.fake_root),
        ):
            patched.start()
            self.addCleanup(patched.stop)
        self.branch: dict[tuple[str, str], bytes] = {}
        read = unittest.mock.patch.object(
            depends_on, "read_from_branch", side_effect=lambda project, sid, name: self.branch.get((sid, name))
        )
        read.start()
        self.addCleanup(read.stop)

    def session(self, sid: str, status: str, depends: str | None = None, report: str | None = None, **more) -> Path:
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        (folder / "plan.md").write_text(plan_text(status, self.project, depends, **more), encoding="utf-8", newline="\n")
        if report is not None:
            (folder / "report.md").write_text(f"---\nTitle: T\nStatus: {report.capitalize()}\n---\n# Report\n", encoding="utf-8", newline="\n")
        return folder

    def finish(self, folder: Path) -> None:
        """Make the session at FOLDER Complete, plan and report."""
        for name, status in (("plan.md", "Complete"), ("report.md", "Complete")):
            path = folder / name
            if path.exists():
                text = path.read_text(encoding="utf-8")
                path.write_text(text.replace("Status: Active", f"Status: {status}").replace("Status: Queued", f"Status: {status}"), encoding="utf-8", newline="\n")
            else:
                path.write_text(f"---\nTitle: T\nStatus: {status}\n---\n# Report\n", encoding="utf-8", newline="\n")

    def status_of(self, folder: Path) -> str:
        return session_plan.read_plan(folder / session_plan.PLAN_NAME).status

    def refused(self, call, *args, **kwargs) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args, **kwargs)
        return str(raised.exception.code)

    def printed(self, call, *args, **kwargs) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            call(*args, **kwargs)
        return out.getvalue()


class Status(Fixture):
    def test_a_queued_session_with_an_unmet_dependency_becomes_blocked_and_the_log_says_memar_did_it(self) -> None:
        self.session("before", "active")
        waiting = self.session("after", "queued", depends="before")
        session_depends.reconcile(read_session(waiting), depends_on.Reader(None))
        self.assertEqual(self.status_of(waiting), "blocked")
        self.assertTrue(session_depends.blocked_by_memar(waiting))
        self.assertIn(session_depends.BLOCKED_EVENT, session_log.log_path(waiting).read_text(encoding="utf-8"))

    def test_a_blocked_session_whose_dependencies_are_met_is_queued_again_only_if_memar_blocked_it(self) -> None:
        before = self.session("before", "active")
        ours = self.session("after-ours", "queued", depends="before")
        by_hand = self.session("after-by-hand", "blocked", depends="before")
        reader = depends_on.Reader(None)
        session_depends.reconcile(read_session(ours), reader)
        self.finish(before)
        session_depends.reconcile_all([read_session(ours), read_session(by_hand)])
        self.assertEqual(self.status_of(ours), "queued")
        self.assertFalse(session_depends.blocked_by_memar(ours))
        self.assertEqual(self.status_of(by_hand), "blocked")

    def test_an_active_session_is_never_changed(self) -> None:
        self.session("before", "active")
        running = self.session("running", "active", depends="before")
        session_depends.reconcile_all([read_session(running)])
        self.assertEqual(self.status_of(running), "active")

    def test_a_session_without_dependencies_is_left_alone_and_nothing_is_logged(self) -> None:
        plain = self.session("plain", "queued")
        session_depends.reconcile_all([read_session(plain)])
        self.assertEqual(self.status_of(plain), "queued")
        self.assertFalse(session_log.log_path(plain).exists())


class Claiming(Fixture):
    def test_claim_refuses_an_unmet_dependency_naming_it_and_blocks_the_session(self) -> None:
        self.session("before", "active")
        waiting = self.session("after", "queued", depends="before")
        why = self.refused(session_claim.claim_folder, waiting)
        self.assertIn("depends on before (active)", why)
        self.assertEqual(self.status_of(waiting), "blocked")
        self.assertFalse((waiting / Claim.NAME).exists())

    def test_once_the_dependency_is_complete_the_blocked_session_is_claimed_as_a_queued_one_and_goes_active(self) -> None:
        before = self.session("before", "active")
        waiting = self.session("after", "queued", depends="before")
        self.refused(session_claim.claim_folder, waiting)
        self.finish(before)
        session_claim.claim_folder(waiting)
        self.assertEqual(self.status_of(waiting), "active")
        self.assertTrue((waiting / Claim.NAME).exists())

    def test_a_plan_complete_with_a_report_that_is_not_does_not_free_it(self) -> None:
        self.session("before", "complete", report="active")
        waiting = self.session("after", "queued", depends="before")
        self.assertIn("plan complete, report active", self.refused(session_claim.claim_folder, waiting))

    def test_a_dependency_that_cannot_be_found_keeps_it_unclaimable_until_the_key_is_dropped(self) -> None:
        waiting = self.session("after", "queued", depends="ghost")
        why = self.refused(session_claim.claim_folder, waiting)
        self.assertIn("ghost (cannot be found", why)
        self.assertIn("--drop", why)
        self.printed(session_depends_on.change, "after", [], ["ghost"])
        session_claim.claim_folder(waiting)
        self.assertEqual(self.status_of(waiting), "active")

    def test_a_blocked_session_by_hand_with_met_dependencies_is_not_claimed(self) -> None:
        self.session("before", "complete", report="complete")
        held = self.session("after", "blocked", depends="before")
        self.assertIn("not queued", self.refused(session_claim.claim_folder, held))

    def test_start_refuses_an_unmet_dependency_and_a_met_one_starts(self) -> None:
        before = self.session("before", "active")
        waiting = self.session("after", "active", depends="before")
        why = self.refused(session_start.start_passages, "after")
        self.assertIn("depends on before (active)", why)
        self.assertIn("started", why)
        self.finish(before)
        self.assertEqual(session_depends.refusal(waiting, "start"), None)

    def test_claims_passes_a_waiting_session_over_says_why_and_takes_it_once_free(self) -> None:
        before = self.session("before", "active")
        waiting = self.session("after", "queued", depends="before", other="Priority: 9\n")
        plain = self.session("plain", "queued")
        out = self.printed(session_claims.claims, 2, str(self.project))
        self.assertIn("claimed 1 of 2", out)
        self.assertIn("after  waiting: before (active)", out)
        self.assertEqual(self.status_of(plain), "active")
        self.assertEqual(self.status_of(waiting), "blocked")
        self.finish(before)
        out = self.printed(session_claims.claims, 2, str(self.project))
        self.assertIn("claimed 1 of 2", out)
        self.assertEqual(self.status_of(waiting), "active")


class Writing(Fixture):
    def test_add_and_drop_write_one_key_and_keep_every_other_line(self) -> None:
        self.session("one", "active")
        two = self.session("two", "queued", other="Priority: 7\n")
        before = (two / "plan.md").read_text(encoding="utf-8")
        out = self.printed(session_depends_on.change, "two", ["one"], [])
        self.assertIn("Depends_on: one, was (none)", out)
        text = (two / "plan.md").read_text(encoding="utf-8")
        self.assertEqual(text.replace("Status: Blocked", "Status: Queued").replace("Depends_on: one\n", ""), before)
        self.assertEqual(self.status_of(two), "blocked")
        self.assertIn("one (active)", out)
        self.printed(session_depends_on.change, "two", [], ["one"])
        self.assertNotIn("Depends_on", (two / "plan.md").read_text(encoding="utf-8"))
        self.assertEqual(self.status_of(two), "queued")

    def test_it_refuses_itself_an_unknown_id_a_drop_that_is_not_there_and_a_cycle(self) -> None:
        self.session("a", "queued")
        self.session("b", "queued", depends="a")
        self.assertIn("cannot depend on itself", self.refused(session_depends_on.change, "a", ["a"], []))
        self.assertIn("cannot be found", self.refused(session_depends_on.change, "a", ["ghost"], []))
        self.assertIn("is not in", self.refused(session_depends_on.change, "a", [], ["b"]))
        self.assertIn("a → b → a", self.refused(session_depends_on.change, "a", ["b"], []))
        self.assertNotIn("Depends_on", (memar_fs.session_dir("a") / "plan.md").read_text(encoding="utf-8"))

    def test_a_dependency_on_a_session_of_another_project_is_written_as_project_and_id(self) -> None:
        other = self.fake_root / "organization"
        other.mkdir()
        registry.add_project("organization", other, [])
        self.session("theirs", "active")
        mine = self.session("mine", "queued")
        self.printed(session_depends_on.change, "mine", ["organization/theirs"], [])
        self.assertIn("Depends_on: organization/theirs", (mine / "plan.md").read_text(encoding="utf-8"))
        self.assertEqual(self.status_of(mine), "blocked")
        why = self.refused(session_depends_on.change, "mine", ["nowhere-at-all/theirs"], [])
        self.assertIn("project nowhere-at-all does not resolve", why)

    def test_a_session_closed_and_kept_on_the_branch_satisfies_a_dependency(self) -> None:
        self.branch[("kept", "plan.md")] = plan_text("complete", self.project).encode()
        self.branch[("kept", "report.md")] = b"---\nTitle: T\nStatus: Complete\n---\n# Report\n"
        mine = self.session("mine", "queued")
        self.printed(session_depends_on.change, "mine", ["kept"], [])
        self.assertEqual(self.status_of(mine), "queued")

    def test_new_writes_a_blocked_plan_for_an_unmet_dependency_and_a_queued_one_for_a_met_one(self) -> None:
        before = self.session("before", "active")
        sid, folder = session_ensure.ensure_session("later", "Later", None, True, project=str(self.project), depends_on=["before"])
        self.assertEqual(self.status_of(folder), "blocked")
        self.assertIn("Depends_on: before", (folder / "plan.md").read_text(encoding="utf-8"))
        self.finish(before)
        _, free = session_ensure.ensure_session("free", "Free", None, True, project=str(self.project), depends_on=["before"])
        self.assertEqual(self.status_of(free), "queued")
        self.assertIn("cannot depend on itself", self.refused(session_ensure.ensure_session, "me", "Me", None, True, project=str(self.project), depends_on=["me"]))
        self.assertFalse(memar_fs.session_dir("me").exists())

    def test_new_on_an_existing_queued_plan_adds_and_blocks(self) -> None:
        self.session("before", "active")
        waiting = self.session("later", "queued")
        session_ensure.ensure_session("later", depends_on=["before"], project=str(self.project))
        self.assertEqual(self.status_of(waiting), "blocked")

    def test_the_verb_and_the_flag_are_named_from_the_one_key(self) -> None:
        self.assertEqual(session_depends.DEPENDS_COMMAND, "depends-on")
        self.assertEqual(depends_on.DependsOn.KEY.written, "Depends_on")


class Showing(Fixture):
    def test_list_shows_each_dependency_with_where_it_stands_and_who_depends_on_a_session(self) -> None:
        before = self.session("before", "active")
        self.session("after", "queued", depends="before, ghost")
        out = self.printed(session_find.list_sessions, project=str(self.project))
        self.assertIn("Depends_on: before (active), ghost (cannot be found)", out)
        self.assertIn("Depends_for: after", out)
        self.assertIn("status: blocked", out)
        self.assertIn("ghost: cannot be found", out)
        self.assertIn("it stays unclaimable until the key is dropped", out)
        only = self.printed(session_find.list_sessions, status="blocked", project=str(self.project))
        self.assertIn("after", only)
        self.assertNotIn(before.name + "  T", only)

    def test_list_brings_a_released_session_up_to_date(self) -> None:
        before = self.session("before", "active")
        waiting = self.session("after", "queued", depends="before")
        self.printed(session_find.list_sessions, project=str(self.project))
        self.assertEqual(self.status_of(waiting), "blocked")
        self.finish(before)
        self.printed(session_find.list_sessions, project=str(self.project))
        self.assertEqual(self.status_of(waiting), "queued")

    def test_a_blocked_session_whose_dependencies_are_complete_is_said_to_be_able_to_resume(self) -> None:
        self.session("before", "complete", report="complete")
        self.session("coordinator", "blocked", depends="before")
        out = self.printed(session_find.list_sessions, project=str(self.project))
        self.assertIn("every Depends_on is Complete: it can resume", out)

    def test_digest_gathers_a_session_blocked_by_its_dependencies_with_what_it_waits_for(self) -> None:
        self.session("before", "active")
        self.session("after", "queued", depends="before")
        out = self.printed(session_digest.print_digest, project=str(self.project))
        self.assertIn("after", out)
        self.assertIn("blocked by Depends_on: before (active)", out)

    def test_show_prints_the_dependencies_and_the_sessions_that_depend_on_the_session(self) -> None:
        self.session("before", "active", report="active")
        self.session("after", "queued", depends="before", report="")
        out = self.printed(session_show.show, "before", self.project, [])
        self.assertIn("=== dependencies", out)
        self.assertIn("Depends_for: after", out)
        out = self.printed(session_show.show, "after", self.project, [])
        self.assertIn("Depends_on: before (active)", out)


class Prompt(Fixture):
    def test_the_sessions_a_coordinators_plan_cites_are_marked_as_blocking(self) -> None:
        for sid in ("one", "two"):
            folder = self.session(sid, "queued")
        self.session("coordinator", "blocked", depends="one")
        with unittest.mock.patch.object(new_chats, "brief_text", return_value="BRIEF"):
            out = self.printed(new_chats.print_chats, ["one", "two"], [], "coordinator")
            by_hand = self.printed(new_chats.print_chats, ["one", "two"], ["two"], "coordinator")
        self.assertIn("— blocks\n", out.split("two")[0])
        self.assertEqual(out.count("— blocks"), 1)
        self.assertEqual(by_hand.count("— blocks"), 2)
        self.assertIn("no coordinator session", self.refused(new_chats.print_chats, ["one"], [], "nobody"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
