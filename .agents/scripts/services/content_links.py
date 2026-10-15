#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_links.py — the links and anchors of a Markdown document judged: headings, citation layers, relative links.

What `memar content check` asks of a document's links, apart from its encoding and the folder walk
(`content_check`): the fragment a heading produces, whether an in-page anchor and a relative link
resolve to a file and a heading, and whether a link points up the layers of the written content
(Documentation -> Citation Direction). These are Memar's own written-surface conventions; whether
they apply to a file is decided by the caller.
"""
from __future__ import annotations

import re
from pathlib import Path

from services.content_markdown import EXTERNAL_LINK, without_code


def anchor_slug(heading: str) -> str:
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


def headings_by_fragment(visible: str, text: str) -> set[str]:
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
        slug = anchor_slug(heading)
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
            cache[key] = headings_by_fragment(without_code(text), text)
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


def link_problems(path: Path, visible: str, cache: dict) -> list[str]:
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


def anchor_problems(visible: str, text: str) -> list[str]:
    """Every in-page link in a Markdown document that names a heading the document lacks."""
    problems: list[str] = []
    if "](#" in visible:
        present = headings_by_fragment(visible, text)
        for match in re.finditer(r"\]\(#([^)]*)\)", visible):
            if match.group(1) not in present:
                problems.append(
                    f"line {text[: match.start()].count(chr(10)) + 1}: in-page "
                    f"anchor #{match.group(1)} has no matching heading in this file"
                )
    return problems
