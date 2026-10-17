#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/claim.py — the claim an agent leaves in a session's folder while it holds the task, declared once.

A claim is a file, created with exclusive create so that exactly one of two
agents taking one session wins (`session_claim` does the taking). What the
claim is — the file's name, the name of the guard held while a stale claim is
replaced, how long a claim lives, and what the file says — is the type's, and
every service that takes, keeps, lays out or describes a claim calls it
([A Fact in Code Is Written Once](../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)).

Why a claim lapses. Nothing keeps a claim fresh: no process of Memar's watches
the sub-agent, so a claim's age is only the time since it was taken. A dead
agent's claim must still lapse, or its session is held forever; but the lapse
must not take a session from a sub-agent still at work, and one evening's
batch of sessions, handed out one after another, can run through the night.
A day outlasts that batch.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass(frozen=True)
class Claim:
    """The claim of one session FOLDER: where it is, and whether it still holds."""

    folder: Path

    NAME: ClassVar[str] = "claim"
    # Held only while a stale claim is replaced.
    TAKEOVER_NAME: ClassVar[str] = f"{NAME}.takeover"
    NAMES: ClassVar[tuple[str, str]] = (NAME, TAKEOVER_NAME)
    # A claim this old is a dead agent's.
    STALE_SECONDS: ClassVar[int] = 24 * 60 * 60

    @property
    def path(self) -> Path:
        """The claim file in the folder."""
        return self.folder / self.NAME

    @property
    def takeover_path(self) -> Path:
        """The guard held while a stale claim is replaced."""
        return self.folder / self.TAKEOVER_NAME

    def exists(self) -> bool:
        """Whether the folder holds a claim file, fresh or stale."""
        return self.path.exists()

    def is_fresh(self) -> bool:
        """Whether the folder holds a claim that has not gone stale."""
        try:
            touched = self.path.stat().st_mtime
        except OSError:
            return False
        return time.time() - touched < self.STALE_SECONDS

    @classmethod
    def stale_hours(cls) -> int:
        """How long a claim lives, in whole hours, as a help says it."""
        return cls.STALE_SECONDS // 3600

    @staticmethod
    def body(stamp: str, host: str, pid: int) -> str:
        """What the claim file says: when it was taken, by which host and process."""
        return f"claimed: {stamp}\nhost: {host}\npid: {pid}\n"
