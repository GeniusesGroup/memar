#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/changelog_record.py — a changelog record and its contributors, read as changelog.md defines them.

Shared by `list-ai-only-changelog-records`, which lists the records no person
contributed to, and by `add-human-approval-to-changelog-record`, which adds a
person's approval to one. One reading, so the record one verb lists is the
record the other writes to.

**The structure is the document's, not a second one.** changelog.md →
Structure says a record is a `###` under the one `## Changelog`, its metadata
bullets directly under the title; → Contributors (entry field) says the
`Contributors` bullet holds one sub-bullet per contributor, each a link to that
contributor's CONTRIBUTORS.md heading followed by role tags. → CONTRIBUTORS.md
says who a heading is: a `##` is a natural person or a legal entity, the
legal entity carrying a `Full Legal Name` bullet ("legal persons only", the
Template says), and a brand, tool, or model is a `###` under its entity. So a
contributor's kind is read from the heading its link lands on, never from its
name, and nothing here keeps a list of which names are models.

**"Only AI" is a reading of that structure, and its edge is stated.** A record
is listed when every contributor lands on a `###` — a brand or a tool. A `###`
tool that is not an AI (an editor) is still a `###`; the document gives no
finer type, so none is invented. A record with a natural person among its
contributors is not listed. A contributor whose link lands nowhere is not
guessed at: its record, when no person is among the others, is counted apart,
neither listed nor approvable. A legal entity is neither a person nor a brand,
so a record naming one is not listed.

**Where CONTRIBUTORS.md is.** Each contributor link is resolved against the
ledger's own folder, as a reader following the link would resolve it, so a
project with its own CONTRIBUTORS.md is read with its own, and the approval
line reuses the very path the record's links already use.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from modules.knowledge.documentation.changelog.primitive.contributor_role import ContributorRole
from modules.knowledge.content.services.markdown import without_code

NATURAL_PERSON = "natural person"
LEGAL_ENTITY = "legal entity"
BRAND_OR_TOOL = "brand or tool"

CHANGELOG_HEADING = "## Changelog"
TEMPLATE_ANCHOR = "template"
APPROVED = ContributorRole.APPROVED.word

_FIELD = re.compile(r"^- Contributors:[ \t]*(.*)$")
_SUB_BULLET = re.compile(r"^([ \t]+)[-*][ \t]+(.*)$")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)#\s]*)#([^)\s]+)\)")
_HEADING = re.compile(r"^(#{2,3})[ \t]+(.+?)[ \t]*$")
_LEGAL_NAME = re.compile(r"^[-*][ \t]+(?:\*\*)?Full Legal Name(?:\*\*)?:")


@dataclass(frozen=True)
class Contributor:
    """One sub-bullet of a record's `Contributors`: the first link's label, path, and anchor."""

    name: str
    target: str
    anchor: str
    line: int


@dataclass(frozen=True)
class ChangelogRecord:
    """One `###` entry of a ledger; lines are 0-based indexes into the ledger's lines."""

    number: int
    title: str
    line: int
    contributors: tuple[Contributor | None, ...]
    insert_at: int | None
    indent: str


@dataclass(frozen=True)
class ContributorSection:
    """One heading of CONTRIBUTORS.md and the kind of contributor it is."""

    name: str
    anchor: str
    kind: str


@dataclass
class LedgerReading:
    """A ledger's records sorted by what a human reviewer may do with them."""

    total: int = 0
    listed: list[ChangelogRecord] = field(default_factory=list)
    unknown: list[ChangelogRecord] = field(default_factory=list)


