#!/usr/bin/env python3
"""memar-install-agents.py — put Memar into a project as https://agents.md/ instructions.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `--help` prints: it is addressed to whoever wants Memar in a
project and says what lands there and what does not. Everything from here down
is addressed to whoever opens this file.

Writes two things: a one-line `## Memar` section in the project's AGENTS.md
pointing at `.agents/memar/README.md`, and that README. AGENTS.md is not the
place for how to install Memar — it is read on every session and needs only to
say which file to read; the README beside it carries the substance.

It places no script and no Python file in the project: the bootstrap for the
machine is fetched from the Memar repository at the point of use, and a copy per
repository is unmaintainable — every change here would have to be re-copied into
every project by hand.

Where Memar lives on this machine is one thing, and this file asks rather than
decides: `machine/env_location.py` is the one module that reads the location
variable, and `memar_repository.py` holds the test of what a Memar repository is
— which is what keeps the Memar repository's own hand-written README from being
replaced by the text written for a project that has to fetch Memar first.

Run it from the project you want Memar in, a subdirectory being fine — this walks
up to the version-control root — with the Memar checkout's own copy beside it:

  python "$MEMAR_ROOT/.agents/scripts/memar-install-agents.py"

Needs Python 3 and a Memar checkout on this machine. It never installs anything:
the machine is settled before this runs, and the README it writes says what to
run when it is not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from memar_console import use_utf8_stdio
from memar_repository import is_memar_repository
from machine.env_location import VARIABLE, recorded_value

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
# A failed fetch must not look like success. `sh -c "$(curl …)"` runs an empty
# script and exits 0 when curl fails, so the command stops unless the fetch
# produced a script.
POSIX_BOOTSTRAP = (
    "sh -c 'c=$(curl -fsSL "
    f"{SCRIPTS_RAW}/install.sh); test -n \"$c\" && exec sh -c \"$c\" install.sh'"
)
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
    "This project is developed within Memar's framework.\n\n"
    "Load the Memar skill at the start of every session: run `memar content "
    "path .agents/skills/memar/SKILL.md`, then load and follow the file it "
    "prints.\n\n"
    "If `memar` is not on PATH, Memar is not available to this program yet. "
    "Run the bootstrap for your platform:\n\n"
    "Windows:\n\n"
    "```powershell\n"
    f"{WINDOWS_BOOTSTRAP}\n"
    "```\n\n"
    "macOS or Linux:\n\n"
    "```sh\n"
    f"{POSIX_BOOTSTRAP}\n"
    "```"
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
    if not is_memar_repository(target):
        write_text(
            target / CONSUMER_README,
            CONSUMER_README_TEXT,
            dry_run=dry_run,
        )
    agents_index = target / ".agents" / "README.md"
    if not agents_index.is_file():
        write_text(agents_index, AGENTS_DIR_README, dry_run=dry_run)
    if not dry_run:
        # Asked of the module that owns the variable, so a session opened
        # before it was written does not conclude Memar was never installed and
        # send this project to the bootstrap a second time.
        recorded = recorded_value()
        if not recorded:
            print(
                f"{VARIABLE} is not set, so Memar is not on this machine yet; the "
                "bootstrap this project now points at installs it",
                file=sys.stderr,
            )
        else:
            print(f"{VARIABLE} is set to {recorded}")


DESCRIPTION = """memar-install-agents — let a project know Memar exists

Writes two things into the project you run this from:

  - a `## Memar` line in its AGENTS.md, saying which file to read;
  - that file, `.agents/memar/README.md`, which carries the substance.

Nothing else is placed there. No script and no Python file — a project's copy of
Memar's tooling would go stale on every change here, so the tooling is fetched
from the Memar repository when it is needed instead.

Run this from the project, or any folder inside it. `memar install` already does
this for you; run it directly when you want the project layer and nothing else.

    (none)      put Memar into the current project
    update      refresh a project that already has it
"""


def main() -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
