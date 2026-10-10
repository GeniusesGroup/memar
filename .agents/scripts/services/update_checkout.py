#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/update_checkout.py — how far a Memar checkout is behind its upstream, and bringing it up to date.

A checkout is obtained by the bootstrap, which is a shell and cannot be asked,
so whether a checkout has fallen behind the branch it tracks is answered here,
for the update and for the installer that marks a checkout as a developer's,
and so is the one act that brings it up to date. What a Memar repository is
belongs to `machine/fs_memar_repository.py`, which everything below the update
asks as well.

Most checkouts belong to people who use Memar and never change it; a few are
where Memar is developed, and an update that moved one of those under its
developer would be the worst thing an update could do. So `fast_forward` moves
a checkout only when nothing in it can be anyone's work: it is not marked as a
development checkout, its working tree is clean, its branch tracks an upstream,
and it is behind that upstream and not ahead of it. Anything else is reported
and left — a detached HEAD, no upstream, uncommitted changes, or unpushed
commits each make a checkout a development checkout whether or not it is
marked. The move is a fast-forward and nothing else: no merge commit, no
rebase, no reset.

The mark is `memar.development` in the checkout's own git configuration, and
`mark_development` is the one write of it. It is the checkout's and not the
machine's: the location variable says where Memar is, and a second checkout,
or the variable pointed elsewhere, must neither inherit nor lose the mark. The
git configuration of a clone travels with nothing, is never tracked, never
shows in `git status`, and survives a cleared `temp/`.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import NamedTuple

# A fetch that has not answered by then is a network that is not there; the
# comparison goes on against what was fetched last.
FETCH_SECONDS = 20
DEVELOPMENT_KEY = "memar.development"


class Upstream(NamedTuple):
    """Where a checkout stands against the branch it tracks.

    `branch` is None when nothing is tracked — a detached HEAD, no upstream, or
    no git — and then `ahead` and `behind` mean nothing; `unfetched` says why a
    fetch was skipped or failed, so the counts are as of the last fetch.
    """

    branch: str | None
    ahead: int
    behind: int
    unfetched: str | None


def _git(checkout: Path, *arguments: str, timeout: float | None = None) -> subprocess.CompletedProcess[str]:
    # Never a prompt: a caller running unattended has nobody to answer one.
    environment = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    return subprocess.run(
        ["git", "-C", str(checkout), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        timeout=timeout,
    )


def upstream_of(checkout: Path, *, fetch: bool) -> Upstream:
    """How far CHECKOUT is ahead of and behind its upstream, fetching first when FETCH."""
    try:
        tracked = _git(checkout, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    except OSError:
        return Upstream(None, 0, 0, "git is not on this machine")
    branch = tracked.stdout.strip()
    if tracked.returncode != 0 or not branch:
        return Upstream(None, 0, 0, None)
    unfetched = None if fetch else "not fetched, as asked"
    if fetch:
        current = _git(checkout, "branch", "--show-current").stdout.strip()
        remote = _git(checkout, "config", f"branch.{current}.remote").stdout.strip() or "origin"
        try:
            fetched = _git(checkout, "fetch", "--quiet", remote, timeout=FETCH_SECONDS)
        except subprocess.TimeoutExpired:
            unfetched = f"the fetch did not answer within {FETCH_SECONDS} seconds"
        else:
            if fetched.returncode != 0:
                said = fetched.stderr.strip().splitlines()
                unfetched = f"the fetch failed: {said[-1] if said else 'git gave no reason'}"
    counted = _git(checkout, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    try:
        ahead, behind = (int(part) for part in counted.stdout.split())
    except ValueError:
        return Upstream(None, 0, 0, unfetched)
    return Upstream(branch, ahead, behind, unfetched)


def is_marked_development(checkout: Path) -> bool:
    """Whether CHECKOUT's own git configuration marks it as a development checkout."""
    try:
        said = _git(checkout, "config", "--get", "--bool", DEVELOPMENT_KEY)
    except OSError:
        return False
    return said.stdout.strip() == "true"


def mark_development(checkout: Path) -> None:
    """Mark CHECKOUT as a development checkout, so no update ever moves it."""
    done = _git(checkout, "config", "--bool", DEVELOPMENT_KEY, "true")
    if done.returncode != 0:
        said = done.stderr.strip().splitlines()
        raise RuntimeError(said[-1] if said else f"git config exited {done.returncode}")


def development_reasons(checkout: Path, standing: Upstream) -> list[str]:
    """Each reason CHECKOUT is a development checkout, which no update moves; empty for a consumer's."""
    reasons = []
    if is_marked_development(checkout):
        reasons.append("it is marked as a development checkout")
    if not _git(checkout, "branch", "--show-current").stdout.strip():
        reasons.append("its HEAD is detached")
    elif standing.branch is None:
        reasons.append("its branch tracks no upstream")
    status = _git(checkout, "status", "--porcelain")
    if status.returncode != 0:
        reasons.append("its working tree could not be read")
    elif status.stdout.strip():
        reasons.append("it has uncommitted changes")
    if standing.ahead:
        reasons.append(f"it has {standing.ahead} unpushed commit(s)")
    return reasons


class Forwarded(NamedTuple):
    """What `fast_forward` did: the standing it acted on, the commits it moved, and why it would not."""

    standing: Upstream
    moved: int
    refused: list[str]


def fast_forward(checkout: Path, *, fetch: bool) -> Forwarded:
    """Bring a consumer's CHECKOUT up to its upstream by a fast-forward; leave any other as it is."""
    standing = upstream_of(checkout, fetch=fetch)
    try:
        refused = development_reasons(checkout, standing)
    except OSError:
        return Forwarded(standing, 0, ["git is not on this machine"])
    if refused or not standing.behind:
        return Forwarded(standing, 0, refused)
    merged = _git(checkout, "merge", "--ff-only", "--quiet", "@{upstream}")
    if merged.returncode != 0:
        said = merged.stderr.strip().splitlines()
        return Forwarded(standing, 0, [f"git refused the fast-forward: {said[-1] if said else merged.returncode}"])
    return Forwarded(standing, standing.behind, [])
