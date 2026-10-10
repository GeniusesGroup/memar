#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_markdown.py — what in a Markdown document is a link, and what is only text about one.

Shared by `backlinks`, which collects a document's links, by `check`, which
judges them, and by the work-list of open propagations, which reads a ledger's
fields. One reading, so a link one verb follows is the link another verb judges,
and a link quoted in backticks is quoted for all of them.
"""
from __future__ import annotations

import re

# A link this checker cannot judge by looking at the filesystem: a URI with a
# scheme (`https:`, `mailto:`) and a protocol-relative `//host/path`. A leading
# `/` is a site-root reference, which resolves against a server rather than
# against the document's own folder, so it is not a file this run can see.
EXTERNAL_LINK = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)


def without_code(text: str) -> str:
    """`text` with the inside of code spans and fenced blocks blanked out.

    Offsets and line breaks are preserved, so a position in the result is the
    same position in the original. A `](#x)` written inside backticks is text
    about links, not a link, and a `# comment` inside a fence is not a heading;
    neither may be read as either.
    """
    def blank(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    fenced = re.compile(r"(?ms)^(```|~~~).*?^\1[ \t]*$")
    spans = re.compile(r"(?s)(`+)(?:(?!\1).)*?\1")
    return spans.sub(blank, fenced.sub(blank, text))
