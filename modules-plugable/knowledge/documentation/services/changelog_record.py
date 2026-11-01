#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import re
from dataclasses import dataclass
from pathlib import Path
Approved = import_module('modules-plugable.knowledge.documentation.changelog.primitive.approved').Approved
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
_m_refs = import_module('modules-plugable.knowledge.documentation.services.content_refs')
without_code = _m_markdown.without_code
NATURAL_PERSON = 'natural person'
LEGAL_ENTITY = 'legal entity'
BRAND_OR_TOOL = 'brand or tool'
TEMPLATE_ANCHOR = 'template'
CHANGELOG_KIND = 'changelog'
APPROVAL_KIND = 'approval'
APPROVED = Approved.word
_HEADING = re.compile('^(#{2,3})[ \\t]+(.+?)[ \\t]*$')
_LEGAL_NAME = re.compile('^[-*][ \\t]+(?:\\*\\*)?Full Legal Name(?:\\*\\*)?:')
_VERDICT = re.compile('^[ \\t]*(?:[-*|][ \\t]*)?\\*{0,2}Verdict\\*{0,2}[ \\t]*[:|][ \\t]*\\*{0,2}(\\w+)', re.I | re.M)
_TITLE = re.compile('^#{1,6}[ \\t]+(.*?)[ \\t]*#*[ \\t]*$')


@dataclass(frozen=True)
class ContributorSection:
    name: str
    anchor: str
    kind: str


def lines_of(text: str) -> list[str]:
    return text.replace('\r\n', '\n').replace('\r', '\n').split('\n')


def heading_anchor(heading: str) -> str:
    kept = re.sub('[^\\w\\- ]', '', heading.strip().lower())
    return kept.replace(' ', '-')


def contributor_sections(path: Path) -> dict[str, ContributorSection]:
    sections: dict[str, ContributorSection] = {}
    current: list = []
    in_template = False
    for line in lines_of(without_code(path.read_text(encoding='utf-8'))):
        heading = _HEADING.match(line)
        if heading:
            level, name = (len(heading.group(1)), heading.group(2))
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


def is_ai_author(author, sections: dict) -> bool:
    if not author:
        return False
    section = sections.get(heading_anchor(str(author)))
    return section is not None and section.kind == BRAND_OR_TOOL


def title_of(content) -> str:
    first = ''
    for line in content.body.splitlines():
        if not line.strip():
            continue
        heading = _TITLE.match(line)
        if heading and line.startswith('###'):
            return heading.group(1)
        first = first or line.strip()
    return first


def _approved_by_a_non_ai(task_id: str, content, sections: dict) -> bool:
    if content.header.get('kind') != APPROVAL_KIND or is_ai_author(content.header.get('author'), sections):
        return False
    verdict = _VERDICT.search(content.body)
    return verdict is not None and verdict.group(1).lower() == APPROVED.lower()


def ai_only_changelogs(contents, sections: dict) -> list:
    held = list(contents)
    approved = set()
    for task_id, content in held:
        if _approved_by_a_non_ai(task_id, content, sections):
            approved |= _m_refs.refs_of(task_id, content)
    found = []
    for task_id, content in held:
        if content.header.get('kind') != CHANGELOG_KIND or not is_ai_author(content.header.get('author'), sections):
            continue
        if (task_id, content.number) in approved:
            continue
        found.append((task_id, content.number, title_of(content), content.header.get('placed_at', '')))
    found.sort(key=lambda entry: (entry[3], entry[0], entry[1]))
    return found
