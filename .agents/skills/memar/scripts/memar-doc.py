#!/usr/bin/env python3
"""memar-doc.py — resolve, read, and search Memar documentation.

For agents: instead of resolving Markdown links by hand and hoping the
file exists, ask this script. Every path Memar documentation uses —
`/docs/...`, `./foo.md`, `../bar.md`, anchors — is relative to the Memar
repository root (never to the user's project or the machine root).

Subcommands
  path REF [REF ...]     Resolve reference(s) to absolute file paths.
                         REF may be a root-style path (`/docs/cognition.md`),
                         a document-relative link with `--from FILE`, or a
                         bare name (`cognition.md`, `docs/cognition.md` —
                         resolved against the root; prefer bare names on
                         Git Bash/MSYS shells, which rewrite leading-`/`
                         arguments into Windows paths before this script
                         sees them). `#anchor` and `?section` suffixes are
                         split off and echoed, not validated. Prints one
                         absolute path per line.
  meta FILE [FILE ...]   Print front matter (--- YAML block or H1 line) plus
                         the Abstract — the relevance-judging unit, so an
                         agent can decide what to read without opening
                         whole files.
  section FILE HEADING   Print one section: the text under a heading whose
                         title matches HEADING (case-insensitive, level-2 or
                         deeper), up to the next heading of the same or
                         higher level. Great for "read only the needed part".
  search PATTERN         Full-text regex search across the explanatory /
                         practice surface of the doc set (not handoff,
                         changelog, or research companions — those are
                         opened only when explicitly named or linked), one
                         `path:line:text` hit per line. Memar's rule is to
                         search full-text, not by filename (filenames are
                         slugs, not a taxonomy) — this makes that rule cheap.
                         Extra args are extra regexes; files matching all are
                         listed (`path:all-matched`).

Root resolution: --root PATH, then $MEMAR_ROOT, then `memar-root.py`
(which resolves the canonical temp clone). Only files under the root and
under a `docs` directory are ever returned.

Examples
  python scripts/memar-doc.py path /docs/cognition.md
  python scripts/memar-doc.py path ./modeling.md --from docs/system.md
  python scripts/memar-doc.py meta /docs/framework.md
  python scripts/memar-doc.py section /docs/framework.md "Goal-Oriented Frameworks and Purpose Space"
  python scripts/memar-doc.py search "generics|polymorphism"
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Windows consoles default to a legacy codepage (e.g. cp1252) while Memar
# docs are UTF-8; force UTF-8 output so printing content never crashes.
for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8", errors="replace")

# Companion facets that are *not* the explanatory surface. Blind `search`
# is for finding what to study or follow; these companions are reached only
# when explicitly named (`path` / `meta` / `section`) or linked from a base
# document — never as search hits during an explanatory / Q&A session:
#   - .handoff.md        — resume developing the base document
#   - .changelog.md      — audit history
#   - .research.<NNN>.md — inquiry trail (same role as changelog for readers
#                         of settled explanation; matched by pattern below)
# Practice companions (.practice.md) stay in search: their reader
# relationship is "follow to accomplish," which discovery must surface.
# Governing specs such as documentation-research.md are Explanation-facet
# documents (hyphen, not `.research.<NNN>`), so search still finds them.
_SEARCH_EXCLUDED_SUFFIXES = (".handoff.md", ".changelog.md")
_RESEARCH_COMPANION = re.compile(r"\.research\.\d+\.md$", re.IGNORECASE)


# ---------------------------------------------------------------- root

def _find_companion(script_dir: Path) -> Path | None:
    sibling = script_dir / "memar-root.py"
    if sibling.is_file():
        return sibling
    return None


def resolve_root(explicit: str | None) -> Path:
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    env = os.environ.get("MEMAR_ROOT")
    if env:
        candidates.append(env)
    for candidate in candidates:
        path = Path(candidate).expanduser()
        if (path / "README.md").is_file():
            return path.resolve()
        sys.stderr.write(
            f"error: {path} does not look like the Memar repository "
            "(no README.md)\n"
        )
        sys.exit(1)

    companion = _find_companion(Path(__file__).resolve().parent)
    if companion is not None:
        result = subprocess.run(
            [sys.executable, str(companion)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            printed = [line for line in result.stdout.strip().splitlines() if line]
            if printed:
                return Path(printed[-1]).resolve()
        sys.stderr.write(result.stderr)
        sys.exit(
            "error: could not resolve the Memar root; pass --root or set MEMAR_ROOT"
        )

    sys.exit("error: no root given; pass --root or set MEMAR_ROOT")


# ------------------------------------------------------------- docs set

def _excluded_from_search(path: Path) -> bool:
    name = path.name
    if any(name.endswith(suffix) for suffix in _SEARCH_EXCLUDED_SUFFIXES):
        return True
    return _RESEARCH_COMPANION.search(name) is not None


def doc_files(root: Path) -> list[Path]:
    docs_dir = root / "docs"
    if not docs_dir.is_dir():
        sys.exit(f"error: no docs directory under {root}")
    return sorted(
        path for path in docs_dir.rglob("*.md") if not _excluded_from_search(path)
    )


# -------------------------------------------------------------- resolve

def resolve_ref(ref: str, root: Path, from_file: Path | None) -> Path:
    anchor_split = re.split(r"[#?]", ref, maxsplit=1)
    clean = anchor_split[0].strip()
    if not clean:
        sys.exit(f"error: reference '{ref}' has no file part")

    windows_drive = len(clean) > 1 and clean[1] == ":"
    if clean.startswith("/") and not windows_drive:
        candidate = root / clean.lstrip("/")
    elif not windows_drive and (clean == "docs" or clean.startswith("docs/")):
        # Root-relative without the leading slash: shell-proof on MSYS,
        # which rewrites leading-`/` arguments.
        candidate = root / clean
    elif clean.startswith("~"):
        candidate = Path(clean).expanduser()
    else:
        base = from_file.parent if from_file else root
        candidate = base / clean
    candidate = candidate.resolve()

    root_resolved = root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        sys.exit(
            f"error: '{ref}' resolves outside the Memar root "
            f"({candidate} vs {root_resolved})"
        )
    if not candidate.is_file():
        sys.exit(
            f"error: '{ref}' -> {candidate} does not exist in this clone; "
            "it may be an unpublished draft — say so instead of guessing"
        )
    return candidate


# ----------------------------------------------------------- extraction

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        sys.exit(f"error: cannot read {path}: {error}")


def front_matter(text: str) -> str | None:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[: end + 4].strip()
    return None


def h1(text: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def abstract(text: str) -> str | None:
    match = re.search(
        r"^##\s+Abstract\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if not match:
        return None
    return match.group(1).strip()


def headings(text: str) -> list[str]:
    pattern = re.compile(r"^(#{2,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
    return [match.group(2).strip() for match in pattern.finditer(text)]


def section(text: str, heading: str) -> str | None:
    pattern = re.compile(r"^(#{2,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    wanted = heading.strip().lower()
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        if title.lower() != wanted:
            continue
        level = len(match.group(1))
        start = match.end()
        end = len(text)
        for later in matches[index + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        return text[start:end].strip()
    return None


# ----------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve, read, and search Memar documentation."
    )
    parser.add_argument("--root", help="Memar repository root", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_path = subparsers.add_parser("path", help="resolve references to absolute paths")
    p_path.add_argument("refs", nargs="+")
    p_path.add_argument(
        "--from", dest="from_file", default=None,
        help="document whose directory relative refs resolve against",
    )

    p_meta = subparsers.add_parser("meta", help="print front matter and Abstract")
    p_meta.add_argument("files", nargs="+")

    p_section = subparsers.add_parser("section", help="print one named section")
    p_section.add_argument("file")
    p_section.add_argument("heading")

    p_search = subparsers.add_parser("search", help="regex search the doc set")
    p_search.add_argument("patterns", nargs="+")

    args = parser.parse_args()
    root = resolve_root(args.root)

    if args.command == "path":
        from_file = None
        if args.from_file:
            from_file = resolve_ref(args.from_file, root, None)
        for ref in args.refs:
            anchor = re.split(r"([#?])", ref, maxsplit=1)
            file_part = anchor[0].strip()
            suffix = "".join(anchor[1:]) if len(anchor) > 1 else ""
            resolved = resolve_ref(file_part, root, from_file)
            line = str(resolved)
            if suffix:
                line += suffix
            print(line)

    elif args.command == "meta":
        for file_ref in args.files:
            path = resolve_ref(file_ref, root, None)
            text = read_text(path)
            print(f"== {path.name} ==")
            fm = front_matter(text)
            if fm:
                print(fm)
            else:
                title = h1(text)
                if title:
                    print(f"# {title}")
            abstr = abstract(text)
            if abstr:
                print(f"\n## Abstract\n{abstr}")
            print()

    elif args.command == "section":
        path = resolve_ref(args.file, root, None)
        text = read_text(path)
        found = section(text, args.heading)
        if found is None:
            available = headings(text)
            sys.exit(
                f"error: no section '{args.heading}' in {path.name}; "
                f"headings: {' | '.join(available)}"
            )
        print(found)

    elif args.command == "search":
        patterns = [re.compile(pattern, re.IGNORECASE) for pattern in args.patterns]
        for path in doc_files(root):
            text = read_text(path)
            if all(pattern.search(text) for pattern in patterns):
                if len(patterns) > 1:
                    print(f"{path.relative_to(root)}:all-matched")
                else:
                    for number, line in enumerate(
                        text.splitlines(), start=1
                    ):
                        if patterns[0].search(line):
                            print(f"{path.relative_to(root)}:{number}:{line.strip()}")


if __name__ == "__main__":
    main()
