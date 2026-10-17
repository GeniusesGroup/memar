#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_check.py — `memar content check`: what is wrong with a text file, reported before it is inherited.

Two sets of rules, separated by what they hold for. The encoding and newline
rules hold for every text file in every project, because a shell damages a file
the same way whatever the file is for. Memar's written-surface rules — no blank
line under a heading, no run of blank lines, a link that resolves to a file and
a heading — are Memar's own conventions and apply only inside a Memar
repository, which is asked of `machine/fs_memar_repository.py` rather than
assumed.

Given a folder it also prints the undischarged propagations its ledgers hold,
apart from the problems and not counted among them: a `Pending` entry is the
correct content of the changelog that holds it, and a gate that is always red
is not a gate. A link that points up the layers of the written content is a
warning for the same kind of reason: it is a debt, repaid when its text is
upgraded, and never a defect a link is deleted to clear.

The links and anchors of a Markdown document are judged in `content_links`, and
a normative-references list's entries in `normative_references_check`; this file
holds the encoding and newline rules, the folder walk, and the report.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from services.content_corpus import is_generated
from services.content_links import anchor_problems, link_problems, upward_link_warnings
from services.content_markdown import without_code
from services.content_owed import owed_hints
from services.content_propagation import undischarged_propagations
from services.content_questions_lint import entry_warnings
from services.content_reference import content_root
from services.content_text import plain_path
from services.normative_references_check import is_declared, list_drops, list_problems, list_warnings

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
                    "link, or a root-relative one (/docs/...) resolved as "
                    "`memar content path` resolves it, whose file or heading "
                    "does not exist; and for a normative-references list in "
                    ".agents/scripts/rules/normative_references/, or in a "
                    "folder the `normative_references` preference of the "
                    "project it lies in names, a word that "
                    "names no kind, an entry whose link names no Markdown file "
                    "of the repository or is root-relative, a missing review "
                    "mark or one that differs from its section's hash now, "
                    "a drop that drops nothing or has no reason, and a "
                    "project's drop of an every-act section, which is "
                    "refused; the summary line counts the passages of Memar "
                    "a project's lists drop. A relative link that "
                    "points up the citation layers, an Open Questions entry "
                    "missing a field, a file named like a list outside the "
                    "declared places, and one passage twice in a list, are "
                    "printed apart as warnings; given a "
                    "folder it also reports undischarged propagations. Neither "
                    "is counted as a problem.",
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


def _is_link_stand_in(path: Path, raw: bytes) -> bool:
    """Whether PATH is a folder's README that git records as a symlink, as a checkout without symlink support writes it.

    Such a checkout writes the link as a text file holding its target path and
    nothing else, with no final newline: that is the file's whole content by
    design (Documentation Practice, Folder READMEs), and the link's target is
    the document the checks judge. A real symlink is read through to its
    target, so it needs no stand-in rule. Only a README is read this way, only
    when its single line names an existing file beside it.
    """
    if path.name != "README.md" or path.is_symlink():
        return False
    target = raw.decode("utf-8", errors="replace").strip()
    return bool(target) and "\n" not in target and not any(c.isspace() for c in target) and (path.parent / target).is_file()


def check_file(
    path: Path,
    link_cache: dict | None = None,
    memar_rules: bool = True,
    *,
    root: Path,
) -> list[str]:
    """Report what is wrong with a text file. Empty list means clean.

    `root` is the checkout a root-relative link (`/docs/...`) resolves under,
    the one `memar content path` resolves against.

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
    if _is_link_stand_in(path, raw):
        return []
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
        problems.extend(anchor_problems(visible, text))
        problems.extend(link_problems(path, visible, cache, root))
    if path.suffix == ".md":
        problems.extend(list_problems(path, root))
    return problems


def upward_warnings(path: Path, link_cache: dict | None = None) -> list[str]:
    """Every link in a Markdown document that points up the citation layers.

    A warning and not a problem (Documentation -> Citation Direction): an
    upward link is a debt, and a link is never deleted to comply.
    """
    if path.suffix != ".md":
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # check_file reports the read itself
    cache: dict = {} if link_cache is None else link_cache
    return upward_link_warnings(path, without_code(text), cache)


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
        problems = check_file(path, link_cache, memar_rules, root=root)
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
    # An Open Questions entry missing a field is a warning for the same reason:
    # entries written before the rule stay valid, and only a Memar repository
    # has adopted the rule. An upward link is one too: a debt repaid when its
    # text is upgraded, never by deleting the link.
    warnings: list[str] = []
    if memar_rules:
        for path in files:
            try:
                shown = path.relative_to(root)
            except ValueError:
                shown = path
            if path.name.endswith(".handoff.md"):
                warnings.extend(f"{shown}:{text.removeprefix('line ')}" for text in entry_warnings(path))
            warnings.extend(f"{shown}:{text.removeprefix('line ')}" for text in upward_warnings(path, link_cache))
            if path.suffix == ".md":
                warnings.extend(f"{shown}: {text}" for text in list_warnings(path, root))
    else:
        # A project's list is judged where its project declares it, whether or not the project is a Memar repository.
        for path in files:
            if path.suffix == ".md" and is_declared(path, root):
                warnings.extend(f"{path}: {text}" for text in list_warnings(path, root))
    if warnings:
        print("\nwarnings (not counted as problems):")
        for warning in warnings:
            print(f"  - {warning}")
    # Owed marks found on one side only are hints for the same reason: a
    # document may owe work no Test can execute, and a Test may be pending for
    # a claim not yet written. Only identifiers are read; no path is opened.
    if directories and memar_rules:
        hints = owed_hints(files)
        if hints:
            print("\nowed marks on one side only (hints, not counted as problems):")
            for hint in hints:
                print(f"  - {hint}")
    dropped = sum(list_drops(path, root) for path in files if path.suffix == ".md")
    print(
        f"\nchecked {len(files)} file{'s' if len(files) != 1 else ''}, "
        f"{total} problem{'s' if total != 1 else ''}"
        + (
            f", {len(outstanding)} undischarged propagation"
            f"{'s' if len(outstanding) != 1 else ''}"
            if outstanding
            else ""
        )
        + (f", {len(warnings)} warning{'s' if len(warnings) != 1 else ''}" if warnings else "")
        + (f", {dropped} passage{'s' if dropped != 1 else ''} of Memar dropped by this project's lists" if dropped else "")
    )
    if not memar_rules:
        print(
            "not a Memar repository, so Memar's Markdown conventions were not "
            "applied: encoding, newlines, and decoding damage only"
        )
    if total:
        raise SystemExit(1)
