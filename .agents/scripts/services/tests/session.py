#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar session` in `services/session.py` and the services that declare its verbs.

    python .agents/scripts/services/tests/session.py

The subject is the session command — its help, its arguments, and which
service answers each verb — named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
What each service does is pinned by its own suite beside this one; a behavior
pinned in two files is one of them to forget.

Nothing here writes outside its scratch folder. The Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names, and removed again. The command is assembled by the launcher from the
session services alone, so another domain's services are not this suite's
subject. The subprocesses run ask for `--help` only, which resolves no root and
writes nothing.

What is pinned, and what each pin is for:

  HelpSaysWhatToRun  `memar session --help` says what to run, that one session
                     is one task, the shape of plan.md and its status, how a
                     further task is linked with --parent, how another session
                     continues one, and when its starter may close it; each
                     verb's own help says what it accepts, and `new`'s points
                     here rather than repeating it. It also says that
                     the folder's top holds plan.md and report.md and the rest
                     goes in role folders, whose names it leaves to
                     `memar module folders --help`, that report.md is written before
                     work on a task ends with a Stop the plan's Status agrees
                     with, and that a folder may lie in the project's own
                     session location — relative or absolute, never the
                     project's top folder or a root — which the sweep never
                     reaches, which `list` shows only with --project or
                     --conversation, and which keeps its own log. It says
                     how a task is handed to a sub-agent: the delegator
                     opens its session, writes its plan, and hands only the
                     brief, which `brief ID` prints again. The help says
                     nothing about how the folder is arranged: the mechanism
                     is a DevActionNote, and the why is pinned to the services'
                     own docstrings, where it is maintained.
                     It also says how a conversation that only adds work
                     queues a task with a priority and never runs it, and how
                     an agent told only to "do some of the queued tasks", or N
                     of a project's, works them: `list --status queued`,
                     `claims N --project X` — the project always named, no
                     default and no all, the owner asked when it is unknown
                     — one fresh sub-agent per printed brief, never
                     in its own context, each report's Stop and Decisions
                     needed read and its status checked, and one `digest
                     --conversation` for the owner at the end, holding failed
                     hand-backs and leaving out done sessions; that the only
                     writes into another session's folder are the queued or
                     delegated plan by the session it came from and a
                     text-only sub-agent's report and Status by its
                     coordinator; that priority is 1 to 10, 5 when
                     absent, higher sooner, and changed with `priority`; what a
                     short hand-back is; how long a claim holds and why; and
                     that no external runner is involved. `memar --help`'s
                     line for `session` names queued tasks, so an agent
                     starting from the top reaches it.
  EachServiceDeclaresItsVerb
                     Each verb is declared by the service that answers it, and
                     the services the others share declare none.
  VerbsDispatch      Each verb reaches its one service with the arguments as
                     parsed; the verb that added tasks to a plan is gone.
  MovedBeforeAnyVerb The quiet folders an earlier Memar left directly in temp/
                     are moved into temp/sessions/ before any verb runs, so the
                     first command after an update already finds them there;
                     one at work is listed where it is; asking for help moves
                     nothing.
  CommandEndToEnd    What a caller types — `new`, then `list` — opens a folder,
                     prints its id and path, and finds it again, through the
                     real services; and `memar session <verb> --help` answers
                     through the launcher for every verb.
  StaleCopiesAreNotNew
                     `new` does not ask whether the skill copies are stale:
                     that is `memar update`'s question.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from importlib.machinery import SourceFileLoader
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

import machine.fs_memar as memar_fs
import services.session as session
import services.session_brief as session_brief
import services.session_claim as session_claim
import services.session_claims as session_claims
import services.session_close as session_close
import services.session_digest as session_digest
import services.session_find as session_find
import services.session_folder as session_folder
import services.session_gc as session_gc
import services.session_id as session_id
import services.session_location as session_location
import services.session_log as session_log
import services.session_migrate as session_migrate
import services.session_new as session_new
import services.session_plan as session_plan
import services.session_priority as session_priority
import services.session_report as session_report

