#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a session's identity in `services/session_id.py`.

    python .agents/scripts/services/tests/session_id.py

The subject is the id a session's folder and intent notes carry, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes anything: an id is minted and read back.

What is pinned, and what each pin is for:

  MintedIdUnique     Two ids minted by one process differ, also within one
                     second, so two sessions opening a shared scratch root
                     cannot land on one folder; the form is the date, a dash,
                     the time, and the process id, so a person reads it and a
                     name sort is creation order; only that form is a session
                     id, so a person's folder named by a date is not one, and
                     neither is a name in a form minted before (a folder so
                     named is a session by its plan, `session_folder`, as
                     long as it keeps that name).

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import os
import sys
import time
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import services.session_id as session_id


class MintedIdUnique(unittest.TestCase):
    """The id a session gets when it does not bring one.

    Minting happens in a module of its own rather than in the session command,
    so a caller that needs an id without running a session can have one; what
    makes it an identity rather than a label is that no two calls agree, which is
    the one property a shared scratch root depends on.
    """

    def test_two_minted_ids_differ_even_within_one_second(self) -> None:
        first, second = session_id.SessionId.new(), session_id.SessionId.new()
        self.assertNotEqual(first, second)
        self.assertTrue(session_id.SessionId.is_form(first) and session_id.SessionId.is_form(second))

    def test_the_form_is_the_date_a_dash_the_time_and_the_process_id(self) -> None:
        minted = session_id.SessionId.new()
        self.assertRegex(minted, r"^\d{8}-T\d{6}Z-\d+$")
        self.assertTrue(minted.startswith(time.strftime("%Y%m%d-T", time.gmtime())))
        self.assertTrue(minted.endswith(f"-{os.getpid()}"))

    def test_a_name_sort_is_creation_order(self) -> None:
        # The clock leads, so any file listing sorted by name lists sessions in
        # the order they were opened, and the date is readable off the name.
        self.assertLess("20261008-T082722Z-99999", "20261008-T082723Z-1")
        self.assertLess("20261008-T235959Z-1", "20261009-T000000Z-1")

    def test_only_the_minted_form_is_a_session_id(self) -> None:
        for name in ("20261013-T190845Z-23368", "20261010-T054304Z-1"):
            with self.subTest(name=name):
                self.assertTrue(session_id.SessionId.is_form(name))
        for name in (
            "20261013T190845Z-23368-0",
            "34852-18dc8080b906c944-0",
            "2024-01-01",
            "20261013-T190845Z-",
            "20261013-T190845Z-23368-0",
            "repo_tree.md",
        ):
            with self.subTest(name=name):
                self.assertFalse(session_id.SessionId.is_form(name))


if __name__ == "__main__":
    unittest.main(verbosity=2)
