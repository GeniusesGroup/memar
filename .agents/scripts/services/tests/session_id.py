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

  MintedIdUnique     Two ids minted without a session differ, so two sessions
                     opening a shared scratch root cannot land on one folder;
                     the clock leads, so a name sort is creation order; a
                     folder named in the earlier form is still a session, and
                     a person's folder named by a date is not one.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

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

    def test_two_minted_ids_differ(self) -> None:
        self.assertNotEqual(session_id.new_session_id(), session_id.new_session_id())

    def test_a_name_sort_is_creation_order(self) -> None:
        # The clock leads, so any file listing sorted by name lists sessions in
        # the order they were opened, and the date is readable off the name.
        minted = session_id.new_session_id()
        self.assertRegex(minted, r"^\d{8}T\d{6}Z-")
        self.assertTrue(minted.startswith(time.strftime("%Y%m%d", time.gmtime())))
        self.assertLess("20261008T082722Z-99999-0", "20261008T082723Z-1-0")
        self.assertTrue(session_id.is_session_id(minted))
        self.assertTrue(session_id.is_dated_session_id(minted))

    def test_a_folder_named_in_the_earlier_form_is_still_a_session(self) -> None:
        # Folders opened before the clock came first must still be reaped.
        self.assertTrue(session_id.is_session_id("34852-18dc8080b906c944-0"))
        self.assertFalse(session_id.is_dated_session_id("34852-18dc8080b906c944-0"))
        self.assertFalse(session_id.is_session_id("repo_tree.md"))

    def test_every_form_ever_minted_is_a_session_and_a_dated_folder_is_not(self) -> None:
        # The earlier form wrote its counter in hex, so a process that minted
        # ten ids ended in `a`; a person's folder named by a date is no session.
        earlier = f"{1234}-{1_728_000_000_000_000_000:x}-{10:x}"
        for name in ("20261010T054304Z-15624-0", "20261010T054304Z-15624-1f", "13356-18dc21f975d06e54-0", earlier):
            with self.subTest(name=name):
                self.assertTrue(session_id.is_session_id(name))
        for name in ("2024-01-01", "2024-01-01-1", "1-abc-0", "12-18dc21f975d06e5-0", "12-18dc21f975d06e54-"):
            with self.subTest(name=name):
                self.assertFalse(session_id.is_session_id(name))


if __name__ == "__main__":
    unittest.main(verbosity=2)
