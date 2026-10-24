#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/codec/markdown/services/links.py — the links and anchors of a Markdown document judged: headings, citation layers, relative links.

What `memar content check` asks of a document's links, apart from its encoding and the folder walk
(`content_check`): the fragment a heading produces, whether an in-page anchor and a relative or
root-relative link resolve to a file and a heading, and whether a link points up the layers of the written content
(Documentation -> Citation Direction), which is a warning rather than a problem. These are Memar's own written-surface conventions; whether
they apply to a file is decided by the caller.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar_repository = plugable_load('computer.filesystem.services.fs_memar_repository')
enclosing_repository = _m_fs_memar_repository.enclosing_repository
import re
from pathlib import Path
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
EXTERNAL_LINK = _m_markdown.EXTERNAL_LINK
without_code = _m_markdown.without_code
from modules.knowledge.content.services.reference import under_root

def anchor_slug(heading: str) -> str:
    """The fragment a Markdown heading produces, as GitHub and most renderers make it."""
    slug = re.sub('`([^`]*)`', '\\1', heading)
    slug = re.sub('\\[([^\\]]*)\\]\\([^)]*\\)', '\\1', slug)
    slug = re.sub('[*~]', '', slug)
    slug = re.sub('[^\\w\\s-]', '', slug.lower())
    return re.sub('\\s', '-', slug.strip())

def headings_by_fragment(visible: str, text: str) -> set[str]:
    """Every fragment a heading produces, disambiguators included.

    Which lines are headings is read from `visible`, so a `#` inside a fenced
    block is not one; each such line's fragment is then taken from `text`, since
    a heading's own code span is part of its text and only its backticks go.

    Two headings that slug alike get GitHub's suffix on the second and later
    ones, so a document with two `## LLM Wiki` sections answers to
    `llm-wiki` and `llm-wiki-1`; a set of slugs alone knows only the first.
    """
    slugs = []
    raw_lines = text.split('\n')
    for number, line in enumerate(visible.split('\n')):
        match = re.fullmatch('#{1,6}\\s+(.*?)\\s*#*\\s*', line)
        if not match:
            continue
        heading = raw_lines[number] if number < len(raw_lines) else match.group(1)
        slugs.append(anchor_slug(re.sub('^#{1,6}\\s+', '', heading).rstrip()))
    return {fragment for fragment in fragments(slugs) if fragment}

def fragments(slugs: list[str]) -> list[str]:
    """The fragment each heading answers to, in document order, from the slugs of every heading of every level:
    GitHub's `-N` suffix on a slug's Nth repeat; an empty slug answers to no fragment ("") and is not counted."""
    seen: dict[str, int] = {}
    answers = []
    for slug in slugs:
        count = seen.get(slug, 0)
        seen[slug] = count + 1 if slug else 0
        answers.append(slug if not slug or count == 0 else f'{slug}-{count}')
    return answers

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
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            cache[key] = None
        else:
            cache[key] = headings_by_fragment(without_code(text), text)
    return cache[key]
LAYER_NAMES = ('the base (docs/)', 'the modules (modules/, bundles/)')

def _repository_of(path: Path, cache: dict) -> Path | None:
    """The Memar repository `path` sits in, asked once per folder per run."""
    key = ('repository', str(path.parent))
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
    if parts[0] == 'docs':
        return 0
    if parts[0] in ('bundles', 'modules', 'modules-plugable'):
        return 1
    return None

def _upward_link_warning(path: Path, file_part: str, line: int, cache: dict) -> str | None:
    """The warning a link from `path` to a higher layer is, or None.

    A warning and never a problem: an upward link is a debt, repaid when the
    text is upgraded to name the concept, and a link is never deleted to comply
    (Documentation -> Citation Direction).
    """
    repository = _repository_of(path, cache)
    source = citation_layer(path, repository)
    if source is None:
        return None
    target = path.parent / file_part
    higher = citation_layer(target, repository)
    if higher is None or higher <= source:
        return None
    if path.name == 'README.md':
        try:
            target.resolve().relative_to(path.parent.resolve())
            return None
        except ValueError:
            pass
    return f"line {line}: relative link {file_part} points up from {LAYER_NAMES[source]} to {LAYER_NAMES[higher]}: a debt, not a problem (Documentation -> Citation Direction). Keep the link; it is repaid when the text is upgraded to state the concept in the base's own terms, never by deleting the link."

