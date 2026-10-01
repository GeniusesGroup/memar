#!/usr/bin/env python3
"""Install Memar into a project as https://agents.md/ instructions.

Writes two things: a one-line `## Memar` section in the project's AGENTS.md
pointing at `.agents/memar/README.md`, and that README. AGENTS.md is not the
place for how to install Memar — it is read on every session and needs only to
say which file to read; the README beside it carries the substance.

It places no script and no Python file in the project: the bootstrap for the
machine is fetched from the Memar repository at the point of use, and a copy per
repository is unmaintainable — every change here would have to be re-copied into
every project by hand.

Where Memar lives on this machine is one thing: the MEMAR_ROOT environment
variable, written at install time by `.agents/scripts/install.py` and read by
everything, including the test this script asks that file for rather than
carrying: whether a folder is the Memar repository, which is what keeps the
Memar repository's own hand-written README from being replaced by this text.

Run it from the project you want Memar in, a subdirectory being fine — this walks
up to the version-control root — with the Memar checkout's own copy beside it:

  python "$MEMAR_ROOT/.agents/scripts/install-agents.py"

Needs Python 3 and a Memar checkout on this machine. It never resolves MEMAR_ROOT
itself and never installs anything: the machine is settled before this runs, and
the README it writes says what to run when it is not.

  (none)    install into the current project
  update    refresh an existing project install

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import install

PUBLISH_BRANCH = "main"
SCRIPTS_RAW = (
    f"https://raw.githubusercontent.com/GeniusesGroup/memar/{PUBLISH_BRANCH}/.agents/scripts"
)
# The point-of-use command, per platform: fetch the bootstrap from the publishing
# branch and run it where it stands. Both addresses are built from the one base
# this script publishes under, so the command a consumer is told to run cannot
# name a different branch than the one this file ships on.
WINDOWS_BOOTSTRAP = (
    "powershell -ExecutionPolicy Bypass -Command \"& ([scriptblock]::Create((irm "
    f"{SCRIPTS_RAW}/install.ps1)))\""
)
POSIX_BOOTSTRAP = f'sh -c "$(curl -fsSL {SCRIPTS_RAW}/install.sh)" install.sh'
# One path, used both as the file written and as the link AGENTS.md points at, so
# the pointer cannot name a file that is not there.
CONSUMER_README = Path(".agents") / "memar" / "README.md"
MEMAR_HEADING = "## Memar"
AGENTS_H1 = "# Repository instructions"
AGENTS_SECTION_BODY = (
    "Before any other work in a session, read "
    f"[`{CONSUMER_README.as_posix()}`]({CONSUMER_README.as_posix()})."
)
# The substance, in the document AGENTS.md points at rather than in AGENTS.md.
README_BODY = (
    "`MEMAR_ROOT` names the Memar checkout on this machine. If it is unset, run "
    "the bootstrap from Memar's repository — it makes sure git and Python are "
    "here, then installs Memar and writes that variable:\n\n"
    "```\n"
    f"{WINDOWS_BOOTSTRAP}   # Windows\n"
    f"{POSIX_BOOTSTRAP}   # POSIX\n"
    "```\n\n"
    "Then restart your program: a program of your own that is already running "
    "keeps the value it was started with, while the scripts in the checkout that "
    "variable names read the platform's record of it and see it at once. Load "
    "`.agents/skills/memar/SKILL.md` from the checkout that variable names, and use "
    "the scripts in its `.agents/scripts/`. To put Memar into another project, run "
    "`install-agents.py` from that checkout, in that project."
)
CONSUMER_README_TEXT = f"# Memar\n{README_BODY}\n"
AGENTS_DIR_README = """# Agents
This directory holds configuration and practices for agents working on this project. It is not reserved for any one framework. What a session should load is declared in [AGENTS.md](../AGENTS.md). Discover what lives here by listing the directory.
"""
HEADING_RE = re.compile(r"(?m)^## Memar[ \t]*$")
NEXT_HEADING_RE = re.compile(r"(?m)^#{1,2}[ \t]+\S")
VCS_MARKERS = (".git", ".hg", ".svn", ".fossil", ".bzr", "_darcs", ".pijul")


def _has_vcs_marker(path: Path) -> bool:
    return any((path / name).exists() for name in VCS_MARKERS)


def _vcs_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if _has_vcs_marker(candidate):
            return candidate
    return None


def resolve_project_dir(cwd: Path) -> Path:
    cwd = cwd.resolve()
    if cwd == Path.home().resolve() or cwd.parent == cwd:
        sys.exit(
            f"error: {cwd} is not a project directory; run from the "
            "version-controlled project you want Memar in"
        )
    root = _vcs_root(cwd)
    if root is not None:
        if root != cwd:
            print(f"using repository root {root}", file=sys.stderr)
        return root
    print(
        f"warning: no VCS metadata under {cwd}; installing into this directory",
        file=sys.stderr,
    )
    return cwd


def memar_section_markdown() -> str:
    return f"{MEMAR_HEADING}\n{AGENTS_SECTION_BODY}\n"


def upsert_memar_section(content: str) -> str:
    section = memar_section_markdown()
    match = HEADING_RE.search(content)
    if match is None:
        stripped = content.rstrip()
        if stripped:
            return stripped + "\n\n" + section
        return f"{AGENTS_H1}\n\n{section}"
    start = match.start()
    rest = content[match.end() :]
    next_heading = NEXT_HEADING_RE.search(rest)
    if next_heading is None:
        prefix = content[:start].rstrip()
        if prefix:
            return prefix + "\n\n" + section
        return section
    end = match.end() + next_heading.start()
    prefix = content[:start].rstrip()
    suffix = content[end:].lstrip("\n")
    middle = section
    if prefix:
        middle = prefix + "\n\n" + section
    if suffix:
        return middle.rstrip() + "\n" + suffix
    return middle


def has_memar_section(content: str) -> bool:
    return HEADING_RE.search(content) is not None


def write_text(path: Path, text: str, *, dry_run: bool) -> None:
    if not text.endswith("\n"):
        text += "\n"
    if dry_run:
        print(f"dry-run: write {path}")
        print(text, end="" if text.endswith("\n") else "\n")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n": the text is written on whichever platform ran this, not the
    # one that will read it.
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path}")


def cmd_install(*, dry_run: bool, require_existing: bool) -> None:
    target = resolve_project_dir(Path.cwd())
    agents = target / "AGENTS.md"
    if require_existing:
        if not agents.is_file() or not has_memar_section(
            agents.read_text(encoding="utf-8")
        ):
            sys.exit("error: Memar is not installed in this project")
    if agents.is_file():
        updated = upsert_memar_section(agents.read_text(encoding="utf-8"))
    else:
        updated = upsert_memar_section("")
    write_text(agents, updated, dry_run=dry_run)
    # The Memar repository installs itself, and its .agents/memar/README.md is
    # written by hand to point at its own skill; it must not be replaced by the
    # text written for a project that has to fetch Memar first.
    if not install.is_memar_repository(target):
        write_text(
            target / CONSUMER_README,
            CONSUMER_README_TEXT,
            dry_run=dry_run,
        )
    agents_index = target / ".agents" / "README.md"
    if not agents_index.is_file():
        write_text(agents_index, AGENTS_DIR_README, dry_run=dry_run)
    if not dry_run:
        recorded = os.environ.get("MEMAR_ROOT", "").strip()
        if not recorded:
            print(
                "MEMAR_ROOT is not set, so Memar is not on this machine yet; the "
                "bootstrap this project now points at installs it",
                file=sys.stderr,
            )
        else:
            print(f"MEMAR_ROOT is set to {recorded}")


def main() -> None:
    install.use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print writes without touching the filesystem",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default=None,
        help="omitted: install into the current project; 'update': refresh",
    )
    args = parser.parse_args()
    if args.command not in (None, "update"):
        sys.exit("error: unknown command; expected omitted or update")
    cmd_install(dry_run=args.dry_run, require_existing=args.command == "update")


if __name__ == "__main__":
    main()
