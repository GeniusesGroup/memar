#!/usr/bin/env python3
"""memar-documentation.py — resolve, read, and search Memar documentation.

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
  changelog-append FILE  Append one Changelog-facet entry to FILE (must be a
                         `*.changelog.md`). Entry Markdown on stdin, or
                         `--entry-file PATH`. Entry must begin with `### `.
                         Oldest-first rule: always appends at end-of-file;
                         peeks only at the file tail for `---` separator
                         hygiene — does not require reading the changelog
                         into an agent context. See documentation-changelog.md
                         → Structure.
  hour-id                Print whole UTC hours since the Unix epoch — the
                         coarse value used when minting an Explanation-facet
                         document's `ID` field.
  write FILE             Put text into FILE as UTF-8 with **no BOM**, keeping
                         the file's own line endings (LF for a new file) and
                         guaranteeing a final newline. Text on stdin, or
                         `--content-file PATH`. `--create` is required to add
                         a file that does not exist. Any path, not only one
                         inside this repository. This is the way to write a
                         document from a shell; see `check` for why.
  edit FILE              Replace exact text in FILE. `--old`/`--new`, or
                         `--old-file`/`--new-file` when the text is long or
                         contains non-ASCII characters a command line may
                         mangle. Refuses to write when `--old` is absent or
                         occurs more than once (override with `--all`), and
                         removes a BOM if it finds one. Same encoding and
                         newline guarantees as `write`.
  check FILE|DIR...      Report what is wrong with text files: a UTF-8 BOM,
                         invalid UTF-8, a U+FFFD replacement character, mixed
                         or CRLF line endings, a missing final newline, and
                         the fingerprints of mojibake; and for Markdown, two
                         blank lines in a row, a blank line between a heading
                         and its body, an `#anchor` with no matching heading
                         in the document it names — the same one for an
                         in-page link, and the named one for a link to
                         another document — and a relative link whose target
                         does not exist. A directory is walked. Any path, not
                         only one inside this repository. Exits 1 if anything
                         is reported.

Why the write subcommands exist. Reading a file and writing it back is where
a document gets silently damaged, and the damage is invisible until someone
reads a character the round trip destroyed. The mechanism on Windows
PowerShell 5.1 is specific: `Get-Content` has no encoding argument, so it
detects a file's encoding from a byte-order mark and falls back to the console
codepage when there is none. Memar's documents are UTF-8 **without** a BOM —
correctly, since a BOM becomes part of the first line for every tool that
reads the file as text — which is exactly the case that loses. Measured here:
round-tripping a BOM-less UTF-8 file through `Get-Content -Raw` and
`Set-Content -Encoding UTF8` destroys every non-ASCII character, while the
same round trip over a file that had a BOM preserves them. So the rule is not
"PowerShell mangles Unicode" in general; it is that a correctly-encoded
document is the one this shell cannot read.

These subcommands read UTF-8 strictly (an invalid file is an error, never a
silent substitution), write UTF-8 without a BOM, preserve the file's own line
endings rather than the platform's, refuse an empty or ambiguous write, and
offer `check` so damage that already happened is reported instead of
inherited. Use them instead of Get-Content/Set-Content, `echo`, `Out-File`, or
any other shell-level text round trip.

The one thing no script here can do is repair text on its way in. On this
machine a PowerShell 5.1 pipe to a native program, a command-line argument,
and `Out-File` each lose every non-ASCII character, and setting
`$OutputEncoding` or `[Console]::OutputEncoding` first does not recover them —
the loss happens before this process starts. So for text that is not pure
ASCII, pass it as a file (`--content-file`, `--old-file`, `--new-file`) or
write the file with a tool that writes it directly, and reserve stdin for
ASCII. What arrives is what gets written; that is the point of the command,
and it is also its limit.

One more limit, stated plainly because it is why prevention and not detection
is the design: mojibake is still valid UTF-8, so no checker can see all of it.
What survives as a fingerprint is the shape of the mis-decode, and `check`
reports the common patterns as hints rather than as verdicts.

The Memar root is not decided here: `install.py`, in the same folder, is the one
place that reads $MEMAR_ROOT and this script asks it. Only files under the root
and under a `docs` directory are ever returned for
path/meta/section/search/changelog-append. hour-id needs no document root, and
write/edit/check take a plain path of their own.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import install
from memar_repository import enclosing_repository

# Windows consoles default to a legacy codepage (e.g. cp1252) while Memar
# docs are UTF-8; force UTF-8 output so printing content never crashes.
install.use_utf8_stdio()

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


# ------------------------------------------------------------- writing
# Reading and writing a text file from a shell is where a document gets
# silently damaged, and the damage is invisible until someone reads a
# character that a round trip destroyed. The usual culprit is a shell whose
# read and write disagree about encoding: on Windows PowerShell 5.1,
# `Get-Content` decodes with the console codepage and `Set-Content -Encoding
# UTF8` writes a BOM, so a round trip through those two turns every
# non-ASCII character in a document — an em dash, an arrow, a Persian word —
# into mojibake and leaves the file looking perfectly normal.
#
# These three functions are the whole discipline, and the subcommands below
# are the only supported way to put text into a file from a shell:
#
#   * read UTF-8, strictly. Invalid input is an error, never a substitution,
#     because a substitution is how the corruption hides.
#   * write UTF-8 with no BOM. A BOM in a Markdown file is a defect: it
#     becomes part of the first line for every tool that reads the file as
#     text rather than as bytes.
#   * preserve the file's own newline convention instead of the platform's.
#     A document written on one platform and committed from another should
#     not gain or lose line endings.
#   * check the result, so a damage that already happened is reported rather
#     than inherited.

_BOM = "﻿"


def read_utf8_strict(path: Path) -> tuple[str, bool]:
    """Return (text, had_bom). Raises SystemExit on unreadable or non-UTF-8."""
    try:
        raw = path.read_bytes()
    except OSError as error:
        sys.exit(f"error: cannot read {path}: {error}")
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    if had_bom:
        raw = raw[3:]
    try:
        return raw.decode("utf-8"), had_bom
    except UnicodeDecodeError as error:
        sys.exit(
            f"error: {path} is not valid UTF-8 ({error}).\n"
            "  It is not written to, because writing a decoded-with-replacement\n"
            "  copy is how the damage spreads. Recover it from version control,\n"
            "  or convert it deliberately, before editing."
        )


def detect_newline(path: Path) -> str:
    """The file's own line ending, defaulting to LF for a new file."""
    try:
        raw = path.read_bytes()
    except OSError:
        return "\n"
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    if crlf and not lf:
        return "\r\n"
    return "\n"


