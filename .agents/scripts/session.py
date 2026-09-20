#!/usr/bin/env python3
"""Print the canonical Memar checkout this session should load.

That checkout is always the process temp directory plus a folder named
`memar`. If a usable Memar tree is already beside the current project
(or this process is running from one), that tree is the source and the
temp path is a directory symlink to it. Otherwise this script clones
into the temp path. Load `.agents/skills/memar/SKILL.md` from the printed
path and use the scripts beside it.

A Memar checkout does not run this file to find itself; consuming
projects invoke it through `.agents/memar/session.py`.

Needs Python 3. Needs network and git only when the temp path is empty
and no sibling checkout exists. If git is missing, git.py tries to
install it. Peer scripts are invoked as programs, not imported.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

SCRIPTS_RAW = (
    "https://raw.githubusercontent.com/GeniusesGroup/memar/main"
    "/.agents/scripts"
)
REPO_URL = "https://github.com/GeniusesGroup/memar.git"
SKILL_MARKER = Path(".agents") / "skills" / "memar" / "SKILL.md"
SESSION_SCRIPT = Path(".agents") / "scripts" / "session.py"


def _utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def canonical_memar() -> Path:
    return Path(tempfile.gettempdir()) / "memar"


def is_usable_memar(path: Path) -> bool:
    path = path.resolve()
    return (
        (path / "README.md").is_file()
        and (path / "docs").is_dir()
        and (path / SKILL_MARKER).is_file()
    )


def _walk_starts() -> list[Path]:
    starts: list[Path] = [Path.cwd()]
    try:
        starts.insert(0, Path(__file__).resolve().parent)
    except NameError:
        pass
    return starts


def find_local_memar() -> Path | None:
    seen: set[Path] = set()
    for start in _walk_starts():
        for candidate in [start, *start.parents]:
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            if is_usable_memar(resolved):
                return resolved
            sibling = (resolved.parent / "memar").resolve()
            if sibling not in seen and is_usable_memar(sibling):
                return sibling
    return None


def _scripts_dir() -> Path | None:
    try:
        here = Path(__file__).resolve().parent
        if (here / "fs.py").is_file() and (here / "git.py").is_file():
            return here
    except NameError:
        pass
    found = find_local_memar()
    if found is not None:
        directory = found / ".agents" / "scripts"
        if (directory / "fs.py").is_file():
            return directory
    directory = canonical_memar() / ".agents" / "scripts"
    if (directory / "fs.py").is_file():
        return directory
    return None


def _run_script(path: Path, args: list[str]) -> None:
    completed = subprocess.run(
        [sys.executable, str(path), *args],
        check=False,
    )
    if completed.returncode != 0:
        sys.exit(completed.returncode)


def _script(name: str) -> Path:
    directory = _scripts_dir()
    if directory is not None:
        path = directory / f"{name}.py"
        if path.is_file():
            return path
    url = f"{SCRIPTS_RAW}/{name}.py"
    path = Path(tempfile.gettempdir()) / f"memar-{name}.py"
    path.write_bytes(urllib.request.urlopen(url).read())
    return path


def _link(link: Path, target: Path) -> None:
    fs_py = target / ".agents" / "scripts" / "fs.py"
    if not fs_py.is_file():
        fs_py = _script("fs")
    _run_script(fs_py, ["link", "--replace", str(link), str(target)])


def _clone(dest: Path) -> None:
    _run_script(_script("git"), ["ensure"])
    if dest.exists() or dest.is_symlink():
        _run_script(_script("fs"), ["trash", str(dest)])
    dest.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(dest)],
        check=False,
    )
    if completed.returncode != 0 or not is_usable_memar(dest):
        shutil.rmtree(dest, ignore_errors=True)
        sys.exit(f"error: `git clone --depth 1 {REPO_URL}` failed")


def ensure_memar_root() -> Path:
    dest = canonical_memar()
    found = find_local_memar()
    if found is not None and found.resolve() != dest.resolve():
        _link(dest, found)
        return dest
    if is_usable_memar(dest):
        return dest
    _clone(dest)
    return dest


def _this_file() -> Path | None:
    try:
        return Path(__file__).resolve()
    except NameError:
        return None


def main() -> None:
    _utf8_stdio()
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="ensure the checkout without printing its path",
    )
    args = parser.parse_args()
    root = ensure_memar_root()
    live = (root / SESSION_SCRIPT).resolve()
    here = _this_file()
    if live.is_file() and (here is None or here != live):
        _run_script(live, ["--quiet"] if args.quiet else [])
        return
    if not args.quiet:
        # Print the resolved real tree. Canonical temp may be a
        # symlink/junction; agent runtimes that refuse unverified temp
        # path strings still need a concrete checkout path to load.
        print(root.resolve())


if __name__ == "__main__":
    main()
