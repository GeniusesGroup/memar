#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a plan's dependencies, in `services/depends_on.py`.

    python .agents/scripts/services/tests/depends_on.py

The subject is the process a plan's `Depends_on` names: the sessions it cannot
start without, each an id or `project/id`, met when the cited session's plan
and report both state Complete, read from its folder or from its project's
records branch once the folder is gone, and refused when written for itself,
for a session or a project that does not resolve, or in a cycle. The design is
session 20261016-T122241Z-23960's, with the owner's rulings of 2026-10-16
(session 20261016-T191644Z-14044). Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one made under the folder `machine/fs_test_scratch.py`
names, and the records branch is replaced by a dictionary.

What is pinned, and what each pin is for:

  Writing    A reference is an id or project/id; a list is one line, in order,
             none twice; reading never refuses.
  Met        Only a cited session whose plan and report both say Complete is
             met; one that is not found, or whose project does not resolve,
             says why; a closed session is read from the branch.
  Refusing   A plan is refused a dependency on itself, on what cannot be found,
             and one that makes a cycle of any length, naming the path.
"""
from __future__ import annotations

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
from services.depends_on import DependsOn, Reader, Ref, refused_for_writing
from services.session_record import PlanKey


def plan_text(status: str, depends: str | None = None, project: str = "P") -> str:
    given = f"Depends_on: {depends}\n" if depends else ""
    return (
        f"---\nTitle: T\nStatus: {status.capitalize()}\nOpened: 2026-10-12T00:00:00Z\nProject: {project}\n{given}---\n# T\n"
        "\n## Request\nDo it.\n\n## Why\n\n## Steps\n\n## Next\n"
    )


def report_text(status: str) -> str:
    return f"---\nTitle: T\nStatus: {status.capitalize()}\n---\n# Report\n"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.branch: dict[tuple[str, str], bytes] = {}
        read = unittest.mock.patch.object(
            depends_on, "read_from_branch", side_effect=lambda project, sid, name: self.branch.get((sid, name))
        )
        read.start()
        self.addCleanup(read.stop)

    def session(self, sid: str, status: str, report: str | None = None, depends: str | None = None) -> Path:
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        (folder / "plan.md").write_text(plan_text(status, depends, str(self.fake_root)), encoding="utf-8", newline="\n")
        if report is not None:
            (folder / "report.md").write_text(report_text(report), encoding="utf-8", newline="\n")
        return folder

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)


class Writing(unittest.TestCase):
    def test_a_reference_is_an_id_or_a_project_and_an_id(self) -> None:
        self.assertEqual(Ref.parse("20261016-T1-2"), Ref("20261016-T1-2"))
        self.assertEqual(Ref.parse(" organization/20261016-T1-2 "), Ref("20261016-T1-2", "organization"))
        self.assertEqual(str(Ref("a", "organization")), "organization/a")
        for bad in ("", "a b", "/a", "a/", "../x"):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    Ref.parse(bad)

    def test_a_list_keeps_its_order_and_names_each_once_on_one_line(self) -> None:
        refs = DependsOn.checked("b, a,b ,, organization/c")
        self.assertEqual(refs.text(), "b, a, organization/c")
        self.assertEqual(refs.ids(), ["b", "a", "c"])
        self.assertEqual(DependsOn.checked(""), ())
        self.assertIn("one line", str(self.assertRaises(SystemExit) and self._refused("a\nb")))

    def _refused(self, text: str) -> str:
        try:
            DependsOn.checked(text)
        except SystemExit as refused:
            return str(refused.code)
        return ""

    def test_reading_a_plan_never_refuses_and_leaves_out_what_is_no_reference(self) -> None:
        front = {PlanKey.DEPENDS_ON.key: "a, no good, /x, b"}
        self.assertEqual(DependsOn.of(front).ids(), ["a", "b"])
        self.assertEqual(DependsOn.of(None), ())
        self.assertEqual(DependsOn.of({}), ())

    def test_the_key_and_its_inverse_are_each_declared_once(self) -> None:
        self.assertEqual(PlanKey.DEPENDS_ON.written, "Depends_on")
        self.assertEqual(depends_on.DEPENDS_FOR, "Depends_for")


class Met(Fixture):
    def reason(self, ref: str, home: Path | None = None) -> list[str]:
        return Reader(home or self.fake_root).unmet([Ref.parse(ref)])

    def test_only_a_plan_and_a_report_both_complete_are_met(self) -> None:
        self.session("done", "complete", "complete")
        self.session("running", "active")
        self.session("report-lags", "complete", "active")
        self.session("no-report", "complete")
        self.assertEqual(self.reason("done"), [])
        self.assertEqual(self.reason("running"), ["running (active)"])
        self.assertEqual(self.reason("report-lags"), ["report-lags (plan complete, report active)"])
        self.assertEqual(self.reason("no-report"), ["no-report (plan complete, report without a status)"])

    def test_a_session_that_is_nowhere_says_it_cannot_be_found(self) -> None:
        [why] = self.reason("gone")
        self.assertTrue(why.startswith("gone (cannot be found"), why)

    def test_a_closed_session_is_read_from_the_records_branch(self) -> None:
        self.branch[("kept", "plan.md")] = plan_text("complete").encode()
        self.branch[("kept", "report.md")] = report_text("complete").encode()
        self.branch[("half", "plan.md")] = plan_text("complete").encode()
        self.assertEqual(self.reason("kept"), [])
        self.assertEqual(self.reason("half"), ["half (plan complete, report without a status)"])

    def test_a_session_of_another_project_is_found_through_that_project_by_name(self) -> None:
        other = self.fake_root / "other-project"
        other.mkdir()
        registry.add_project("other-project", other, [])
        self.session("theirs", "complete", "complete")
        self.assertEqual(self.reason("other-project/theirs"), [])
        [why] = self.reason("nobody-knows-this/theirs")
        self.assertIn("project nobody-knows-this does not resolve", why)

    def test_a_cited_session_is_read_once_for_a_run(self) -> None:
        self.session("done", "complete", "complete")
        reader = Reader(self.fake_root)
        with unittest.mock.patch.object(depends_on, "read_report_status", wraps=depends_on.read_report_status) as read:
            reader.unmet([Ref("done")])
            reader.unmet([Ref("done")])
        self.assertEqual(read.call_count, 1)


class Refusing(Fixture):
    def check(self, sid: str, text: str) -> None:
        refs = DependsOn.checked(text)
        refused_for_writing(sid, refs, Reader(self.fake_root))

    def test_a_session_cannot_depend_on_itself(self) -> None:
        self.session("a", "queued")
        self.assertIn("cannot depend on itself", self.refused(self.check, "a", "a"))

    def test_what_cannot_be_found_is_refused_with_why(self) -> None:
        self.session("a", "queued")
        why = self.refused(self.check, "a", "ghost")
        self.assertIn("Depends_on ghost: cannot be found", why)

    def test_a_cycle_of_any_length_is_refused_naming_the_path(self) -> None:
        self.session("a", "queued")
        self.session("b", "queued", depends="a")
        self.session("c", "queued", depends="b")
        why = self.refused(self.check, "a", "c")
        self.assertIn("a → c → b → a", why)
        self.assertIn("cycle", why)

    def test_a_chain_that_is_not_a_cycle_is_accepted(self) -> None:
        self.session("a", "queued")
        self.session("b", "queued", depends="a")
        self.session("c", "queued")
        self.check("c", "b")

    def test_a_dependency_already_written_that_no_longer_resolves_is_not_refused_when_another_is_added(self) -> None:
        self.session("a", "queued")
        self.session("b", "complete", "complete")
        whole = DependsOn.checked("ghost, b")
        refused_for_writing("a", whole, Reader(self.fake_root), DependsOn.checked("b"))
        self.assertIn("ghost", self.refused(refused_for_writing, "a", whole, Reader(self.fake_root)))

    def test_a_cycle_already_written_is_met_when_read_and_does_not_loop_for_ever(self) -> None:
        self.session("a", "queued", depends="b")
        self.session("b", "queued", depends="a")
        reader = Reader(self.fake_root)
        self.assertEqual(reader.cycle("a", [Ref("b")]), ["a", "b", "a"])
        self.assertIsNone(Reader(self.fake_root).cycle("zzz", [Ref("a")]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