def write_utf8(path: Path, text: str, newline: str = "\n") -> int:
    """Write text as UTF-8, no BOM, with the given newline. Returns bytes."""
    if newline != "\n":
        text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)
    elif "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text and not text.endswith(newline):
        text += newline
    data = text.encode("utf-8")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            handle.write(data)
    except OSError as error:
        sys.exit(f"error: cannot write {path}: {error}")
    return len(data)


def content_from(args: argparse.Namespace, stdin: str) -> str:
    """The new text, from a file if asked for, else from stdin.

    A file is the only transport that survives non-ASCII text. On Windows
    PowerShell 5.1, a pipe to a native program, a command-line argument, and
    `Out-File` all cross the console codepage on the way out, and a character
    that codepage cannot represent is replaced by `?` or dropped *before* this
    script ever sees it. The document is then written with the loss already
    baked in, and no check on the written file can find it, because the file is
    perfectly valid UTF-8 — it is simply the wrong text. Measured on this
    machine: a here-string piped to this script loses every non-ASCII
    character, and so does one passed as an argument; setting `$OutputEncoding`
    or `[Console]::OutputEncoding` first does not recover it.

    So the order of preference is: a tool that writes the file directly (an
    agent's own file-write, which is not a shell), then `--content-file` when
    the content is already safely on disk, then stdin for ASCII only.
    """
    source = getattr(args, "content_file", None)
    if source:
        try:
            return Path(source).expanduser().read_bytes().decode("utf-8")
        except UnicodeDecodeError as error:
            sys.exit(f"error: --content-file is not valid UTF-8: {error}")
        except OSError as error:
            sys.exit(f"error: cannot read --content-file {source}: {error}")
    return stdin


def refuse_empty(path: Path, text: str, verb: str) -> None:
    """An empty write is almost never meant, and it is not reversible.

    A shell that fails to deliver a here-string, a redirect from a missing file,
    or a pipe that was never connected all look the same to this process: no
    input. Writing that over an existing document empties it, so the refusal is
    the whole point of having this command rather than a shell redirect.
    """
    if not text.strip():
        sys.exit(
            f"error: no text to {verb} {path.name}. Nothing was written.\n"
            "  Empty input usually means the pipe or redirect delivered nothing,\n"
            "  not that the file should be emptied. Pass the text on stdin, or\n"
            "  use --content-file PATH."
        )


