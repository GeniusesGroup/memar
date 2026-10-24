#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/text/services/text_check.py — what is wrong with the bytes of a text file, reported before it is inherited.

The encoding and newline rules hold for every text file in every project, because a shell damages a file
the same way whatever the file is for: a UTF-8 BOM, bytes that are not UTF-8, a replacement character, mixed
line endings, a missing final newline, the fingerprints of mojibake. This is the text domain's half of
`memar content check`; the Markdown conventions and Memar's written-surface rules are the documentation
module's, and `memar content check` composes the two.
"""
from __future__ import annotations
from pathlib import Path
MIXED_ENDINGS = 'mixed line endings: {crlf} CRLF and {lf} LF. A file that already holds one convention will gain the other the first time a tool writes it with the other, which is how a diff stops being readable.'
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
            hits.append(f"{count} occurrence{('s' if count > 1 else '')} of {marker!r}, the signature of {source} having been decoded as Latin-1 and re-encoded — a shell read/write round trip, not the file's own text (a hint; the leading letter is a real letter in some languages, so judge before acting)")
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
    if path.name != 'README.md' or path.is_symlink():
        return False
    target = raw.decode('utf-8', errors='replace').strip()
    return bool(target) and '\n' not in target and (not any((c.isspace() for c in target))) and (path.parent / target).is_file()

def file_problems(path: Path) -> tuple[list[str], str | None]:
    """What is wrong with the bytes of PATH, and its text; the text is None when nothing more can be judged.

    An unreadable file, a file that is not UTF-8, and a README that is only a link stand-in end the judgment
    there: the first two with their problem, the stand-in with none.
    """
    problems: list[str] = []
    try:
        raw = path.read_bytes()
    except OSError as error:
        return ([f'unreadable: {error}'], None)
    if _is_link_stand_in(path, raw):
        return ([], None)
    if raw.startswith(b'\xef\xbb\xbf'):
        problems.append('line 1: UTF-8 BOM present; every tool that reads this as text sees the BOM as content')
    try:
        text = raw[3:].decode('utf-8') if raw.startswith(b'\xef\xbb\xbf') else raw.decode('utf-8')
    except UnicodeDecodeError as error:
        problems.append(f'not valid UTF-8 ({error}); a tool that decodes with replacement characters has already lost the original')
        return (problems, None)
    if not raw:
        problems.append('file is empty')
    crlf = text.count('\r\n')
    lf = text.count('\n') - crlf
    if crlf and lf:
        problems.append(MIXED_ENDINGS.format(crlf=crlf, lf=lf))
    if text and (not text.endswith('\n')):
        problems.append('no newline at end of file')
    for number, line in enumerate(text.split('\n'), start=1):
        if '\ufffd' in line:
            problems.append(f'line {number}: U+FFFD replacement character — a tool decoded this file with errors replaced instead of failing, so the original characters are already gone')
    for hint in _mojibake_hints(text):
        problems.append('likely mojibake: ' + hint)
    return (problems, text)
