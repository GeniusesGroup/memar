#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_index.py — the index `memar content find` ranks: the sections of the checkout's content, scored by word similarity.

**The corpus is the one `content_corpus` names**, the same as `search`'s, so no verb sees a narrower
or a wider world than the verb beside it. Its units are each Markdown section, from its heading to
the next heading of any level, and each document's text before its first heading; each `.kh` file
is one unit, since a declaration file has no headings. A unit records the links its text makes to
a section by anchor, resolved to a document of the corpus, which `find` prints under a hit.

**The ranking is BM25 over weighted fields**, the constants below. They are kept because they are
the first version's and nothing measured beats them, not because the probe of proposal v3 (section
11, 50 frozen sessions) chose them: no variant it measured can be told from them case by case on
the documents a planner named. A constant changes only when a variant beats the current one case
by case at a two-sided sign-test p below 0.05, on that sample plus the sessions completed since.
It does not find what an act must read: at most 12% of a kind's sections are in a top 10 with
links, which is why the lists of `normative_references` exist; the ranking is informative.

**The index is built in memory on each call** and kept nowhere: about a second for Memar's corpus,
a query in tens of milliseconds. A file to keep true by hand beside the documents would be a copy
with no re-derivation path.

TODO(when the Memar server exists): keep the index across calls, keyed per file by its stat and
SHA-256 and per section by its hash, so a call reads only what changed; and rank by meaning as well
as by words — a dense vector per section, keyed by its hash, fused with BM25 by reciprocal rank.
Neither is done in a process that ends with each call: the first would be a file to keep true by
hand, and the second needs a model this offline tool does not carry. Recorded 2026-10-16, session
20261016-T135247Z-15464; the study of the server is session 20261016-T095101Z-14276.
"""
from __future__ import annotations

import math
import posixpath
import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

from services.content_corpus import content_files
from services.content_reference import read_text
from services.content_section import outline, section_hash

# BM25's usual constants, the first version's; see the docstring for the support they have.
K1 = 1.2
B = 0.75
# The weight of a word found in a unit's heading, in its document's path, and in its body.
HEADING_WEIGHT = 3
PATH_WEIGHT = 1
BODY_WEIGHT = 1
# At most this many sections of one document are ranked, so a long document does not fill the list.
PER_DOCUMENT = 2
# Words that say nothing about a subject. No stemming: a plural is another word.
STOP = frozenset(
    "the a an of to and or in is are for on that this it as be by with from at not its which each one into than then so if when what".split()
)
WORD = re.compile(r"[a-z0-9][a-z0-9_-]+")
MINIMUM_WORD = 3
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


class Unit(NamedTuple):
    """One section: its document's path from the checkout, where in the document's text it runs and where its whole section
    (subsections included) stops, its heading and anchor (both empty for the text before a first heading), its section's
    hash, the sections it links as (path, anchor), and whether it is a `.kh` file."""

    path: str
    start: int
    end: int
    stop: int
    heading: str
    anchor: str
    hash: str
    links: tuple[tuple[str, str], ...]
    kh: bool


class Index(NamedTuple):
    """The units, each document's text, and what ranking needs of them."""

    units: tuple[Unit, ...]
    texts: dict[str, str]
    fields: tuple[Counter, ...]
    lengths: tuple[int, ...]
    idf: dict[str, float]

    def rank(self, query: str) -> list[int]:
        """The numbers of the units with a word of QUERY, best first, at most `PER_DOCUMENT` of one document."""
        asked = set(words(query))
        average = sum(self.lengths) / len(self.lengths) if self.lengths else 1
        scored = []
        for number, field in enumerate(self.fields):
            norm = K1 * (1 - B + B * self.lengths[number] / average)
            score = sum(
                self.idf[word] * field[word] * (K1 + 1) / (field[word] + norm) for word in asked if field.get(word)
            )
            if score > 0:
                scored.append((-score, number))
        scored.sort()
        taken: Counter = Counter()
        ranked = []
        for _, number in scored:
            path = self.units[number].path
            if taken[path] < PER_DOCUMENT:
                taken[path] += 1
                ranked.append(number)
        return ranked

    def text_of(self, unit: Unit) -> str:
        """The text UNIT runs over, its heading line first."""
        return self.texts[unit.path][unit.start : unit.end]


def words(text: str) -> list[str]:
    """The words of TEXT that count: lower case, not a stop word, at least `MINIMUM_WORD` characters."""
    return [word for word in WORD.findall(text.lower()) if word not in STOP and len(word) >= MINIMUM_WORD]


def _link_target(path: str, link: str) -> tuple[str, str] | None:
    """The (document, anchor) a LINK in the document at PATH names by anchor; None for an external link or one with no anchor."""
    if EXTERNAL.match(link):
        return None
    file_part, _, anchor = link.partition("#")
    if not anchor:
        return None
    if not file_part:
        return path, anchor
    joined = file_part.lstrip("/") if file_part.startswith("/") else posixpath.join(posixpath.dirname(path), file_part)
    return posixpath.normpath(joined), anchor


def _links(path: str, body: str) -> tuple[tuple[str, str], ...]:
    found = (_link_target(path, link) for link in LINK.findall(body))
    return tuple(dict.fromkeys(target for target in found if target is not None))


def _units(path: str, text: str) -> list[Unit]:
    headings = outline(text)
    bounds = [(0, 0, "", "", None)] + [(each.start, each.level, each.heading, each.anchor, each) for each in headings]
    units = []
    for number, (start, _, heading, anchor, found) in enumerate(bounds):
        end = bounds[number + 1][0] if number + 1 < len(bounds) else len(text)
        if not found and not text[start:end].strip():
            continue
        stop = found.stop if found else end
        units.append(Unit(path, start, end, stop, heading, anchor, section_hash(text[start:stop]), _links(path, text[start:end]), False))
    return units


def build(root: Path) -> Index:
    """The index of the corpus of the checkout at ROOT, read now."""
    units: list[Unit] = []
    texts: dict[str, str] = {}
    for file in content_files(root):
        path = file.relative_to(root).as_posix()
        text = read_text(file)
        texts[path] = text
        if file.suffix.lower() == ".kh":
            units.append(Unit(path, 0, len(text), len(text), file.stem, "", section_hash(text), (), True))
        else:
            units.extend(_units(path, text))
    fields, lengths = [], []
    frequency: Counter = Counter()
    for unit in units:
        body = texts[unit.path][unit.start : unit.end]
        field: Counter = Counter()
        for weight, text in (
            (HEADING_WEIGHT, unit.heading),
            (PATH_WEIGHT, unit.path.replace("/", " ").replace(".", " ")),
            (BODY_WEIGHT, body),
        ):
            for word in words(text):
                field[word] += weight
        fields.append(field)
        lengths.append(len(words(body)) + 1)
        frequency.update(field.keys())
    count = len(units)
    idf = {word: math.log(1 + (count - seen + 0.5) / (seen + 0.5)) for word, seen in frequency.items()}
    return Index(tuple(units), texts, tuple(fields), tuple(lengths), idf)
