#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that each shared service fact has one home, across `.agents/scripts`.

    python .agents/scripts/services/tests/shared_types.py

The subject is the rule [A Fact in Code Is Written Once](../../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)
applied to the facts the services share: a session id, a project's name and its
path, a claim, a priority, a topic, and the keys of a plan's front matter. Each
is declared as a type in a file of its own, and a service or a help text that
needs the fact calls the type. This suite reads the scripts' source (never a
test file) and fails when a fact is spelled outside its home, which is how the
copy the rule forbids would show. Named for the concern per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes.

What is pinned, and what each pin is for:

  OneHome   For each fact a pattern that would spell it, and the one file
            allowed to: the bounds and the words of a priority, the form and
            clock format of a session id, the names and life of a claim, the
            two project flags and their attributes, the front-matter keys read
            as strings, and the dependency key and its inverse.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

# The scripts' own source: services, machine and the router, never a test and never host (host/
# wraps tools the machine has and imports nothing from services).
SHELVES = ("services", "machine")


def sources() -> dict[str, str]:
    found: dict[str, str] = {}
    for shelf in SHELVES:
        for path in sorted((SCRIPTS / shelf).glob("*.py")):
            found[f"{shelf}/{path.name}"] = path.read_bytes().decode("utf-8")
    found["memar"] = (SCRIPTS / "memar").read_bytes().decode("utf-8")
    return found


# (what the fact is, a pattern that spells it, the one file that may)
SPELLINGS = (
    ("a priority's bounds and default as names", r"\b(?:LOWEST|HIGHEST|DEFAULT)_PRIORITY\b", "services/priority.py"),
    ("a priority's range as words", r"\b1 to 10\b", "services/priority.py"),
    ("the form of a session id", r"\\d\{8\}-T", "services/session_id.py"),
    ("the clock format of a session id", r"%Y%m%d-T", "services/session_id.py"),
    ("a claim's file name as a name", r"\bCLAIM_(?:NAME|TAKEOVER_NAME|STALE_SECONDS)\b", "services/claim.py"),
    ("a claim's takeover guard", r"claim\.takeover", "services/claim.py"),
    ("the flag that carries a project's name", r"[\"']--project[\"']", "services/project_name.py"),
    ("the flag that carries a project's path", r"[\"']--project-path[\"']", "services/project_path.py"),
    ("the old flag names", r"\b(?:NAME|PATH)_FLAG\b", "services/none.py"),
    ("the attribute a parser gives the path flag", r"getattr\(args, [\"']project_path[\"']", "services/none.py"),
    ("a plan's key read as a string", r"\.get\(\"(?:title|project|parent|conversation|opened|priority|topic|kind|session)\"", "services/none.py"),
    ("the key of a plan's dependencies, as a string literal", r"[\"']depends_on[\"']", "services/session_record.py"),
    ("the written key of a plan's dependencies", r"[\"']Depends_on[\"']", "services/none.py"),
    ("the inverse of a plan's dependencies", r"[\"']Depends_for[\"']", "services/depends_on.py"),
    ("a plan's priority or topic helper by its old name", r"\b(?:priority_of|checked_priority|normalized_topic|checked_topic|topic_of|new_session_id|is_session_id)\b", "services/none.py"),
)


class OneHome(unittest.TestCase):
    def test_each_fact_is_spelled_only_in_its_home(self) -> None:
        files = sources()
        for fact, pattern, home in SPELLINGS:
            with self.subTest(fact=fact):
                regex = re.compile(pattern)
                outside = sorted(name for name, text in files.items() if name != home and regex.search(text))
                self.assertEqual(outside, [], f"{fact} is spelled outside {home}")

    def test_the_homes_exist_and_spell_what_they_own(self) -> None:
        files = sources()
        for fact, pattern, home in SPELLINGS:
            if home.endswith("none.py"):
                continue
            with self.subTest(fact=fact):
                self.assertIn(home, files)


if __name__ == "__main__":
    unittest.main(verbosity=2)
