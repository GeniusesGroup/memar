#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import re
from pathlib import Path
RULE = 'modules-plugable/knowledge/documentation/documentation.md#written-surface'
DECISIVE = ('holds no', 'holds nothing', 'knows no', 'knows nothing', 'does not hold', 'does not know')
WEAK = ('has no', 'is not a', 'is not an', 'does not have', 'owns no', 'does not own', 'carries no', 'does not carry')
VERB = '|'.join((re.escape(verb) for verb in sorted(DECISIVE + WEAK, key=len, reverse=True)))
SENTENCE = re.compile(f'^(?P<subject>(?:[A-Za-z][\\w-]*\\s+){{0,3}}?[A-Za-z][\\w-]*)\\s+(?P<verb>{VERB})\\b', re.IGNORECASE)
RULES_FOLDER = 'rules'
HEADING = re.compile('^#{1,6}[ \\t]+(.*)$')
LIST_MARK = re.compile('^(?:[-*+>][ \\t]+|\\d+[.)][ \\t]+)+')
CLOSURE = re.compile('^\\s+(?:else|other|more|but)\\b', re.IGNORECASE)
PHRASAL = re.compile('^(?:\\s+[\\w-]+){0,3}\\s+back\\b', re.IGNORECASE)
SENTENCE_BREAK =re.compile('(?<=[.!?])\\s+')
NOT_IN_A_SUBJECT = frozenset(('when', 'if', 'that', 'which', 'where', 'who', 'whose', 'because', 'while', 'and', 'or', 'but', 'unless', 'until', 'with', 'without', 'of', 'in', 'for', 'on', 'at', 'by', 'from', 'under', 'as', 'than', 'so', 'then', 'also', 'nor', 'not', 'no', 'to', 'does', 'is', 'has', 'why', 'how'))


def _problem(line: int, text: str) -> str:
    return f"line {line}: '{text.strip()}' denies something in order to name it; the body states what the thing is and holds, and what it lacks follows from that ({RULE})"


def _hint(line: int, text: str) -> str:
    return f"line {line}: '{text.strip()}' may deny something in order to name it; read it against {RULE}"


def _without_front_matter(visible: str) -> str:
    if not visible.startswith('---\n'):
        return visible
    end = visible.find('\n---\n', 4)
    if end < 0:
        return visible
    return re.sub('[^\\n]', ' ', visible[:end + 5]) + visible[end + 5:]


def _denial(sentence: str) -> str | None:
    if not sentence[:1].isupper():
        return None
    match = SENTENCE.match(sentence)
    if match is None:
        return None
    if any((word.lower() in NOT_IN_A_SUBJECT for word in match.group('subject').split())):
        return None
    if CLOSURE.match(sentence[match.end():]) or PHRASAL.search(sentence[match.end():]):
        return None
    return match.group('verb').lower()


def _judged(visible: str):
    for number, line in enumerate(_without_front_matter(visible).splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('|'):
            continue
        heading = HEADING.match(stripped)
        sentences = [heading.group(1).replace('**', '').strip()] if heading else SENTENCE_BREAK.split(LIST_MARK.sub('', stripped).replace('**', ''))
        for sentence in sentences:
            verb = _denial(sentence)
            if verb is not None:
                yield (number, sentence, verb)


def denial_findings(visible: str, path: Path | None = None) -> tuple[list[str], list[str]]:
    in_a_rule = path is not None and RULES_FOLDER in path.parts
    problems: list[str] = []
    hints: list[str] = []
    for number, sentence, verb in _judged(visible):
        if verb in DECISIVE and not in_a_rule:
            problems.append(_problem(number, sentence))
        else:
            hints.append(_hint(number, sentence))
    return (problems, hints)