def file_links(visible: str):
    """Each link to a file in `visible`: (line, link, file part, fragment).

    Relative links and root-relative ones (`/docs/...`) both; `link_target`
    says which file each names. External and in-page links are not links to a
    file and are left out.
    """
    for match in re.finditer('\\]\\(([^)\\s]+)\\)', visible):
        link = match.group(1)
        if EXTERNAL_LINK.match(link):
            continue
        file_part, _, fragment = link.partition('#')
        if not file_part:
            continue
        line = visible[:match.start()].count('\n') + 1
        yield (line, link, file_part, fragment)

def is_root_relative(file_part: str) -> bool:
    """Whether a link's file part is written from the checkout's root rather than from its document's folder."""
    return file_part.startswith('/')

def link_target(path: Path, file_part: str, root: Path) -> Path:
    """The file a link in `path` names: a root-relative one under the checkout `root`, as
    `memar content resolve-path` resolves it; any other from `path`'s own folder."""
    if is_root_relative(file_part):
        return under_root(file_part, root)
    return path.parent / file_part

def upward_link_warnings(path: Path, visible: str, cache: dict) -> list[str]:
    """Every relative link in a Markdown document that points up the layers.

    A root-relative link is resolved and judged by `link_problems`; whether it
    points up the layers is not asked here.
    """
    warnings: list[str] = []
    for line, _, file_part, _ in file_links(visible):
        if is_root_relative(file_part):
            continue
        upward = _upward_link_warning(path, file_part, line, cache)
        if upward:
            warnings.append(upward)
    return warnings

def link_problems(path: Path, visible: str, cache: dict, root: Path) -> list[str]:
    """Every relative or root-relative link in a Markdown document that does not resolve.

    Both halves of a link are checked, because both break the same way and a
    document moved one folder deep takes its links' paths and their anchors with
    it: the file the link names, and the heading inside that file. A
    root-relative link resolves under `root`, the checkout `memar content resolve-path`
    resolves against.
    """
    problems: list[str] = []
    for line, link, file_part, fragment in file_links(visible):
        target = link_target(path, file_part, root)
        if is_root_relative(file_part):
            kind = 'root-relative link'
            breaks = f'It is resolved under {root}, the checkout `memar content resolve-path` resolves against, and what breaks it is the target moving.'
        else:
            kind = 'relative link'
            breaks = 'Moving a document is what breaks one silently: nothing about the link changes, only the folder it was written from.'
        if not target.exists():
            problems.append(f'line {line}: {kind} {file_part} does not exist. A link to a document that is not there cannot be followed. {breaks}')
            continue
        if not fragment or not target.is_file() or target.suffix.lower() != '.md':
            continue
        present = _fragments_of(target, cache)
        if present is not None and fragment not in present:
            problems.append(f'line {line}: {kind} {link} names no heading in {file_part}. The file is there and the anchor is not, so a reader lands on the document rather than on the part of it the link was written to point at.')
    return problems

def anchor_problems(visible: str, text: str) -> list[str]:
    """Every in-page link in a Markdown document that names a heading the document lacks."""
    problems: list[str] = []
    if '](#' in visible:
        present = headings_by_fragment(visible, text)
        for match in re.finditer('\\]\\(#([^)]*)\\)', visible):
            if match.group(1) not in present:
                problems.append(f'line {text[:match.start()].count(chr(10)) + 1}: in-page anchor #{match.group(1)} has no matching heading in this file')
    return problems
