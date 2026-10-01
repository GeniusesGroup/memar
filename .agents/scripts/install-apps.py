#!/usr/bin/env python3
"""Copy the Memar skill into local AI agent apps.

Does not write AGENTS.md or `.agents/memar/` — that is install-agents.py
(the https://agents.md/ project pointer).

The skill is copied from the Memar checkout that $MEMAR_ROOT names, read by
`install.py` in this folder, which is also where the writing of that variable
lives. This script never copies the repository anywhere else. The skill carries
no scripts: the navigation script it names lives in the checkout, in
`.agents/scripts/`, and is reached there rather than copied here.

Run it from the Memar checkout, with the file beside it:

  python .agents/scripts/install-apps.py

Needs Python 3 and a Memar checkout on this machine. If MEMAR_ROOT is unset this
script says so and points at the install script; it does not clone the
repository to find one.

  (none)             every detected agent app
  cursor|claude|codex|opencode|agents
                     one app only (error if that app's directory is missing)
  update             refresh existing skill copies

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import install

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
        shutil.rmtree(dest)
    shutil.copytree(source, dest, ignore=install.NEVER_COPIED)
    print(f"copied skill -> {dest}")


def main() -> None:
    install.use_utf8_stdio()
    apps = ", ".join(APP_DIRS)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print copies without touching the filesystem",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default=None,
        help=(
            "omitted: all detected agent apps; "
            f"an app name ({apps}): that app only; "
            "'update': refresh existing copies"
        ),
    )
    args = parser.parse_args()
    existing_only = False
    app: str | None = None
    if args.command is None:
        pass
    elif args.command == "update":
        existing_only = True
    elif args.command in APP_DIRS:
        app = args.command
    else:
        sys.exit(
            f"error: unknown command {args.command!r}; "
            f"expected omitted, update, or an app name ({apps})"
        )
    dests = skill_destinations(existing_only=existing_only, app=app)
    if existing_only and not dests:
        sys.exit("error: no existing Memar skill copies found to update")
    # install.py is the only thing that reads where Memar lives on this machine,
    # and this is the one read whose answer is reported and acted on.
    root = install.resolve_root()
    print(f"Memar resolves to {root}")
    source = root / ".agents" / "skills" / "memar"
    for dest in dests:
        copy_skill(source, dest, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