LAUNCHER = SCRIPTS / "memar"

# The launcher is loaded under a name of its own, since its file has no
# extension for the import system to recognize.
_spec = importlib.util.spec_from_loader("memar_launcher", SourceFileLoader("memar_launcher", str(LAUNCHER)))
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)

SESSION_SERVICES = [name for name in launcher.services() if name.partition(launcher.DOMAIN_SEPARATOR)[0] == "session"]
TITLE = "Test the session command"


def command(*arguments: str) -> int:
    """`memar session ARGUMENTS`, assembled from the session services alone."""
    with unittest.mock.patch.object(launcher, "services", return_value=SESSION_SERVICES):
        return launcher.main(["session", *arguments])


def run_help(*arguments: str) -> str:
    environment = dict(os.environ, COLUMNS="80", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, str(LAUNCHER), "session", *arguments, "--help"], capture_output=True, env=environment
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.decode("utf-8").replace("\r\n", "\n")


def flat(text: str) -> str:
    return " ".join(text.split())


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        # `new` asks the project it runs in where to put a folder; a scratch
        # one, so a real project's preferences never reach this suite.
        project = unittest.mock.patch.object(session_new, "project_root", return_value=self.fake_root)
        project.start()
        self.addCleanup(project.stop)

    def run_main(self, *arguments: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = command(*arguments)
        self.assertEqual(code, 0)
        return out.getvalue()


class HelpSaysWhatToRun(unittest.TestCase):
    MECHANISM = ("shared-tree collisions", "advisory locks", "intent notes", "OS-temp", "fails closed", "services/")

    def test_the_help_says_what_to_run_and_what_to_do_afterwards(self) -> None:
        text = run_help()
        for phrase in (
            "One session is one task",
            "memar session new --title TITLE",
            "--parent ID",
            "memar session list --conversation ID",
            "memar session list --status STATUS",
            "memar session close",
            "memar session gc",
            "--session-id",
            "person who started",
            "recycle bin",
            f"{session_gc.SESSION_IDLE_DAYS} days",
            "Once a day",
            "whose status is done",
            "never close a session you did not\nopen",
        ):
            self.assertIn(phrase, text)

    def test_the_help_gives_the_plan_and_how_to_continue_from_it(self) -> None:
        text = run_help()
        for phrase in (
            "plan.md",
            "title: TITLE",
            "opened:",
            "project:",
            "parent: ID, and conversation:",
            "Status: open",
            "A task is one thing the person asked for",
            "A session is the\nrecord of one task",
            "Agent, sub-agent, and conversation are defined in\n`memar --help`",
            "## Request",
            "## Why",
            "in its own words, from the person's request",
            "## Steps",
            "## Next",
            "open, blocked, or done",
            "set done once its check has passed",
            "works in its own session",
            "memar session list --status open",
            "memar session new --session-id ID",
            "start from its Next",
        ):
            self.assertIn(phrase, text)

    def test_the_help_gives_the_report_and_when_to_write_it(self) -> None:
        text = run_help()
        for phrase in (
            "The folder's top holds plan.md and report.md",
            "role folder of its kind",
            "`memar module folders --help` names them",
            "# Report\n    Stop:\n\n    ## What ran\n    ## Check\n    ## Result\n    ## Left open",
            "finished or not",
            "Stop: success, clean no-op",
            "Status: done",
            "Stop: blocked, approval-required",
            "Stop: exhausted, no progress",
            "`list` marks a session whose report and plan disagree",
        ):
            self.assertIn(phrase, text)

    def test_the_help_says_where_a_folder_is_and_what_the_sweep_never_reaches(self) -> None:
        text = flat(run_help())
        for phrase in (
            "under temp/sessions/",
            "sets `sessions` in its .agents/memar/preferences.md",
            "says on a line of its own",
            "relative to the project's top folder, or an absolute one",
            "drive or filesystem root is refused",
            "inside Memar's own temp/ is not used",
            "The sweep reaches only Memar's own temp/sessions/",
            "keeping, committing, or deleting it is the project's",
            "`gc` names those locations",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("lies in Memar's own checkout, also when", text)

    def test_the_help_says_how_a_task_is_handed_to_a_sub_agent(self) -> None:
        text = flat(run_help())
        for phrase in (
            "memar session brief ID",
            "and print the brief that hands it over",
            "open its session yourself with `--parent`",
            "write the whole task into its plan.md — the Request, the check that says it is done, the shape of its report, and its Why, in your own words from the person's request",
            "hand the sub-agent only the brief `new` prints, which `brief ID` prints again",
            "takes that session up and opens none, and does not rewrite its Request",
        ):
            self.assertIn(phrase, text)

    def test_the_help_says_what_list_shows_and_where_each_log_is(self) -> None:
        text = flat(run_help())
        for phrase in (
            "memar session list [TEXT] find Memar's own session folders",
            "memar session list --project [PATH]",
            "`--project` lists every session of a project, in its own location or in Memar's",
            "`--conversation` every session of a conversation, wherever it lies",
            "Each location keeps its own log of what was done to its folders, sessions.log at its top",
            "those it no longer records because their folder is gone",
        ):
            self.assertIn(phrase, text)

    def test_the_help_says_how_a_task_is_queued_with_a_priority_and_never_run(self) -> None:
        text = flat(run_help())
        for phrase in (
            "Status is queued, open, blocked, or done",
            "memar session new --title TITLE --parent ID --queued [--priority N]",
            "memar session priority ID N",
            "new --session-id ID --queued",
            "never do a queued session's work in your own context",
            "To only add work",
            "priority: a whole number from 1 to 10, 5 when absent; the higher goes sooner",
            "Anyone may change it",
        ):
            self.assertIn(phrase, text)

    def test_the_help_says_how_an_agent_told_only_to_do_queued_tasks_works_them(self) -> None:
        # The owner's prompt is one line — "do some of the queued Memar tasks",
        # "do 5 tasks of project X" — so the help alone must carry the recipe.
        text = flat(run_help())
        for phrase in (
            "do some of the queued tasks",
            "`--project` is required: one run serves one project",
            "\"do 5 tasks of X\" means `claims 5 --project X`",
            "there is no default project and no way to take from all",
            "ask the owner rather than guess",
            "memar session list --status queued",
            "memar session claims N --project [PATH]",
            "N is yours to choose",
            "the highest priority first, the oldest first among equals",
            "one fresh sub-agent per session",
            "never in your own context",
            "read its report.md: its Stop and its Decisions needed",
            "a Stop that disagrees with its plan",
            "memar session digest [--conversation ID]",
            "run `memar session digest --conversation ID`, ID your own session's",
            "give the owner that one digest",
            "memar session claim ID",
            f"lapses after {session_claim.CLAIM_STALE_SECONDS // 3600} hours",
            "nothing keeps a claim fresh",
            "at most 10 lines under a `## Decisions needed` heading",
            "failed hand-back",
            "`digest` gathers into one every session's Decisions needed and every failed hand-back",
            "it leaves out done sessions",
            "Two writes reach another session's folder, both from the session it came from",
            "writes the report.md of a sub-agent that could only return text, and sets that plan.md's Status",
            "Memar starts no agent",
        ):
            self.assertIn(phrase, text)

    def test_no_external_runner_is_left_in_the_help(self) -> None:
        texts = [run_help(), *(run_help(verb) for verb in ("new", "claim", "claims", "digest", "priority"))]
        for text in texts:
            for word in ("launch", "runner", "`run`", "session run"):
                self.assertNotIn(word, text)

    def test_the_top_help_leads_to_queued_tasks(self) -> None:
        self.assertIn("queued tasks", session.SUMMARY)

    def test_the_command_lists_keep_one_column(self) -> None:
        columns = set()
        for line in session.DESCRIPTION.splitlines():
            if line.startswith("    memar session"):
                found = re.search(r"\S {2,}(?=\S)", line)
                if found:
                    columns.add(found.end())
            elif line.startswith(" " * 20) and line.strip():
                columns.add(len(line) - len(line.lstrip()))
        self.assertEqual(len(columns), 1, columns)

    def test_each_verbs_help_says_what_it_accepts(self) -> None:
        for verb, phrases in (
            ("new", ("--session-id", "--title TITLE", "--parent ID", "for one task", "first session of that conversation",
                     "said in `memar session --help`")),
            ("list", ("whose id, title, or project holds TEXT", "one word or a short phrase, not a question",
                      "--status {queued,open,blocked,done}", "--conversation ID", "--idle-days DAYS",
                      "--project [PATH]", "List Memar's own session folders", "the git top-level of the current folder")),
            ("brief", ("ID", "ready to paste", "`new --parent` prints", "said in `memar session --help`")),
            ("gc", ("--session-id", "--idle-days DAYS", "never swept", "cannot be read", "at least 1", "whose status is done")),
            ("close", ("--session-id",)),
            ("new", ("--queued", "an existing open one no one has claimed is queued", "--priority N", "1 to 10",
                     "higher goes sooner")),
            ("claim", ("ID", "another agent holds, is refused", "taken over", "said in `memar session --help`")),
            ("claims", ("N", "highest priority first", "oldest", "brief", "Fewer queued than N is not an error", "no default",
                        "--project is required: one run serves one project",
                        "never mixes two projects'", "no default project and no way to take from all",
                        "\"Do 5 tasks of X\" means `claims 5 --project X`", "ask the owner rather than guess",
                        "one fresh sub-agent per session", "said in `memar session --help`")),
            ("priority", ("ID", "N", "1 to 10", "5 when", "higher goes sooner", "Anyone, a person or an agent, may change it")),
            ("digest", ("--conversation ID", "Decisions needed", "priority", "failed hand-back",
                        "entries or not", "Done and queued sessions are left out",
                        "said in `memar session --help`")),
        ):
            with self.subTest(verb=verb):
                text = flat(run_help(verb))
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_new_points_at_the_domain_help_rather_than_repeating_it(self) -> None:
        text = flat(run_help("new"))
        for phrase in ("finished or not", "Stop: blocked", "role folder", ".agents/memar/preferences.md", "sweep"):
            self.assertNotIn(phrase, text)

    def test_the_help_does_not_carry_the_implementation(self) -> None:
        text = run_help()
        for phrase in self.MECHANISM:
            self.assertNotIn(phrase, text)

    def test_the_why_is_in_the_files_the_implementer_reads(self) -> None:
        # Not a second copy: each service's own docstring, the one text
        # addressed to whoever opens it, and the domain's says where they are.
        for name in ("session_new", "session_brief", "session_find", "session_close", "session_gc", "session_migrate"):
            self.assertIn(name, session.__doc__)
        for module, phrases in (
            (session_new, ("shared-tree collisions", "advisory locks", "intent notes", "One session is one task")),
            (session_brief, ("same text for every task", "stated once in the delegator's words")),
            (session_plan, ("disputed", "handoff", "still read")),
            (session_gc, ("Idle is not the same as", "once a day")),
            (session_find, ("listed together",)),
        ):
            for phrase in phrases:
                self.assertIn(phrase, flat(module.__doc__), module.__name__)


class EachServiceDeclaresItsVerb(unittest.TestCase):
    class Recorded:
        """Where a service's verb goes, remembering the names it registers."""

        def __init__(self) -> None:
            self.names: list[str] = []
            self.group = argparse.ArgumentParser().add_subparsers()

        def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
            self.names.append(name)
            return self.group.add_parser(name, **kwargs)

    def test_each_verb_is_declared_by_the_service_that_answers_it(self) -> None:
        for module, declared in (
            (session, ["session"]),
            (session_new, ["new"]),
            (session_brief, ["brief"]),
            (session_find, ["list"]),
            (session_close, ["close"]),
            (session_gc, ["gc"]),
            (session_claim, ["claim"]),
            (session_claims, ["claims"]),
            (session_priority, ["priority"]),
            (session_digest, ["digest"]),
        ):
            with self.subTest(verbs=declared):
                verbs = self.Recorded()
                run = module.describe(verbs)
                self.assertEqual(verbs.names, declared)
                self.assertTrue(callable(run))

    def test_the_shared_services_declare_no_verb(self) -> None:
        for module in (session_plan, session_report, session_folder, session_location, session_log, session_id, session_migrate):
            with self.subTest(module=module.__name__):
                self.assertFalse(hasattr(module, launcher.DESCRIBE))

    def test_the_command_offers_the_nine_verbs_in_the_order_of_their_services(self) -> None:
        def verbs_of(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
            found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            return dict(found[0].choices) if found else {}

        top, before = launcher.assemble(SESSION_SERVICES)
        self.assertEqual(before, [])
        self.assertEqual(
            list(verbs_of(verbs_of(top)["session"])),
            ["brief", "claim", "claims", "close", "digest", "list", "gc", "new", "priority"],
        )


class VerbsDispatch(Fixture):
    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in (
            (["new", "--title", "T"], session_new, "open_session", (None, "T", None)),
            (["new", "--session-id", "s-1", "--parent", "s-0"], session_new, "open_session", ("s-1", None, "s-0")),
            (["list"], session_find, "list_sessions", (None, None, None, None, None)),
            (["list", "word", "--status", "blocked", "--idle-days", "3", "--conversation", "s-0"],
             session_find, "list_sessions", ("word", "blocked", 3.0, "s-0", None)),
            (["list", "word", "--project"], session_find, "list_sessions", ("word", None, None, None, "")),
            (["list", "--project", "C:/work/p"], session_find, "list_sessions", (None, None, None, None, "C:/work/p")),
            (["brief", "s-1"], session_brief, "print_brief", ("s-1",)),
            (["gc"], session_gc, "collect", (None, None)),
            (["gc", "--session-id", "s-1", "--idle-days", "2"], session_gc, "collect", ("s-1", 2.0)),
            (["close", "--session-id", "s-1"], session_close, "close", ("s-1",)),
            (["new", "--title", "T", "--queued"], session_new, "open_session", (None, "T", None, True, None)),
            (["new", "--title", "T", "--queued", "--priority", "8"], session_new, "open_session",
             (None, "T", None, True, 8)),
            (["list", "--status", "queued"], session_find, "list_sessions", (None, "queued", None, None, None)),
            (["claim", "s-1"], session_claim, "claim", ("s-1",)),
            (["claims", "5"], session_claims, "claims", (5, None)),
            (["claims", "5", "--project"], session_claims, "claims", (5, "")),
            (["claims", "2", "--project", "C:/work/p"], session_claims, "claims", (2, "C:/work/p")),
            (["priority", "s-1", "8"], session_priority, "set_session_priority", ("s-1", "8")),
            (["digest"], session_digest, "print_digest", (None,)),
            (["digest", "--conversation", "s-0"], session_digest, "print_digest", ("s-0",)),
        ):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service:
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_the_task_verb_is_gone_and_an_unknown_status_refused(self) -> None:
        for argv in (["task", "--session-id", "s-1", "--title", "T"], ["list", "--status", "released"], ["close"]):
            with self.subTest(argv=argv):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv)


class MovedBeforeAnyVerb(Fixture):
    def test_the_move_runs_before_each_verbs_service(self) -> None:
        for argv, module, name in (
            (["new", "--title", "T"], session_new, "open_session"),
            (["list"], session_find, "list_sessions"),
            (["gc"], session_gc, "collect"),
            (["close", "--session-id", "s-1"], session_close, "close"),
            (["brief", "s-1"], session_brief, "print_brief"),
        ):
            with self.subTest(argv=argv):
                order = unittest.mock.Mock()
                with unittest.mock.patch.object(session_migrate, "migrate", order.migrate), \
                        unittest.mock.patch.object(module, name, getattr(order, name)):
                    command(*argv)
                self.assertEqual([call[0] for call in order.mock_calls], ["migrate", name])

    def test_asking_for_help_moves_nothing(self) -> None:
        for argv in (["--help"], ["new", "--help"], ["list", "--help"], ["gc", "--help"], ["close", "--help"], ["brief", "--help"]):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(session_migrate, "migrate") as migrate:
                    with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
                        command(*argv)
                self.assertEqual(raised.exception.code, 0)
                migrate.assert_not_called()

    def left_in_temp(self, sid: str, idle_days: float) -> Path:
        left = memar_fs.scratch_root() / sid
        left.mkdir(parents=True)
        plan = left / session_plan.PLAN_NAME
        plan.write_text(
            session_plan.plan_skeleton("Left behind", "2026-10-09T12:00:00Z", Path("/w")), encoding="utf-8", newline="\n"
        )
        when = time.time() - idle_days * 24 * 60 * 60
        for path in (plan, left):
            os.utime(path, (when, when))
        return left

    def test_a_quiet_folder_left_in_temp_is_listed_where_the_first_command_moved_it(self) -> None:
        left = self.left_in_temp("20261009T120000Z-42-0", idle_days=2)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            listed = self.run_main("list")
        self.assertIn("20261009T120000Z-42-0  Left behind", listed)
        self.assertIn(f"path: {memar_fs.session_dir('20261009T120000Z-42-0')}", listed)
        self.assertIn("moved from temp/ into temp/sessions/", err.getvalue())
        self.assertFalse(left.exists())

    def test_a_folder_at_work_in_temp_is_listed_where_it_is(self) -> None:
        left = self.left_in_temp("20261009T120000Z-43-0", idle_days=0)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            listed = self.run_main("list")
        self.assertIn(f"path: {left}", listed)
        self.assertEqual(err.getvalue(), "")
        self.assertTrue(left.is_dir())


class CommandEndToEnd(Fixture):
    def test_new_prints_the_id_and_path_and_list_finds_it(self) -> None:
        text = self.run_main("new", "--session-id", "20261003T000000Z-1-0", "--title", TITLE)
        path = memar_fs.session_dir("20261003T000000Z-1-0")
        self.assertIn("session_id: 20261003T000000Z-1-0", text)
        self.assertIn(f"path: {path}", text)
        self.assertTrue((path / session_plan.PLAN_NAME).is_file())
        listed = self.run_main("list", "--status", "open")
        self.assertIn(f"20261003T000000Z-1-0  {TITLE}", listed)

    def test_the_launcher_reaches_each_verbs_help(self) -> None:
        self.assertIn("one folder for the task you are about to do", run_help())
        for verb, phrase in (
            ("new", "--parent ID"),
            ("list", "--conversation ID"),
            ("close", "--session-id SESSION_ID"),
            ("gc", "--idle-days DAYS"),
            ("brief", "ID"),
        ):
            with self.subTest(verb=verb):
                self.assertIn(phrase, run_help(verb))


class StaleCopiesAreNotNew(Fixture):
    def test_new_runs_no_child_process_but_git(self) -> None:
        with unittest.mock.patch.object(subprocess, "run", wraps=subprocess.run) as run:
            self.run_main("new", "--session-id", "s-quiet", "--title", TITLE)
        for call in run.call_args_list:
            self.assertEqual(call.args[0][0], "git")


if __name__ == "__main__":
    unittest.main(verbosity=2)