def lines_of(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def changelog_records(text: str) -> list[ChangelogRecord]:
    """Every record under `## Changelog`, in the ledger's order, numbered from 1."""
    lines = lines_of(text)
    visible = lines_of(without_code(text.replace("\r\n", "\n").replace("\r", "\n")))
    starts: list[int] = []
    inside = False
    for index, line in enumerate(visible):
        if line.rstrip() == CHANGELOG_HEADING:
            inside = True
        elif inside and line.startswith("## "):
            inside = False
        elif inside and line.startswith("### "):
            starts.append(index)
    records = []
    for number, start in enumerate(starts, 1):
        end = starts[number] if number < len(starts) else len(lines)
        records.append(_record(number, lines, visible, start, end))
    return records


def _record(number: int, lines: list[str], visible: list[str], start: int, end: int) -> ChangelogRecord:
    contributors: list[Contributor | None] = []
    insert_at = None
    indent = "  "
    for index in range(start + 1, end):
        if visible[index].startswith("#"):
            break
        if not _FIELD.match(visible[index]):
            continue
        inline = _FIELD.match(lines[index]).group(1)
        if inline:
            contributors.append(_contributor(inline, index))
        cursor = index + 1
        while cursor < end and (bullet := _SUB_BULLET.match(lines[cursor])):
            indent = bullet.group(1)
            contributors.append(_contributor(bullet.group(2), cursor))
            cursor += 1
        insert_at = None if inline else cursor
        break
    return ChangelogRecord(number, lines[start][4:].strip(), start, tuple(contributors), insert_at, indent)


def _contributor(text: str, line: int) -> Contributor | None:
    link = _LINK.search(text)
    return Contributor(link.group(1), link.group(2), link.group(3), line) if link else None


def heading_anchor(heading: str) -> str:
    """The anchor a Markdown renderer gives a heading: lower case, punctuation gone, spaces to hyphens."""
    kept = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return kept.replace(" ", "-")


def contributor_sections(path: Path) -> dict[str, ContributorSection]:
    """The headings of a CONTRIBUTORS.md by anchor, the Template and what it holds left out."""
    sections: dict[str, ContributorSection] = {}
    current: list = []
    in_template = False
    for line in lines_of(without_code(path.read_text(encoding="utf-8"))):
        heading = _HEADING.match(line)
        if heading:
            level, name = len(heading.group(1)), heading.group(2)
            anchor = heading_anchor(name)
            if level == 2:
                in_template = anchor == TEMPLATE_ANCHOR
            if in_template:
                current = []
                continue
            current = [name, anchor, NATURAL_PERSON if level == 2 else BRAND_OR_TOOL]
            sections[anchor] = ContributorSection(*current)
        elif current and current[2] == NATURAL_PERSON and _LEGAL_NAME.match(line):
            current[2] = LEGAL_ENTITY
            sections[current[1]] = ContributorSection(*current)
    return sections


class Directory:
    """CONTRIBUTORS.md files read once each, resolved from the ledger that links to them."""

    def __init__(self, ledger: Path) -> None:
        self.folder = ledger.parent
        self.read: dict[Path, dict[str, ContributorSection]] = {}

    def section(self, contributor: Contributor | None) -> ContributorSection | None:
        if contributor is None:
            return None
        path = (self.folder / contributor.target).resolve()
        if path not in self.read:
            self.read[path] = contributor_sections(path) if path.is_file() else {}
        return self.read[path].get(contributor.anchor)


def classify(records: list[ChangelogRecord], directory: Directory) -> LedgerReading:
    """Records whose every contributor is a brand or tool, and records naming someone unknown."""
    reading = LedgerReading(total=len(records))
    for item in records:
        if not item.contributors:
            continue
        sections = [directory.section(contributor) for contributor in item.contributors]
        if any(section is not None and section.kind == NATURAL_PERSON for section in sections):
            continue
        if any(section is None for section in sections):
            reading.unknown.append(item)
        elif all(section.kind == BRAND_OR_TOOL for section in sections):
            reading.listed.append(item)
    return reading


def ai_only_records(ledger: Path) -> LedgerReading:
    return classify(changelog_records(ledger.read_text(encoding="utf-8")), Directory(ledger))
