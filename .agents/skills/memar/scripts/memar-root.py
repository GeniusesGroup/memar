#!/usr/bin/env python3
"""memar-root.py — resolve the local Memar repository root.

Resolves, and if necessary creates, the local clone of the Memar
documentation repository and prints its absolute path.

Behavior
- Explicit path wins: --root PATH, then the Memar repository this script
  ships in (found by walking up from the script's location and the working
  directory until a directory holds README.md, docs/, and
  .agents/skills/memar/SKILL.md — a marker only a Memar checkout has, so a
  skill-only copy never matches), then $MEMAR_ROOT, then a
  sibling checkout named `memar` next to the current project (so a machine
  that clones both `memar` and e.g. `organization` side-by-side can point
  at the local Memar without a temp clone), else a single canonical
  temporary location: ${TMPDIR:-/tmp}/memar (platform temp dir on
  Windows/macOS). The canonical name is `memar` — never `-repo` or other
  suffixes — matching the skill's path-resolution rules. Ships-in precedes
  $MEMAR_ROOT so an open Memar checkout wins over a stale env from a prior
  session. `git` is required only when a clone (or `--update`) is actually
  needed; an already-usable root works without it.
- Reuse: an existing directory holding `README.md` and `docs/` is reused —
  a `.git` directory is not required, so archive downloads work too; a
  partial or failed clone in the canonical temp location is deleted and
  re-cloned.
- Clone: shallow (`git clone --depth 1`) from
  https://github.com/GeniusesGroup/memar.git
  A shallow clone is preferred over the GitHub REST API, which
  rate-limits quickly; clone does not.
- Update: pass --update to `git pull --ff-only` a reused, cloned root
  (no-op for archive downloads, which have no `.git`). Never done
  implicitly: repeated re-pulls waste time and can churn pinned versions.

Exit codes
  0 — a usable Memar root exists (its path is the last stdout line)
  1 — git is unavailable when a clone is required, the clone failed, or
      PATH is unusable

The printed path is safe to consume in shell and in agent tool calls:
  MEMAR_ROOT="$(python scripts/memar-root.py)"
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/GeniusesGroup/memar.git"
CANONICAL_DIRNAME = "memar"  # same as the repository name; no suffixes


def _canonical_root() -> Path:
    # tempfile.gettempdir() honors TMPDIR/TEMP/TMP and falls back sanely.
    return Path(tempfile.gettempdir()) / CANONICAL_DIRNAME


def _sibling_root() -> Path | None:
    # Side-by-side checkouts: .../memar and .../organization. Prefer a
    # usable sibling named `memar` over cloning into temp.
    seen: set[Path] = set()
    for path in [Path.cwd(), *Path.cwd().parents]:
        sibling = (path.parent / CANONICAL_DIRNAME).resolve()
        if sibling in seen:
            continue
        seen.add(sibling)
        if sibling == path.resolve():
            continue
        if _is_usable_root(sibling):
            return sibling
    return None


def _candidate_roots(explicit: str | None) -> list[Path]:
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit).expanduser())
    env = os.environ.get("MEMAR_ROOT")
    if env:
        roots.append(Path(env).expanduser())
    sibling = _sibling_root()
    if sibling is not None:
        roots.append(sibling)
    roots.append(_canonical_root())
    return roots


def _is_usable_root(path: Path) -> bool:
    # A usable Memar root needs the entry document and the docs directory;
    # a `.git` directory is deliberately not required (archive downloads
    # are valid read-only roots).
    return (path / "README.md").is_file() and (path / "docs").is_dir()


def _git_available() -> bool:
    return shutil.which("git") is not None


def _run_git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _clone(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    result = _run_git(["clone", "--depth", "1", REPO_URL, str(target)])
    if result.returncode != 0 or not _is_usable_root(target):
        # Remove the partial clone so a retry starts clean.
        shutil.rmtree(target, ignore_errors=True)
        sys.stderr.write(
            f"error: `git clone --depth 1 {REPO_URL} {target}` failed\n"
        )
        if result.stderr.strip():
            sys.stderr.write(result.stderr.strip() + "\n")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve (clone if needed) and print the local Memar root."
    )
    parser.add_argument(
        "--root",
        metavar="PATH",
        default=None,
        help="use this checkout instead of $MEMAR_ROOT or the default temp location",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="with an existing checkout, `git pull --ff-only` before printing",
    )
    args = parser.parse_args()

    root: Path | None = None
    explicit = Path(args.root).expanduser() if args.root else None

    if explicit is not None:
        # An explicit --root is sticky: usable → use it; missing → clone
        # into it; present-but-wrong → refuse (never delete a user path).
        if explicit.exists() and not _is_usable_root(explicit):
            sys.stderr.write(
                f"error: {explicit} exists but is not a Memar root "
                "(no README.md + docs/); choose another --root\n"
            )
            sys.exit(1)
        root = explicit
    else:
        # The repository this script ships in, when the script is run from
        # a checkout (or archive) of it: walk up from the script's location
        # and the working directory until the Memar-repo marker appears.
        marker = Path(".agents") / "skills" / "memar" / "SKILL.md"
        starts = [Path(__file__).resolve().parent, Path.cwd()]
        seen: set[Path] = set()
        for start in starts:
            for candidate in [start, *start.parents]:
                if candidate in seen:
                    continue
                seen.add(candidate)
                if (candidate / marker).is_file() and _is_usable_root(candidate):
                    root = candidate
                    break
            if root is not None:
                break
        if root is None:
            for candidate in _candidate_roots(None):
                if not candidate.exists():
                    continue
                if _is_usable_root(candidate):
                    root = candidate
                    break
                # Exists but not a Memar root (stale partial clone, wrong
                # content): only the canonical temp location is safe to
                # replace.
                if candidate == _canonical_root():
                    sys.stderr.write(
                        f"warning: replacing non-root content at {candidate}\n"
                    )
                    shutil.rmtree(candidate, ignore_errors=True)

    if root is None or not _is_usable_root(root):
        target = root or _canonical_root()
        if not _git_available():
            sys.stderr.write(
                "error: `git` was not found on PATH; a clone is required\n"
            )
            sys.exit(1)
        _clone(target)
        root = target
    elif args.update and (root / ".git").exists():
        if not _git_available():
            sys.stderr.write(
                "warning: `git` not on PATH; skipping --update\n"
            )
        else:
            pull = _run_git(["pull", "--ff-only"], cwd=root)
            if pull.returncode != 0:
                sys.stderr.write(
                    "warning: update failed; using the existing checkout\n"
                )
                if pull.stderr.strip():
                    sys.stderr.write(pull.stderr.strip() + "\n")

    if root is None or not _is_usable_root(root):
        sys.stderr.write(
            f"error: {root} does not look like the Memar repository "
            "(no README.md + docs/); remove it and retry\n"
        )
        sys.exit(1)

    print(str(root.resolve()))


if __name__ == "__main__":
    main()