def changelog_append(path: Path, entry: str) -> None:
    """Append one Changelog entry at EOF (oldest-first). Peeks only the tail."""
    if path.suffixes[-2:] != [".changelog", ".md"] and not path.name.endswith(
        ".changelog.md"
    ):
        # Accept both Path("x.changelog.md") forms across platforms.
        if not path.name.endswith(".changelog.md"):
            sys.exit(
                f"error: changelog-append expects a *.changelog.md path, got {path.name}"
            )
    entry = entry.strip()
    if not entry.startswith("### "):
        sys.exit("error: changelog entry must begin with '### ' (an entry title)")

    if not path.is_file():
        sys.exit(f"error: not a file: {path}")

    # Peek at most the last 512 bytes for separator hygiene — never load the
    # whole changelog into memory for an append.
    size = path.stat().st_size
    with path.open("rb") as handle:
        handle.seek(max(0, size - 512))
        tail = handle.read().decode("utf-8", errors="replace")
    tail_stripped = tail.rstrip()
    needs_rule = not tail_stripped.endswith("---")

    parts: list[str] = []
    if size > 0 and not tail.endswith("\n"):
        parts.append("\n")
    if needs_rule:
        if size > 0 and not tail_stripped.endswith("\n\n"):
            if not tail.endswith("\n"):
                parts.append("\n")
            parts.append("\n")
        parts.append("---\n\n")
    elif size > 0 and not tail.endswith("\n\n"):
        if tail.endswith("\n"):
            parts.append("\n")
        else:
            parts.append("\n\n")
    parts.append(entry)
    parts.append("\n")

    # The file's own convention, not this machine's. Appending with a fixed one
    # is how a changelog that held CRLF for a year gains an LF tail from the
    # first append made on a host whose default differs — and `check` then
    # reports mixed line endings on the tool the documentation tells every
    # contributor to append with. The entry is normalized first so that a
    # contributor's CRLF does not survive as a stray CR inside an LF file.
    entry_text = "".join(parts).replace("\r\n", "\n").replace("\r", "\n")
    newline = detect_newline(path) if size else "\n"
    if newline != "\n":
        entry_text = entry_text.replace("\n", newline)
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(entry_text)


# ----------------------------------------------------------------- commands
# One function per subcommand, so the command's own behaviour is read in one
# place and `main` below is only the parser and the dispatch.


def cmd_path(args: argparse.Namespace, root: Path) -> None:
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


def cmd_meta(args: argparse.Namespace, root: Path) -> None:
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


def cmd_section(args: argparse.Namespace, root: Path) -> None:
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


def cmd_search(args: argparse.Namespace, root: Path) -> None:
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in args.patterns]
    for path in doc_files(root):
        text = read_text(path)
        if all(pattern.search(text) for pattern in patterns):
            if len(patterns) > 1:
                print(f"{path.relative_to(root)}:all-matched")
            else:
                for number, line in enumerate(text.splitlines(), start=1):
                    if patterns[0].search(line):
                        print(f"{path.relative_to(root)}:{number}:{line.strip()}")


def cmd_changelog_append(args: argparse.Namespace, root: Path) -> None:
    path = resolve_ref(args.file, root, None)
    if args.entry_file:
        entry = Path(args.entry_file).expanduser().read_text(encoding="utf-8")
    else:
        entry = sys.stdin.read()
    changelog_append(path, entry)
    print(f"appended to {path}")


