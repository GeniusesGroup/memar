#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/install_apps.py — the agent-app layer of `memar install`: a pointer to the Memar skill written into local AI agent apps.

Does not write AGENTS.md or `.agents/memar/` — that is `install_project` (the
https://agents.md/ project pointer).

An agent app does not get a copy of the skill. A copy goes stale the moment the
checkout's skill changes, and an agent reading an old one acts on rules that are
gone. What the app gets is one file, `SKILL.md`, that an app finds the skill by
— the frontmatter `name` and `description` — and whose body sends the agent to
the checkout's skill through `memar content path`. The description is taken from
the checkout's skill each time the pointer is made, so the two cannot say
different things; the body names no rule, so it cannot fall behind one. Where
`memar` is not on PATH the pointer says so with the bootstrap commands
`install_project` publishes, imported from it so both name the same branch.

The checkout is the one the location variable names, which
`machine/env_location.py` is the one module that reads. This layer never copies
the repository anywhere. If the variable names no repository this layer says so
and points at the install step; it does not clone the repository to find one.

`warn_stale` is how a pointer that is not what the checkout would now write is
noticed: a description changed in the checkout, or a full copy of the skill left
by an earlier install. `memar update` asks it through `services/update_copies.py`
and relays its lines, one per stale pointer and none when every one matches, and
with `--apply` asks `into_apps` for the existing ones only, which rewrites only
those that differ — a full copy is moved to the trash and replaced by the
pointer. Its lines name `memar update --apply` rather than this layer: a bare
`memar install` would also write into the project the caller stands in.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
from pathlib import Path

from machine.env_location import resolve_root
from machine.fs_trash import soft_delete
from services.install_project import POSIX_BOOTSTRAP, WINDOWS_BOOTSTRAP

APP_DIRS = {
    "agents": lambda: Path.home() / ".agents",
    "cursor": lambda: Path.home() / ".cursor",
    "claude": lambda: Path.home() / ".claude",
    "codex": lambda: Path.home() / ".codex",
    "opencode": lambda: Path.home() / ".config" / "opencode",
}

# The one file an app's skill folder holds.
POINTER_NAME = "SKILL.md"
# The checkout's skill, as `memar content path` resolves it.
SKILL_RELATIVE = ".agents/skills/memar/SKILL.md"
POINTER_BODY = (
    "# Memar\n"
    "This file points to the Memar skill; it is not the skill. `memar install` "
    "wrote it, and `memar update --apply` rewrites it.\n\n"
    f"Load the Memar skill: run `memar content path {SKILL_RELATIVE}`, then load "
    "and follow the file it prints.\n\n"
    "If `memar` is not on PATH, Memar is not available to this program yet. "
    "Run the bootstrap for your platform:\n\n"
    "Windows:\n\n"
    "```powershell\n"
    f"{WINDOWS_BOOTSTRAP}\n"
    "```\n\n"
    "macOS or Linux:\n\n"
    "```sh\n"
    f"{POSIX_BOOTSTRAP}\n"
    "```\n"
)


def skill_dest_for_app(app: str) -> Path:
    return APP_DIRS[app]() / "skills" / "memar"


def skill_destinations(*, existing_only: bool, app: str | None) -> list[Path]:
    if app is not None:
        app_dir = APP_DIRS[app]()
        dest = skill_dest_for_app(app)
        if existing_only:
            if not dest.is_dir():
                sys.exit(f"error: no existing Memar skill pointer at {dest}")
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


def skill_description(source: Path) -> str:
    """The `description` entry of SOURCE's SKILL.md frontmatter, as written there, continuation lines included."""
    skill = source / POINTER_NAME
    lines = skill.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        sys.exit(f"error: {skill} has no frontmatter to take the skill's description from")
    entry: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if entry and line[:1] in (" ", "\t"):
            entry.append(line)
        elif entry:
            break
        elif line.startswith("description:"):
            entry.append(line)
    if not entry:
        sys.exit(f"error: {skill} has no description in its frontmatter")
    return "\n".join(entry)


def pointer_text(source: Path) -> str:
    """The SKILL.md an agent app gets: the checkout's name and description, and the way to the checkout's skill."""
    return f"---\nname: memar\n{skill_description(source)}\n---\n\n{POINTER_BODY}"


def pointer_current(dest: Path, text: str) -> bool:
    """Whether DEST holds TEXT as its only file — no full copy, no other file beside it."""
    try:
        if sorted(p.name for p in dest.iterdir()) != [POINTER_NAME]:
            return False
        return (dest / POINTER_NAME).read_bytes() == text.encode("utf-8")
    except OSError:
        return False


def write_pointer(text: str, dest: Path, *, dry_run: bool) -> None:
    pointer = dest / POINTER_NAME
    if dry_run:
        print(f"dry-run: write {pointer}:")
        for line in text.splitlines():
            print(f"    {line}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        # What is there may be a full copy from an earlier install or hold a
        # local edit. Move it to the trash, so it can be taken back, then write
        # the pointer.
        soft_delete(dest)
    dest.mkdir()
    # newline="\n": the same bytes on every platform, so the stale comparison
    # does not depend on which one wrote the file.
    pointer.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote skill pointer -> {pointer}")


def stale_copies(source: Path) -> list[Path]:
    """The skill folders already in agent apps that are not the pointer SOURCE would now write; none when SOURCE has no skill."""
    if not (source / POINTER_NAME).is_file():
        return []
    text = pointer_text(source)
    return [
        dest
        for dest in skill_destinations(existing_only=True, app=None)
        if not pointer_current(dest, text)
    ]


# The one command that refreshes what Memar installed; a stale line names it.
REFRESH = "memar update --apply"


def checkout_skill() -> Path:
    """The skill folder in the checkout the location variable names, which the pointer is made from.

    Asked of the module that owns the variable and refuses to guess when it
    names no repository, because a session that quietly put a checkout on the
    machine would produce a location nothing else agrees on.
    """
    return resolve_root() / ".agents" / "skills" / "memar"


def warn_stale(source: Path) -> None:
    """One line per stale pointer or full copy, naming the command that refreshes them."""
    for dest in stale_copies(source):
        print(
            f"stale: the Memar skill at {dest} is not the pointer the checkout would write; "
            f"refresh with: {REFRESH}"
        )


def into_apps(*, dry_run: bool = False, app: str | None = None, existing_only: bool = False) -> None:
    """Write the skill pointer into every agent app found, or into APP only, leaving one already current; with EXISTING_ONLY only where a skill folder exists."""
    dests = skill_destinations(existing_only=existing_only, app=app)
    if existing_only and not dests:
        sys.exit("error: no existing Memar skill pointers found to update")
    source = checkout_skill()
    print(f"Memar resolves to {source.parents[2]}")
    text = pointer_text(source)
    for dest in dests:
        if pointer_current(dest, text):
            print(f"already current: {dest}")
            continue
        write_pointer(text, dest, dry_run=dry_run)
