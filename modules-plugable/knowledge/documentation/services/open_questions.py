#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import re
RULE = 'modules-plugable/knowledge/documentation/rules/no-record-beside-a-document/no-record-beside-a-document.md'
HEADING = re.compile('^#{1,6}[ \\t]+(?:\\d+[.)][ \\t]+)?\\**((?:open|unresolved|review)[ \\t]+questions?|(?:open[ \\t]+)?questions?[ \\t]+for[ \\t]+the[ \\t]+owner)\\**[ \\t]*(?:\\([^)]*\\))?[ \\t]*:?[ \\t]*#*[ \\t]*$', re.IGNORECASE | re.MULTILINE)


def open_questions_problems(visible: str) -> list[str]:
    return [f"line {visible[:match.start()].count(chr(10)) + 1}: a section '{match.group(1)}': no document has a section of questions; each question is posted as a `question` content on the timeline of the task it concerns, and the document states only what holds ({RULE})" for match in HEADING.finditer(visible)]
