#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/install_apps.py — the agent-app layer of `memar install`: the Memar skill copied into local AI agent apps.

Does not write AGENTS.md or `.agents/memar/` — that is `install_project` (the
https://agents.md/ project pointer).

The skill is copied from the Memar checkout that the location variable names,
which `machine/env_location.py` is the one module that reads. This layer never
copies the repository anywhere else. The skill carries no scripts: what it names
lives in the checkout, in `.agents/scripts/`, and is reached there rather than
copied here. If the variable names no repository this layer says so and points
at the install step; it does not clone the repository to find one.

`warn_stale` is how a copy that has fallen behind the checkout is noticed: a copy
is written once and the skill keeps changing, and an agent reading an old one
acts on rules that are gone. Which copies exist is decided here, what a copy
leaves out by `machine/fs_copy_excluded.py`, and whether one still matches by
`machine/fs_copy.py`. `memar update` asks it through `services/update_copies.py`
and relays its lines, one per stale copy and none when every copy matches, and
with `--apply` asks `into_apps` for the existing copies only, which rewrites only
the copies that differ. Its lines name `memar update --apply` rather than this
layer: a bare `memar install` would also write into the project the caller
stands in.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from machine.fs_copy_excluded import NEVER_COPIED
from machine.fs_copy import differs
from machine.env_location import resolve_root
from machine.fs_trash import soft_delete

APP_DIRS = {
    "agents": lambda: Path.home() / ".agents",
    "cursor": lambda: Path.home() / ".cursor",
    "claude": lambda: Path.home() / ".claude",
    "codex": lambda: Path.home() / ".codex",
    "opencode": lambda: Path.home() / ".config" / "opencode",
}


def skill_dest_for_app(app: str) -> Path:
    return APP_DIRS[app]() / "skills" / "memar"


def skill_destinations(*, existing_only: bool, app: str | None) -> list[Path]:
    if app is not None:
        app_dir = APP_DIRS[app]()
        dest = skill_dest_for_app(app)
        if existing_only:
            if not dest.is_dir():
                sys.exit(f"error: no existing Memar skill copy at {dest}")
            return [dest]
        if not app_dir.is_dir():
            sys.exit(
                f"error: {app} does not appear to be installed "
                f"({app_dir} is missing)"
            )
        return [dest]
    dests = [skill_dest_for_app("agents")]
    for name in ("cursor", "claude", "codex", "opencode"):
        app_dir = APP_DIRS[name]()
        if app_dir.is_dir():
            dests.append(skill_dest_for_app(name))
    if existing_only:
        dests = [d for d in dests if d.is_dir()]
    seen: set[Path] = set()
    unique: list[Path] = []
    for dest in dests:
        if dest in seen:
            continue
        seen.add(dest)
        unique.append(dest)
    return unique


def copy_skill(source: Path, dest: Path, *, dry_run: bool) -> None:
    if dry_run:
        print(f"dry-run: copy {source} -> {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        # An earlier copy may hold a local edit. Move it to the trash, so the
        # edit can be taken back, then write the checkout's skill.
        soft_delete(dest)
    shutil.copytree(source, dest, ignore=NEVER_COPIED)
    print(f"copied skill -> {dest}")


def stale_copies(source: Path) -> list[Path]:
    """The skill copies already in agent apps that differ from SOURCE; none when SOURCE is absent."""
    stale: list[Path] = []
    if not source.is_dir():
        return stale
    for dest in skill_destinations(existing_only=True, app=None):
        try:
            if differs(source, dest, NEVER_COPIED):
                stale.append(dest)
        except OSError:
            stale.append(dest)
    return stale


# The one command that refreshes what Memar installed; a stale line names it.
REFRESH = "memar update --apply"


def checkout_skill() -> Path:
    """The skill in the checkout the location variable names.

    Asked of the module that owns the variable and refuses to guess when it
    names no repository, because a session that quietly put a checkout on the
    machine would produce a location nothing else agrees on.
    """
    return resolve_root() / ".agents" / "skills" / "memar"


def warn_stale(source: Path) -> None:
    """One line per stale copy, naming the command that refreshes them."""
    for dest in stale_copies(source):
        print(f"stale: the Memar skill at {dest} differs from the checkout's; refresh with: {REFRESH}")


def into_apps(*, dry_run: bool = False, app: str | None = None, existing_only: bool = False) -> None:
    """Copy the checkout's skill into every agent app found, or into APP only; with EXISTING_ONLY refresh the copies that differ."""
    dests = skill_destinations(existing_only=existing_only, app=app)
    if existing_only and not dests:
        sys.exit("error: no existing Memar skill copies found to update")
    source = checkout_skill()
    print(f"Memar resolves to {source.parents[2]}")
    for dest in dests:
        try:
            current = existing_only and not differs(source, dest, NEVER_COPIED)
        except OSError:
            current = False
        if current:
            print(f"already current: {dest}")
            continue
        copy_skill(source, dest, dry_run=dry_run)

