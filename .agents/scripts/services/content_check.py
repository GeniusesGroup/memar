#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_check.py — `memar content check`: what is wrong with a text file, reported before it is inherited.

Two sets of rules, separated by what they hold for. The encoding and newline
rules hold for every text file in every project, because a shell damages a file
the same way whatever the file is for. Memar's written-surface rules — no blank
line under a heading, no run of blank lines, a link that resolves to a file and
a heading and does not point up the layers of the written content — are Memar's
own conventions and apply only inside a Memar
repository, which is asked of `machine/fs_memar_repository.py` rather than
assumed.

Given a folder it also prints the undischarged propagations its ledgers hold,
apart from the problems and not counted among them: a `Pending` entry is the
correct content of the changelog that holds it, and a gate that is always red
is not a gate.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from services.content_corpus import is_generated
from services.content_markdown import EXTERNAL_LINK, without_code
from services.content_propagation import undischarged_propagations
from services.content_reference import content_root
from services.content_text import plain_path

# The prose rules are Memar's written-surface rules (documentation.md -> Written
# surface) and apply to Markdown only; the encoding and newline rules apply to
# every text file in the tree. The suffixes are the ones this repository is
# actually written in — a tool named for content that refused to check its own
# source would be checking documents and not content.
CHECKED_SUFFIXES = (".md", ".kh", ".py", ".ts", ".json", ".yaml", ".yml", ".txt", ".ps1", ".sh", ".bat", ".cmd")

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


def describe(verbs):
    parser = verbs.add_parser(
        "check",
        help="report encoding, newline, and written-surface problems in text "
             "files; a folder also reports undischarged propagations",
        description="Report what is wrong with text files: a UTF-8 BOM, "
                    "invalid UTF-8, a U+FFFD replacement character, mixed or "
                    "CRLF line endings, a missing final newline, and the "
                    "fingerprints of mojibake; and for Markdown, two blank "
                    "lines in a row, a blank line between a heading and its "
                    "body, an anchor with no matching heading, a relative "
                    "link whose target does not exist, and a relative link "
                    "that points up the citation layers. Given a folder it also "
                    "reports undischarged propagations, printed apart and not "
                    "counted as problems.",
        formatter_class=argparse.HelpFormatter,
    )
    parser.add_argument("files", nargs="+", help="files or folders (any path)")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="also print clean files"
    )
    parser.add_argument(
        "--memar-rules",
        dest="memar_rules",
        action="store_true",
        default=None,
        help="apply Memar's Markdown conventions; the default asks whether the "
             "folder is a Memar repository",
    )
    parser.add_argument(
        "--no-memar-rules",
        dest="memar_rules",
        action="store_false",
        help="apply only the rules that hold for any text file",
    )
    return run


def run(args: argparse.Namespace) -> None:
    cmd_check(args, content_root())


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
            cache[key] = _headings_by_fragment(without_code(text), text)
    return cache[key]


# The layers of Memar's written content, lowest first, as Documentation ->
# Citation Direction names them; that section owns the order and the reasons,
# and this table only maps a path inside a Memar repository onto it.
LAYER_NAMES = (
    "base documents (docs/)",
    "module documents (docs/modules/)",
    "the language (docs/khayyam/)",
    "implementations (bundles/, modules/)",
)


def _repository_of(path: Path, cache: dict) -> Path | None:
    """The Memar repository `path` sits in, asked once per folder per run."""
    from machine.fs_memar_repository import enclosing_repository

    key = ("repository", str(path.parent))
    if key not in cache:
        found = enclosing_repository(path.parent)
        cache[key] = found.resolve() if found is not None else None
    return cache[key]


def citation_layer(path: Path, repository: Path | None) -> int | None:
    """Which layer of Documentation -> Citation Direction `path` belongs to.

    None for a path outside every layer — outside a Memar repository, or a file
    such as the repository's README, CONTRIBUTORS, or `.agents/` — which the
    rule does not judge.
    """
    if repository is None:
        return None
    try:
        parts = path.resolve().relative_to(repository).parts
    except ValueError:
        return None
    if not parts:
        return None
    if parts[0] == "docs":
        return {"khayyam": 2, "modules": 1}.get(parts[1], 0) if len(parts) > 1 else 0
    if parts[0] in ("bundles", "modules"):
        return 3
    return None


def _upward_link_problem(path: Path, file_part: str, line: int, cache: dict) -> str | None:
    """The problem a link from `path` to a higher layer is, or None."""
    repository = _repository_of(path, cache)
    source = citation_layer(path, repository)
    if source is None:
        return None
    target = path.parent / file_part
    higher = citation_layer(target, repository)
    if higher is None or higher <= source:
        return None
    if path.name == "README.md":
        # A folder's README points into its own folder; that is what it is for.
        try:
            target.resolve().relative_to(path.parent.resolve())
            return None
        except ValueError:
            pass
    return (
        f"line {line}: relative link {file_part} points up from "
        f"{LAYER_NAMES[source]} to {LAYER_NAMES[higher]}. A citation runs down "
        "the layers, never up (Documentation -> Citation Direction): name the "
        "higher place in plain text, as a code span holding its path, or move "
        "the content to the layer that may hold it."
    )


def _relative_link_problems(path: Path, visible: str, cache: dict) -> list[str]:
    """Every relative link in a Markdown document that does not resolve, or points up.

    Both halves of a link are checked, because both break the same way and a
    document moved one folder deep takes its links' paths and their anchors with
    it: the file the link names, and the heading inside that file.
    """
    problems: list[str] = []
    for match in re.finditer(r"\]\(([^)\s]+)\)", visible):
        link = match.group(1)
        if EXTERNAL_LINK.match(link):
            continue
        file_part, _, fragment = link.partition("#")
        if not file_part:
            continue  # in-page; the caller's own anchor pass owns it
        if file_part.startswith("/"):
            continue  # site-root, not a path relative to this document
        target = path.parent / file_part
        line = visible[: match.start()].count("\n") + 1
        upward = _upward_link_problem(path, file_part, line, cache)
        if upward:
            problems.append(upward)
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
    `machine/fs_memar_repository.py` whether the folder is a Memar repository.
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
        visible = without_code(text)
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


def checkable_files(folder: Path) -> list[Path]:
    """Every checked file a walk of `folder` should look at.

    A walk is how the tool chooses for itself, so it chooses only what the
    project owns. An installed dependency tree is not this project's work, and a
    report that raises it on every run is a report about the tool, not the tree.
    """
    return [
        path
        for path in sorted(folder.rglob("*"))
        if path.is_file()
        and path.suffix in CHECKED_SUFFIXES
        and not is_generated(path.relative_to(folder).parts[:-1])
    ]


def cmd_check(args: argparse.Namespace, root: Path) -> None:
    from machine.fs_memar_repository import enclosing_repository

    files: list[Path] = []
    directories: list[Path] = []
    for ref in args.files:
        resolved = plain_path(ref)
        if resolved.is_dir():
            directories.append(resolved)
            files.extend(checkable_files(resolved))
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