def cmd_hour_id() -> None:
    print(int(time.time() // 3600))


def cmd_root(args: argparse.Namespace, root: Path) -> None:
    """Print where Memar is, and nothing else.

    A program that needs to find Memar has three ways to learn where it is, and
    this is the one that survives all of them. A recorded environment variable
    answers only when the program was started after the install and after the
    shell read it; a path typed into a configuration answers only while that
    configuration is intact. Asking the installed command answers by definition,
    because the command is the thing installed — the same reason `go env GOROOT`
    is how a program asks a Go toolchain where it lives rather than reading a
    variable the toolchain also writes.

    One line on stdout and nothing else, so it can be captured by substitution
    without parsing. A caller that wants prose asks a person; a caller that wants
    a path wants the path.
    """
    print(root)


# ------------------------------------------------------------ write commands


def _plain_path(ref: str) -> Path:
    """A path for a file operation, not for documentation navigation.

    `resolve_ref` is the right answer when a reference comes from a document and
    must stay inside the Memar repository. Writing, editing, and checking a file
    are operations on a path the caller states outright, so they are resolved
    against the current directory and are not confined to the repository — a
    round trip that mangles a file does not care which repository it is in.
    """
    return Path(ref).expanduser().resolve()


def cmd_write(args: argparse.Namespace, root: Path) -> None:
    path = _plain_path(args.file)
    if not path.is_file() and not args.create:
        sys.exit(
            f"error: {path} does not exist. Nothing was written.\n"
            "  Pass --create if you mean to add a new file. A mistyped path in a\n"
            "  write would otherwise leave a stray file with no complaint."
        )
    text = content_from(args, sys.stdin.read())
    refuse_empty(path, text, "write")
    newline = args.newline or detect_newline(path)
    existed = path.is_file()
    if existed:
        _, had_bom = read_utf8_strict(path)
        if had_bom:
            print(f"note: {path.name} had a BOM; the write removes it")
    size = write_utf8(path, text, newline)
    verb = "rewrote" if existed else "wrote"
    print(f"{verb} {path} ({size} bytes, utf-8, no BOM, {newline!r} newlines)")


def cmd_edit(args: argparse.Namespace, root: Path) -> None:
    path = _plain_path(args.file)
    if not path.is_file():
        sys.exit(f"error: not a file: {path}")
    text, had_bom = read_utf8_strict(path)
    old = (
        Path(args.old_file).expanduser().read_bytes().decode("utf-8")
        if args.old_file
        else args.old
    )
    new = (
        Path(args.new_file).expanduser().read_bytes().decode("utf-8")
        if args.new_file
        else args.new
    )
    if old == "":
        sys.exit("error: --old must not be empty; it would match everywhere")
    found = text.count(old)
    if found == 0:
        sys.exit(
            f"error: --old does not occur in {path.name}. Nothing was written.\n"
            "  Check the exact text, including line endings and any dash character."
        )
    if found > 1 and not args.all:
        sys.exit(
            f"error: --old occurs {found} times in {path.name}. Nothing was written.\n"
            "  Give more surrounding context to make it unique, or pass --all."
        )
    if had_bom:
        print(f"note: {path.name} had a BOM; the write removes it")
    newline = args.newline or detect_newline(path)
    write_utf8(path, text.replace(old, new), newline)
    print(f"edited {path} ({found} replacement{'s' if found > 1 else ''})")


# ------------------------------------------------------------- inspection

# The prose rules are Memar's written-surface rules (documentation.md -> Written
# surface) and apply to Markdown only; the encoding and newline rules apply to
# every text file in the tree.
_CHECKED_SUFFIXES = (".md", ".kh", ".py", ".ts", ".json", ".yaml", ".yml", ".txt", ".ps1", ".sh", ".bat")

# Mojibake left behind by a read/write round trip through a codepage that is
# not UTF-8 is still *valid* UTF-8, so nothing above can see it: the bytes were
# decoded wrongly and re-encoded faithfully. What survives as a fingerprint is
# the shape of the damage — a Latin-1 letter followed by a character that only
# the mis-decode could have produced. These are reported as hints rather than
# verdicts, because a few of the leading letters are real letters in real
# languages (Romanian and Welsh write "Â", Icelandic and Yoruba write "Ù"), and
# only the pair is telling. They are worth reporting precisely because the
# damage is otherwise invisible.
_MOJIBAKE_HINTS = (
    ("\u00e2\u20ac", "U+2014 em dash, U+201C/D quotes, U+2019 apostrophe, U+2022, U+2122"),
    ("\u00e2\u201e", "U+2192 arrow and the U+2000 block (typographic punctuation)"),
    ("\u00f0\u0178", "any character above U+1F000, such as an emoji"),
    ("\u00c2\u00ab", "U+00AB guillemet"),
    ("\u00c2\u00bb", "U+00BB guillemet"),
    ("\u00c2\u00b7", "U+00B7 middle dot"),
    ("\u00d9\u201e", "U+06xx Arabic and Persian, e.g. Persian text"),
    ("\u00d9\u0085", "U+06xx Arabic and Persian"),
    ("\u00d1\u0085", "U+0300-U+03FF combining marks and Greek"),
)


def _mojibake_hints(text: str) -> list[str]:
    hits: list[str] = []
    for marker, source in _MOJIBAKE_HINTS:
        if marker in text:
            count = text.count(marker)
            hits.append(
                f"{count} occurrence{'s' if count > 1 else ''} of "
                f"{marker!r}, the signature of {source} having been decoded "
                f"as Latin-1 and re-encoded — a shell read/write round trip, "
                f"not the file's own text (a hint; the leading letter is a real "
                f"letter in some languages, so judge before acting)"
            )
    return hits


def _anchor_slug(heading: str) -> str:
    """The fragment a Markdown heading produces, as GitHub and most renderers make it."""
    slug = re.sub(r"`([^`]*)`", r"\1", heading)
    slug = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", slug)
    # `*` and `~` are emphasis markers and go; `_` is not punctuation to a
    # renderer, so `The agent_for Relationship` must slug to
    # `the-agent_for-relationship` and not to `the-agentfor-relationship`.
    slug = re.sub(r"[*~]", "", slug)
    slug = re.sub(r"[^\w\s-]", "", slug.lower())
    # Each whitespace character becomes its own hyphen, not each run of them: a
    # heading whose punctuation was just dropped leaves two spaces where the
    # punctuation stood, and `Scope - Type` must slug to `scope--type`. A run
    # collapses to one hyphen here and every such link reads as broken.
    return re.sub(r"\s", "-", slug.strip())


def _headings_by_fragment(visible: str, text: str) -> set[str]:
    """Every fragment a heading produces, disambiguators included.

    Which lines are headings is read from `visible`, so a `#` inside a fenced
    block is not one; each such line's fragment is then taken from `text`, since
    a heading's own code span is part of its text and only its backticks go.

    Two headings that slug alike get GitHub's suffix on the second and later
    ones, so a document with two `## LLM Wiki` sections answers to
    `llm-wiki` and `llm-wiki-1`; a set of slugs alone knows only the first.
    """
    seen: dict[str, int] = {}
    fragments = set()
    raw_lines = text.split("\n")
    for number, line in enumerate(visible.split("\n")):
        match = re.fullmatch(r"#{1,6}\s+(.*?)\s*#*\s*", line)
        if not match:
            continue
        heading = raw_lines[number] if number < len(raw_lines) else match.group(1)
        heading = re.sub(r"^#{1,6}\s+", "", heading).rstrip()
        slug = _anchor_slug(heading)
        if not slug:
            continue
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        fragments.add(slug if count == 0 else f"{slug}-{count}")
    return fragments


def _without_code(text: str) -> str:
    """`text` with the inside of code spans and fenced blocks blanked out.

    Offsets and line breaks are preserved, so a position in the result is the
    same position in the original. A `](#x)` written inside backticks is text
    about links, not a link, and a `# comment` inside a fence is not a heading;
    neither may be read as either.
    """
    def blank(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    fenced = re.compile(r"(?ms)^(```|~~~).*?^\1[ \t]*$")
    spans = re.compile(r"(?s)(`+)(?:(?!\1).)*?\1")
    return spans.sub(blank, fenced.sub(blank, text))


# A link this checker cannot judge by looking at the filesystem: a URI with a
# scheme (`https:`, `mailto:`) and a protocol-relative `//host/path`. A leading
# `/` is a site-root reference, which resolves against a server rather than
# against the document's own folder, so it is not a file this run can see.
_EXTERNAL_LINK = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)


def _fragments_of(path: Path, cache: dict[str, set[str] | None]) -> set[str] | None:
    """Every heading fragment `path` answers to, or None when it cannot be read.

    Cached per run because a doc set links to the same governing documents
    hundreds of times, and a checker that re-reads each of them per link turns a
    whole-tree run into hundreds of redundant reads. None rather than an empty
    set when the read fails, so an unreadable target is not reported as a
    document whose headings happen to be missing.
    """
    key = str(path)
    if key not in cache:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            cache[key] = None
        else:
            cache[key] = _headings_by_fragment(_without_code(text), text)
    return cache[key]


def _relative_link_problems(path: Path, visible: str, cache: dict) -> list[str]:
    """Every relative link in a Markdown document that does not resolve.

    Both halves of a link are checked, because both break the same way and a
    document moved one folder deep takes its links' paths and their anchors with
    it: the file the link names, and the heading inside that file.
    """
    problems: list[str] = []
    for match in re.finditer(r"\]\(([^)\s]+)\)", visible):
        link = match.group(1)
        if _EXTERNAL_LINK.match(link):
            continue
        file_part, _, fragment = link.partition("#")
        if not file_part:
            continue  # in-page; the caller's own anchor pass owns it
        if file_part.startswith("/"):
            continue  # site-root, not a path relative to this document
        target = path.parent / file_part
        line = visible[: match.start()].count("\n") + 1
        if not target.exists():
            problems.append(
                f"line {line}: relative link {file_part} does not exist. A link "
                "to a document that is not there cannot be followed, and moving "
                "a document is what breaks one silently: nothing about the "
                "link changes, only the folder it was written from."
            )
            continue
        if not fragment or not target.is_file() or target.suffix.lower() != ".md":
            continue
        present = _fragments_of(target, cache)
        if present is not None and fragment not in present:
            problems.append(
                f"line {line}: relative link {link} names no heading in "
                f"{file_part}. The file is there and the anchor is not, so a "
                "reader lands on the document rather than on the part of it "
                "the link was written to point at."
            )
    return problems


# ------------------------------------------- obligations, not defects

# A changelog entry's `Propagates to` field names another artifact and the state
# of the work the change implies there (documentation-changelog.md -> Propagates
# to). `Pending` is the one open state; `Done` and `Rejected` are closed, and
# `Rejected` is closed permanently. Nothing in this script reported the open
# ones: `search` excludes changelog files, because their content is history
# rather than current truth, which is right for concept search and leaves the
# work-list with no surface at all.
#
# The state is read from the entry's own field — the first segment after the
# artifact's colon — so a sentence that mentions `Pending` while describing
# something else is not read as an obligation. `Pending deletion` and `Pending
# at absorb time` are how the sources write the same state, and both are open.
_PROPAGATION_OPEN = re.compile(
    r"(?m)^[ \t]*[-*][ \t]+\S.*?:[ \t]*Pending(?![A-Za-z])"
)

# A ledger is named `<base>.changelog.md`, so its stem ends in `.changelog`. The
# document that *specifies* the facet is named `documentation-changelog.md` and
# shows the same section headings, the same `Propagates to` example, and the
# same field names — testing on `endswith(".changelog.md")` reads that
# specification as a ledger full of obligations.
def _is_changelog_ledger(path: Path) -> bool:
    return path.stem.endswith(".changelog")

# A rejected alternative's home is the `Considered and not done` section of a
# changelog entry, and whether a body holds such a record is deliberately not
# checked here. It is not a question about text: `documentation-changelog.md` is
# the document that specifies the field, so it carries a section by that name in
# its own body, and the specification of where records go differs from a record
# only in what the text is for. Any threshold that separates them — heading
# depth, a bullet beside the heading, the file's name — fires on the project's
# own governing document or misses a record written the other way, and a check
# that stands permanently red on a correct file is one a reader learns to skip.
# The hazard the rule addresses is real and named at
# documentation-explanation.md -> Relevance discipline; it is answered by
# writing the record in the changelog, not by a pattern.


def undischarged_propagations(paths: list[Path]) -> list[tuple[Path, int, str]]:
    """Every `Propagates to` entry left `Pending`, as (file, line, report).

    Changelog files only, since that is where the field is defined. Returns
    rather than raises: a `Pending` entry is correct content of the file that
    holds it, so this is a work-list and not a defect, and a caller that counts
    defects must not count these.
    """
    found: list[tuple[Path, int, str]] = []
    for path in paths:
        if path.suffix.lower() != ".md" or not _is_changelog_ledger(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        visible = _without_code(text)
        for match in _PROPAGATION_OPEN.finditer(visible):
            line = visible[: match.start()].count("\n") + 1
            artifact = match.group(0).lstrip(" \t-*").rstrip()
            found.append((path, line, f"{path.name} {line}: {artifact} — not yet done"))
    return found


def check_file(
    path: Path,
    link_cache: dict | None = None,
    memar_rules: bool = True,
) -> list[str]:
    """Report what is wrong with a text file. Empty list means clean.

    `memar_rules` decides whether the Markdown rules are applied at all. They are
    Memar's own conventions — no blank line under a heading, linear load-bearing
    logic, a relative link that resolves — and a file in a project that has not
    adopted Memar is not a Memar document, so a missing blank line there is not a
    defect and reporting it tells the owner their repository is wrong for a
    reason they never agreed to. The encoding and newline rules are different:
    they hold for every text file in every project, because a shell damages a
    file the same way whatever the file is for. So the two sets are separated by
    a flag rather than by a list, and the caller decides by asking
    `memar_repository` whether the folder is a Memar repository.
    """
    cache: dict = {} if link_cache is None else link_cache
    problems: list[str] = []
    try:
        raw = path.read_bytes()
    except OSError as error:
        return [f"unreadable: {error}"]
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("line 1: UTF-8 BOM present; every tool that reads this "
                        "as text sees the BOM as content")
    try:
        text = raw[3:].decode("utf-8") if raw.startswith(b"\xef\xbb\xbf") else raw.decode("utf-8")
    except UnicodeDecodeError as error:
        problems.append(f"not valid UTF-8 ({error}); a tool that decodes with "
                        "replacement characters has already lost the original")
        return problems
    if not raw:
        problems.append("file is empty")

    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    if crlf and lf:
        problems.append(
            f"mixed line endings: {crlf} CRLF and {lf} LF. A file that already "
            "holds one convention will gain the other the first time a tool "
            "writes it with the other, which is how a diff stops being readable."
        )
    if text and not text.endswith("\n"):
        problems.append("no newline at end of file")

    for number, line in enumerate(text.split("\n"), start=1):
        if "\ufffd" in line:
            problems.append(
                f"line {number}: U+FFFD replacement character — a tool decoded this "
                "file with errors replaced instead of failing, so the original "
                "characters are already gone"
            )
    for hint in _mojibake_hints(text):
        problems.append("likely mojibake: " + hint)
    if path.suffix == ".md" and memar_rules:
        if re.search(r"\n\s*\n\s*\n", text):
            match = re.search(r"\n\s*\n\s*\n", text)
            problems.append(
                f"line {text[: match.start()].count(chr(10)) + 1}: two or more "
                "blank lines in a row"
            )
        blank_after = re.search(r"(?m)^#{1,6} .*\n[ \t]*\n(?=[ \t]*\n|[ \t]*\S)", text)
        if blank_after:
            rest = text[blank_after.end() :].lstrip("\n \t")
            # A section whose body is another section opens with a heading and no
            # prose of its own; the blank line there carries no paragraph break,
            # which is the case the written-surface rule is about.
            if not rest.startswith("#"):
                problems.append(
                    f"line {text[: blank_after.start()].count(chr(10)) + 1}: blank "
                    "line between a heading and its body"
                )
        visible = _without_code(text)
        if "](#" in visible:
            present = _headings_by_fragment(visible, text)
            for match in re.finditer(r"\]\(#([^)]*)\)", visible):
                if match.group(1) not in present:
                    problems.append(
                        f"line {text[: match.start()].count(chr(10)) + 1}: in-page "
                        f"anchor #{match.group(1)} has no matching heading in this file"
                    )
        problems.extend(_relative_link_problems(path, visible, cache))
    return problems


def cmd_check(args: argparse.Namespace, root: Path) -> None:
    files: list[Path] = []
    directories: list[Path] = []
    for ref in args.files:
        resolved = _plain_path(ref)
        if resolved.is_dir():
            directories.append(resolved)
            files.extend(
                p for p in sorted(resolved.rglob("*"))
                if p.is_file() and p.suffix in _CHECKED_SUFFIXES
            )
        else:
            files.append(resolved)
    total = 0
    link_cache: dict = {}
    # Whether Memar's own Markdown conventions apply is a fact about the folder,
    # asked through the module that holds the test rather than assumed from the
    # caller: Memar checks a consuming project as a project, not as a set of
    # documents that failed to become Memar documents.
    memar_rules = args.memar_rules
    if memar_rules is None:
        memar_rules = enclosing_repository(
            directories[0] if directories else files[0]
        ) is not None
    for path in files:
        problems = check_file(path, link_cache, memar_rules)
        total += len(problems)
        try:
            shown = path.relative_to(root)
        except ValueError:
            shown = path
        if not problems:
            if args.verbose:
                print(f"ok    {shown}")
        else:
            print(f"{shown}:")
            for problem in problems:
                print(f"  - {problem}")
    # Reported apart from the problems, and only when a folder was named: the
    # state lives in the files a walk already collected, and a `Pending` entry
    # is the correct content of the changelog that holds it. Counting it as a
    # defect would make every routine run red on work that predates the run, and
    # a gate that is always red is not a gate.
    outstanding: list[tuple[Path, int, str]] = []
    if directories:
        outstanding = undischarged_propagations(files)
    if outstanding:
        print("\nundischarged propagations:")
        for _, _, report in outstanding:
            print(f"  - {report}")
    print(
        f"\nchecked {len(files)} file{'s' if len(files) != 1 else ''}, "
        f"{total} problem{'s' if total != 1 else ''}"
        + (
            f", {len(outstanding)} undischarged propagation"
            f"{'s' if len(outstanding) != 1 else ''}"
            if outstanding
            else ""
        )
    )
    if not memar_rules:
        print(
            "not a Memar repository, so Memar's Markdown conventions were not "
            "applied: encoding, newlines, and decoding damage only"
        )
    if total:
        raise SystemExit(1)


# ----------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve, read, and search Memar documentation."
    )
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

    p_append = subparsers.add_parser(
        "changelog-append",
        help="append one oldest-first Changelog entry at end-of-file",
    )
    p_append.add_argument("file", help="path to a *.changelog.md")
    p_append.add_argument(
        "--entry-file",
        default=None,
        help="read entry Markdown from this file instead of stdin",
    )

    subparsers.add_parser(
        "hour-id",
        help="print UTC hour-count since epoch (Explanation document ID)",
    )

    subparsers.add_parser(
        "root",
        help="print where Memar is installed, for a program that needs to find it",
    )

    p_write = subparsers.add_parser(
        "write",
        help="write a text file as UTF-8 without a BOM, preserving its newlines",
    )
    p_write.add_argument("file", help="path to write (any path, not only in this repo)")
    p_write.add_argument(
        "--content-file",
        default=None,
        help="read the new text from this file instead of stdin",
    )
    p_write.add_argument(
        "--newline",
        choices=["lf", "crlf"],
        default=None,
        help="line ending; default is the file's own, or LF for a new file",
    )
    p_write.add_argument(
        "--create",
        action="store_true",
        help="required to create a file that does not exist yet",
    )

    p_edit = subparsers.add_parser(
        "edit",
        help="replace exact text in a file, refusing an absent or ambiguous match",
    )
    p_edit.add_argument("file", help="path to edit (any path, not only in this repo)")
    p_edit.add_argument("--old", default=None, help="text to replace")
    p_edit.add_argument(
        "--old-file", default=None, help="read the text to replace from this file"
    )
    p_edit.add_argument("--new", default=None, help="replacement text")
    p_edit.add_argument(
        "--new-file", default=None, help="read the replacement from this file"
    )
    p_edit.add_argument(
        "--all", action="store_true", help="replace every occurrence, not only a unique one"
    )
    p_edit.add_argument("--newline", choices=["lf", "crlf"], default=None)

    p_check = subparsers.add_parser(
        "check",
        help="report encoding, newline, and written-surface problems in text "
             "files; a folder also reports undischarged propagations",
    )
    p_check.add_argument("files", nargs="+", help="files or folders (any path)")
    p_check.add_argument(
        "-v", "--verbose", action="store_true", help="also print clean files"
    )
    p_check.add_argument(
        "--memar-rules",
        dest="memar_rules",
        action="store_true",
        default=None,
        help="apply Memar's Markdown conventions; the default asks whether the "
             "folder is a Memar repository",
    )
    p_check.add_argument(
        "--no-memar-rules",
        dest="memar_rules",
        action="store_false",
        help="apply only the rules that hold for any text file",
    )

    args = parser.parse_args()
    # hour-id asks the clock, not the doc set, so it needs no root: a session
    # that has not installed Memar can still mint a document ID.
    if args.command == "hour-id":
        cmd_hour_id()
        return

    root = install.resolve_root_or_here()

    if args.command == "path":
        cmd_path(args, root)
    elif args.command == "root":
        cmd_root(args, root)
    elif args.command == "meta":
        cmd_meta(args, root)
    elif args.command == "section":
        cmd_section(args, root)
    elif args.command == "search":
        cmd_search(args, root)
    elif args.command == "changelog-append":
        cmd_changelog_append(args, root)
    elif args.command == "write":
        cmd_write(args, root)
    elif args.command == "edit":
        if args.old is None and args.old_file is None:
            sys.exit("error: edit needs --old or --old-file")
        if args.new is None and args.new_file is None:
            sys.exit("error: edit needs --new or --new-file")
        cmd_edit(args, root)
    elif args.command == "check":
        cmd_check(args, root)


if __name__ == "__main__":
    main()
