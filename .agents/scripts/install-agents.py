#!/usr/bin/env python3
"""Install Memar into a project as https://agents.md/ instructions.

Writes AGENTS.md (a ## Memar section) and `.agents/memar/` so a session
reads that README and runs the Python file beside it. Does not copy the
skill into agent apps — that is install-apps.py.

Fetch and run from the project (a subdirectory is fine; this walks up to
the version-control root):

  python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install-agents.py').read().decode())"

Needs Python 3 and network access to GitHub. Needs git only when no
usable Memar checkout is already present. If git is missing, git.py
tries to install it.

  (none)    install into the current project
  update    refresh an existing project install

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import re
import runpy
import sys
import tempfile
import urllib.request
from pathlib import Path

THIS = "install-agents.py"
SESSION_URL = (
    "https://raw.githubusercontent.com/GeniusesGroup/memar/main"
    "/.agents/scripts/session.py"
)
MEMAR_HEADING = "## Memar"
AGENTS_H1 = "# Repository instructions"
AGENTS_SECTION_BODY = (
    "Before any other work in a session, read "
    "[`.agents/memar/README.md`](.agents/memar/README.md)."
)
CONSUMER_README = """# Memar
Run [session.py](./session.py) beside this file before any other work. It prints the Memar checkout to load. Then open `.agents/skills/memar/SKILL.md` from that path and use the scripts beside it.
"""
PROJECT_SESSION = f'''#!/usr/bin/env python3
"""Print the Memar checkout this session should load.

Canonical Memar is the process temp directory plus a folder named memar.
This file only invokes that copy.
"""
from pathlib import Path
import runpy
import tempfile
import urllib.request

SESSION = (
    Path(tempfile.gettempdir()) / "memar" / ".agents" / "scripts" / "session.py"
).resolve()
URL = {SESSION_URL!r}


def main() -> None:
    if SESSION.is_file():
        runpy.run_path(str(SESSION), run_name="__main__")
        return
    exec(compile(urllib.request.urlopen(URL).read(), URL, "exec"), {{"__name__": "__main__"}})


if __name__ == "__main__":
    main()
'''
AGENTS_DIR_README = """# Agents
This directory holds configuration and practices for agents working on this project. It is not reserved for any one framework. What a session should load is declared in [AGENTS.md](../AGENTS.md). Discover what lives here by listing the directory.
"""
HEADING_RE = re.compile(r"(?m)^## Memar[ \t]*$")
NEXT_HEADING_RE = re.compile(r"(?m)^#{1,2}[ \t]+\S")
VCS_MARKERS = (".git", ".hg", ".svn", ".fossil", ".bzr", "_darcs", ".pijul")


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
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path}")


def cmd_install(*, dry_run: bool, require_existing: bool) -> None:
    import session

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
    if not session.is_usable_memar(target):
        write_text(
            target / ".agents" / "memar" / "README.md",
            CONSUMER_README,
            dry_run=dry_run,
        )
        write_text(
            target / ".agents" / "memar" / "session.py",
            PROJECT_SESSION,
            dry_run=dry_run,
        )
    agents_index = target / ".agents" / "README.md"
    if not agents_index.is_file():
        write_text(agents_index, AGENTS_DIR_README, dry_run=dry_run)
    if not dry_run:
        session.ensure_memar_root()


def main() -> None:
    _utf8_stdio()
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
