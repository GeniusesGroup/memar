#!/usr/bin/env python3
"""Copy the Memar skill into local AI agent apps.

Does not write AGENTS.md or `.agents/memar/` — that is install-agents.py
(the https://agents.md/ project pointer).

  python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install-apps.py').read().decode())"

Needs Python 3 and network access to GitHub. Needs git only when no
usable Memar checkout is already present. If git is missing, git.py
tries to install it.

  (none)             every detected agent app
  cursor|claude|codex|opencode|agents
                     one app only (error if that app's directory is missing)
  update             refresh existing skill copies

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import runpy
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

THIS = "install-apps.py"
SESSION_URL = (
    "https://raw.githubusercontent.com/GeniusesGroup/memar/main"
    "/.agents/scripts/session.py"
)
SKILL_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
APP_DIRS = {
    "agents": lambda: Path.home() / ".agents",
    "cursor": lambda: Path.home() / ".cursor",
    "claude": lambda: Path.home() / ".claude",
    "codex": lambda: Path.home() / ".codex",
    "opencode": lambda: Path.home() / ".config" / "opencode",
}


def _on_disk() -> bool:
    try:
        parent = Path(__file__).resolve().parent
    except NameError:
        return False
    if not (parent / "session.py").is_file():
        return False
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
    return True


def _utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


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


def copy_skill(dest: Path, *, dry_run: bool) -> None:
    import session

    source = session.ensure_memar_root() / ".agents" / "skills" / "memar"
    if dry_run:
        print(f"dry-run: copy {source} -> {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest, ignore=SKILL_IGNORE)
    print(f"copied skill -> {dest}")


def main() -> None:
    _utf8_stdio()
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
    for dest in dests:
        copy_skill(dest, dry_run=args.dry_run)


if __name__ == "__main__":
    if not _on_disk():
        ns = {"__name__": "memar_session"}
        exec(
            compile(urllib.request.urlopen(SESSION_URL).read(), SESSION_URL, "exec"),
            ns,
        )
        ns["ensure_memar_root"]()
        live = (
            Path(tempfile.gettempdir())
            / "memar"
            / ".agents"
            / "scripts"
            / THIS
        )
        runpy.run_path(str(live), run_name="__main__")
        raise SystemExit(0)
    main()
