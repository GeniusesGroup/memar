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

  HelpSaysWhatToRun  Each help states its own work only (owner, 2026-10-14).
                     `memar session --help` states the domain's: what a task
                     and a session are, that the folder's top holds only
                     plan.md and report.md (and Memar's claim) and the rest
                     goes in role folders by kind, whose names it leaves to
                     `memar module folders --help`, the Status words and that
                     a session ends when its report and plan state the same
                     one, who writes into another session's folder, that each
                     location keeps its own log, and the move its own run
                     makes before every verb; and none of a sub-verb's command
                     lines, files, or recipes. No sub-verb sends its reader
                     back there for its own work. `new` says what it writes
                     (the plan's outline, the report's skeleton, the short
                     hand-back), where the folder lies, how a task is handed
                     to a sub-agent, queued, or continued; `claims` carries
                     the whole recipe for an agent told only to "do some of
                     the queued tasks" — the project always named, one fresh
                     sub-agent per batch of one topic, each report read, one
                     `digest --conversation` at the end; `digest` the owner's
                     review and what a hand-back is; `close` when it may be
                     run; and each verb's own help what it accepts. No
                     external runner is named, and `memar --help`'s line for
                     `session` names queued tasks, so an agent starting from
                     the top reaches `claims`.
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
  NoOneTimeMigration No file of the scripts folder outside the test suites
                     names a one-time migration script, and none is one of
                     them: such a script lives in the session that does the
                     change (.agents/scripts/README.md).

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import os
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
import services.session_archive as session_archive
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
import services.session_topic as session_topic
import services.session_topics as session_topics
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
    # The scripts' own shelf, not the services/ role folder a session's script goes in.
    MECHANISM = ("shared-tree collisions", "advisory locks", "intent notes", "OS-temp", "fails closed", "scripts/services/")

    # The owner's ruling (2026-10-14): each command's help states only its own
    # work; a sub-verb's is reached through that sub-verb's own --help, which
    # argparse's verb list under the domain's help leads to.

    def test_the_domain_help_says_what_a_task_and_a_session_are(self) -> None:
        text = flat(run_help())
        for phrase in (
            "A task is one thing the person asked for",
            "A session is the record of one task",
            "One session is one task",
            "gets a session of its own",
            "Agent, sub-agent, and conversation are defined in `memar --help`",
            "Work inside the session's folder, not in the checkout",
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_the_top_holds_only_the_plan_and_the_report_and_where_the_rest_goes(self) -> None:
        text = flat(run_help())
        for phrase in (
            "The folder's top holds only plan.md and report.md",
            "the `claim` file Memar writes there",
            "Put nothing else at the top",
            "a note (.md) in docs/, a script (.py, .mjs, .js, .ps1, .sh) in services/",
            "a test in tests/",
            "`memar module folders --help` names the role folders",
            "a file of another kind goes in the role folder that holds it",
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_gives_the_status_words_and_how_a_session_ends(self) -> None:
        text = run_help()
        for phrase in (
            "Queued     Waiting to be taken up",
            "Active     Being worked on",
            "Status: Complete   the check passed",
            "Status: Blocked    it waits on an answer or an approval",
            "Status: Active     its budget ended",
        ):
            self.assertIn(phrase, text)
        text = flat(text)
        for phrase in (
            "Queued, Active, Blocked, or Complete",
            "finished or not",
            "its report.md states a Status and its plan.md states the same",
            "Complete once its check has passed",
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_who_writes_into_another_sessions_folder_and_where_each_log_is(self) -> None:
        text = flat(run_help())
        for phrase in (
            "Write only inside your own folder",
            "Two writes reach another session's folder, both from the session it came from",
            "writes the report.md of a sub-agent that could only return text, and sets that plan.md's Status",
            "keeps its own log of what was done to its folders, sessions.log at its top",
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_a_commit_of_a_task_carries_its_sessions_records(self) -> None:
        # The owner's ruling (2026-10-14): a commit of a task's changes adds
        # the records of its sessions, kept in the project, not the folders.
        text = flat(run_help())
        for phrase in (
            "A session's records — its plan.md, its report.md, and each file in its folder its report links to",
            "are kept in .agents/sessions/<id>/ in its project",
            "Committing a task's changes commits the records of its sessions with them",
            "its own and those of the sessions it handed work to",
            "unless its preferences say `records: off`",
        ):
            self.assertIn(phrase, text)

    def test_the_domain_help_says_what_its_own_run_does_before_every_verb(self) -> None:
        text = flat(run_help())
        for phrase in ("Before any verb below runs", "an earlier Memar left directly in temp/", "asking for help moves nothing"):
            self.assertIn(phrase, text)

    def test_the_domain_help_states_no_sub_verbs_work(self) -> None:
        # Each phrase is a sub-verb's: its command line, what it writes, or its recipe.
        text = flat(run_help())
        for phrase in (
            "memar session new",
            "memar session claims",
            "memar session digest",
            "Title: TITLE",
            "## Request",
            "## What ran",
            "do some of the queued tasks",
            "review today's sessions",
            "Once a day",
            "To only add work",
        ):
            self.assertNotIn(phrase, text)

    def test_no_sub_verb_sends_its_reader_to_the_domain_help_for_its_own_work(self) -> None:
        for verb in ("new", "list", "brief", "gc", "close", "archive", "claim", "claims", "priority", "topic", "topics", "digest"):
            with self.subTest(verb=verb):
                text = flat(run_help(verb)).lower()
                self.assertNotIn("when to use", text)
                self.assertNotIn("what to do with each is said", text)
                self.assertNotIn("what a report's decisions are is said", text)

    def test_new_says_what_it_writes_and_where_the_folder_lies(self) -> None:
        text = run_help("new")
        self.assertIn("---\n    Title: TITLE\n    Status:\n    ---\n    # Report\n\n    ## What ran\n    ## Check\n    ## Result\n    ## Left open", text)
        text = flat(text)
        for phrase in (
            "Title: TITLE",
            "Opened:",
            "Project:",
            "Parent: ID of the session this one came from",
            "Conversation: the id of the first session",
            "Status: where the task stands",
            "## Request",
            "## Why",
            "in its own words, from the person's request",
            "## Steps",
            "## Next",
            "written in PascalCase",
            "rewrite it in the shape above",
            "never overwrites one that is there",
            "Left open names each entry the task wrote in a handoff",
            "at most 10 lines under a `## Decisions needed` heading",
            "each the question, its options, and the one it recommends",
            "under temp/sessions/",
            "sets `sessions` in its .agents/memar/preferences.md",
            "says on a line of its own",
            "relative to the project's top folder, or an absolute one",
            "drive or filesystem root is refused",
            "inside Memar's own temp/ is not used",
            "use it as printed",
            "`memar content write`",
            "Once a day",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("lies in Memar's own checkout, also when", text)

    def test_new_says_how_a_task_is_handed_over_queued_and_continued(self) -> None:
        text = flat(run_help("new"))
        for phrase in (
            "open its session yourself with `--parent`",
            "write the whole task into its plan.md — the Request, the check that says it is done, the shape of its report, and its Why, in your own words from the person's request",
            "hand the sub-agent only the brief `new` prints, which `memar session brief ID` prints again",
            "takes that session up and opens none, and does not rewrite its Request",
            "To only add work",
            "--queued",
            "--session-id ID --queued",
            "a queued plan whose Request is empty is not taken",
            "never do a queued session's work in your own context",
            "To continue a task another session left",
            "`memar session list`",
            "start from its Next",
        ):
            self.assertIn(phrase, text)

    def test_new_does_not_repeat_what_the_domain_states(self) -> None:
        text = run_help("new")
        for phrase in ("Status: Blocked    it waits", "Queued     Waiting to be taken up", "Put nothing else at the top"):
            self.assertNotIn(phrase, text)

    def test_claims_carries_the_recipe_for_an_agent_told_only_to_do_queued_tasks(self) -> None:
        # The owner's prompt is one line — "do some of the queued Memar tasks",
        # "do 5 tasks of project X" — so `claims`, which `memar session --help`
        # lists as the verb that takes queued tasks, carries the whole recipe.
        text = flat(run_help("claims"))
        for phrase in (
            "do some of the queued tasks",
            "--project NAME or --project-path PATH is required: one run serves one project",
            "\"Do 5 tasks of X\" means `claims 5 --project X`",
            "there is no default project and no way to take from all",
            "ask the owner rather than guess",
            "`memar session list --status queued`",
            "N is yours to choose",
            "the highest priority first, the oldest opened first among equals",
            "Hand the batch of one topic to one fresh sub-agent",
            "each session keeping its own plan.md and report.md",
            "never one sub-agent for sessions of different topics",
            "never in your own context",
            "read its report.md: its Status and its Decisions needed",
            "a Status that disagrees with its plan",
            "failed hand-back",
            "run `memar session digest --conversation ID`, ID your own session's",
            "give the owner that one digest",
            "Memar starts no agent",
        ):
            self.assertIn(phrase, text)

    def test_the_review_and_the_hand_back_are_digests(self) -> None:
        text = flat(run_help("digest"))
        for phrase in (
            "review today's sessions with me and close the ones I confirm",
            "`memar session close --session-id ID`",
            "at most 10 lines",
            "each the question, its options, and the one it recommends",
            "a complete session is in only when it has entries or a failed hand-back",
            "blocking first",
            "a pointer to a handoff or line that holds no open question is a failed hand-back",
        ):
            self.assertIn(phrase, text)

    def test_close_says_when_it_may_be_run(self) -> None:
        text = flat(run_help("close"))
        for phrase in (
            "recycle bin",
            "the person who started the session has already said the work is finished",
            "never ask them to, and never close a session you did not open",
            "You do not have to close a session",
        ):
            self.assertIn(phrase, text)

    def test_no_external_runner_is_left_in_the_help(self) -> None:
        texts = [run_help(), *(run_help(verb) for verb in ("new", "claim", "claims", "digest", "priority"))]
        for text in texts:
            for word in ("launch", "runner", "`run`", "session run"):
                self.assertNotIn(word, text)

    def test_the_top_help_leads_to_queued_tasks(self) -> None:
        self.assertIn("queued tasks", session.SUMMARY)

    def test_each_verbs_help_says_what_it_accepts(self) -> None:
        for verb, phrases in (
            ("new", ("--session-id", "--title TITLE", "--parent ID", "--project NAME", "--project-path PATH", "never read", "for one task", "first session of that conversation")),
            ("list", ("whose id, title, or project holds TEXT", "one word or a short phrase, not a question",
                      "--status {queued,active,blocked,complete}", "--conversation ID", "--idle-days DAYS",
                      "--project NAME", "--project-path PATH", "List Memar's own session folders", "the calling folder is never read",
                      "earlier shape", "where today's shape is shown")),
            ("brief", ("ID", "ready to paste", "`new --parent` prints")),
            ("gc", ("--session-id", "--idle-days DAYS", "never swept", "cannot be read", "at least 1", "whose status is complete",
                    "once a day", f"{session_gc.SESSION_IDLE_DAYS} unless given")),
            ("close", ("--session-id", "--without-records", "which loses them", "the folder holding them is printed",
                       "is not closed")),
            ("archive", ("--session-id", "every session whose Parent chain leads to it", "relative link",
                         "registered name, not by its path", "the claim is not copied", "name those folders in the commit",
                         "`records: off`", "the verb fails")),
            ("new", ("--queued", "an existing active one no one has claimed is queued", "--priority N", "1 to 10",
                     "higher goes sooner")),
            ("claim", ("ID", "another agent holds, is refused", "taken over", "Nothing keeps a claim fresh",
                       f"{session_claim.CLAIM_STALE_SECONDS // 3600} hours")),
            ("claims", ("N", "highest priority first", "oldest", "brief", "Fewer queued than N is not an error", "no default",
                        "never mixes two projects'", "one fresh sub-agent per batch of one topic", "--topic T", "--fill")),
            ("priority", ("ID", "N", "1 to 10", "5 when", "higher goes sooner", "Anyone, a person or an agent, may change it")),
            ("topic", ("ID", "T", "tasks that share a topic are taken together", "a task with no topic is taken by priority and age alone",
                       "`memar session topics`")),
            ("digest", ("--conversation ID", "Decisions needed", "priority", "failed hand-back",
                        "entries or not", "Queued sessions are left out", "With --day: the review", "The review closes nothing itself")),
        ):
            with self.subTest(verb=verb):
                text = flat(run_help(verb))
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_the_help_does_not_carry_the_implementation(self) -> None:
        text = run_help()
        for phrase in self.MECHANISM:
            self.assertNotIn(phrase, text)

    def test_the_why_is_in_the_files_the_implementer_reads(self) -> None:
        # Not a second copy: each service's own docstring, the one text
        # addressed to whoever opens it, and the domain's says where they are.
        for name in ("session_new", "session_brief", "session_find", "session_close", "session_gc", "session_archive", "session_migrate"):
            self.assertIn(name, session.__doc__)
        for module, phrases in (
            (session_new, ("shared-tree collisions", "advisory locks", "intent notes", "One session is one task")),
            (session_brief, ("same text for every task", "stated once in the delegator's words")),
            (session_plan, ("disputed", "handoff", "Only that shape is read")),
            (session_gc, ("Idle is not the same as", "once a day")),
            (session_find, ("listed together",)),
        ):
            for phrase in phrases:
                self.assertIn(phrase, flat(module.__doc__), module.__name__)


class NoOneTimeMigration(unittest.TestCase):
    # A one-time migration lives in the session that does the change, never in
    # this folder (.agents/scripts/README.md, owner 2026-10-14), so nothing here
    # names one: these three were such scripts, and lie in their sessions now.
    MIGRATION_SCRIPTS = ("session-convert", "session-strays", "session-rename", "CONVERT_SCRIPT")

    def test_no_file_of_the_scripts_folder_names_a_one_time_migration(self) -> None:
        files = [path for path in SCRIPTS.rglob("*.py") if "tests" not in path.relative_to(SCRIPTS).parts]
        files.append(LAUNCHER)
        for path in files:
            text = path.read_text(encoding="utf-8")
            for name in self.MIGRATION_SCRIPTS:
                with self.subTest(path=path.relative_to(SCRIPTS).as_posix(), name=name):
                    self.assertNotIn(name, text)
            with self.subTest(path=path.relative_to(SCRIPTS).as_posix()):
                self.assertFalse(path.name in {f"{name}.py" for name in self.MIGRATION_SCRIPTS})


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
            (session_archive, ["archive"]),
            (session_close, ["close"]),
            (session_gc, ["gc"]),
            (session_claim, ["claim"]),
            (session_claims, ["claims"]),
            (session_priority, ["priority"]),
            (session_topic, ["topic"]),
            (session_topics, ["topics"]),
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

    def test_the_command_offers_the_twelve_verbs_in_the_order_of_their_services(self) -> None:
        def verbs_of(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
            found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            return dict(found[0].choices) if found else {}

        top, before = launcher.assemble(SESSION_SERVICES)
        self.assertEqual(before, [])
        self.assertEqual(
            list(verbs_of(verbs_of(top)["session"])),
            ["archive", "brief", "claim", "claims", "close", "digest", "list", "gc", "new", "priority", "topic", "topics"],
        )


class VerbsDispatch(Fixture):
    def test_each_verb_reaches_its_service_with_the_parsed_arguments(self) -> None:
        for argv, module, name, expected in (
            (["new", "--title", "T"], session_new, "open_session", (None, "T", None)),
            (["new", "--session-id", "s-1", "--parent", "s-0"], session_new, "open_session", ("s-1", None, "s-0")),
            (["list"], session_find, "list_sessions", (None, None, None, None, None)),
            (["list", "word", "--status", "blocked", "--idle-days", "3", "--conversation", "s-0"],
             session_find, "list_sessions", ("word", "blocked", 3.0, "s-0", None)),
            (["list", "--project-path", "<F>"], session_find, "list_sessions", (None, None, None, None, "<F>")),
            (["list", "--project", "p"], session_find, "list_sessions", (None, None, None, None, "<F>")),
            (["brief", "s-1"], session_brief, "print_brief", ("s-1",)),
            (["gc"], session_gc, "collect", (None, None)),
            (["gc", "--session-id", "s-1", "--idle-days", "2"], session_gc, "collect", ("s-1", 2.0)),
            (["close", "--session-id", "s-1"], session_close, "close", ("s-1", False)),
            (["close", "--session-id", "s-1", "--without-records"], session_close, "close", ("s-1", True)),
            (["archive", "--session-id", "s-1"], session_archive, "archive", ("s-1",)),
            (["new", "--title", "T", "--queued"], session_new, "open_session", (None, "T", None, True, None)),
            (["new", "--title", "T", "--queued", "--priority", "8"], session_new, "open_session",
             (None, "T", None, True, 8)),
            (["list", "--status", "queued"], session_find, "list_sessions", (None, "queued", None, None, None)),
            (["claim", "s-1"], session_claim, "claim", ("s-1",)),
            (["claims", "5"], session_claims, "claims", (5, None)),
            (["claims", "2", "--project-path", "<F>"], session_claims, "claims", (2, "<F>")),
            (["priority", "s-1", "8"], session_priority, "set_session_priority", ("s-1", "8")),
            (["new", "--title", "T", "--topic", "docs"], session_new, "open_session", (None, "T", None, False, None, "docs")),
            (["claims", "5", "--project", "p", "--topic", "docs"], session_claims, "claims", (5, "<F>", "docs", False)),
            (["claims", "5", "--project", "p", "--fill"], session_claims, "claims", (5, "<F>", None, True)),
            (["topic", "s-1", "docs"], session_topic, "set_session_topic", ("s-1", "docs")),
            (["topic", "s-1", ""], session_topic, "set_session_topic", ("s-1", "")),
            (["topics"], session_topics, "list_topics", (None,)),
            (["topics", "--project-path", "<F>"], session_topics, "list_topics", ("<F>",)),
            (["digest"], session_digest, "print_digest", (None, None, None)),
            (["digest", "--conversation", "s-0"], session_digest, "print_digest", ("s-0", None, None)),
        ):
            # "<F>" is the project's folder: given as it is by --project-path, and
            # what the registry answers for the name given by --project.
            folder = self.fake_root / "p"
            folder.mkdir(exist_ok=True)
            argv = [str(folder) if word == "<F>" else word for word in argv]
            expected = tuple(folder.resolve() if value == "<F>" else value for value in expected)
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service, \
                        unittest.mock.patch("services.project_find.resolve_project", return_value=folder.resolve()):
                    self.assertEqual(command(*argv), 0)
                service.assert_called_once_with(*expected)

    def test_new_passes_its_project_as_a_folder_and_without_one_passes_none(self) -> None:
        folder = self.fake_root / "docs"
        folder.mkdir()
        with unittest.mock.patch.object(session_new, "open_session") as service:
            self.assertEqual(command("new", "--title", "T", "--project-path", str(folder)), 0)
        service.assert_called_once_with(None, "T", None, project=folder.resolve())
        with unittest.mock.patch.object(session_new, "open_session") as service, \
                unittest.mock.patch("services.project_find.resolve_project", return_value=folder.resolve()):
            self.assertEqual(command("new", "--title", "T", "--project", "docs"), 0)
        service.assert_called_once_with(None, "T", None, project=folder.resolve())
        with unittest.mock.patch.object(session_new, "open_session") as service, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                command("new", "--title", "T", "--project")
        service.assert_not_called()

    def test_every_verb_that_takes_a_project_takes_one_flag_per_kind_and_never_both(self) -> None:
        for argv, module, name in (
            (["new", "--title", "T"], session_new, "open_session"),
            (["list"], session_find, "list_sessions"),
            (["claims", "5"], session_claims, "claims"),
            (["topics"], session_topics, "list_topics"),
            (["digest"], session_digest, "print_digest"),
        ):
            with self.subTest(verb=argv[0]):
                folder = str(self.fake_root)
                with unittest.mock.patch.object(module, name) as service, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv, "--project", "p", "--project-path", folder)
                    with self.assertRaises(SystemExit):
                        command(*argv, "--project", folder)
                    with self.assertRaises(SystemExit):
                        command(*argv, "--project-path", "p-is-a-name")
                service.assert_not_called()

    def test_project_always_takes_a_value_and_no_service_runs_without_one(self) -> None:
        for argv, module, name in (
            (["list", "word", "--project"], session_find, "list_sessions"),
            (["list", "word", "--project-path"], session_find, "list_sessions"),
            (["claims", "5", "--project"], session_claims, "claims"),
            (["topics", "--project"], session_topics, "list_topics"),
            (["digest", "--day", "today", "--project"], session_digest, "print_digest"),
        ):
            with self.subTest(argv=argv):
                with unittest.mock.patch.object(module, name) as service, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        command(*argv)
                service.assert_not_called()

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
        text = self.run_main("new", "--session-id", "20261003T000000Z-1-0", "--title", TITLE, "--project-path", str(self.fake_root))
        path = memar_fs.session_dir("20261003T000000Z-1-0")
        self.assertIn("session_id: 20261003T000000Z-1-0", text)
        self.assertIn(f"path: {path}", text)
        self.assertTrue((path / session_plan.PLAN_NAME).is_file())
        listed = self.run_main("list", "--status", "active")
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
            self.run_main("new", "--session-id", "s-quiet", "--title", TITLE, "--project-path", str(self.fake_root))
        for call in run.call_args_list:
            self.assertEqual(call.args[0][0], "git")


if __name__ == "__main__":
    unittest.main(verbosity=2)
