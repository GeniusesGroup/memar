#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_propagation.py — the `Propagates to` entries a changelog still owes: obligations, not defects.

Shared by `obligations`, which prints the work-list, and by `check`, which
prints it apart from the problems it counts. One reading of the field, so the
two never report a different list.

A changelog entry's `Propagates to` field names another artifact and the state
of the work the change implies there (documentation-changelog.md -> Propagates
to). `Pending` is the one open state; `Done` and `Rejected` are closed, and
`Rejected` is closed permanently. `search` excludes changelog files, because
their content is history rather than current truth, which is right for concept
search and would leave the work-list with no surface at all.
"""
from __future__ import annotations

import re
from pathlib import Path

from services.content_markdown import without_code

# The state is read from the entry's own field — the first segment after the
# artifact's colon — so a sentence that mentions `Pending` while describing
# something else is not read as an obligation. `Pending deletion` and `Pending
# at absorb time` are how the sources write the same state, and both are open.
_PROPAGATION_OPEN = re.compile(
    r"(?m)^[ \t]*[-*][ \t]+\S.*?:[ \t]*Pending(?![A-Za-z])"
)


# A ledger is named `<base>.changelog.md`, so its stem ends in `.changelog`. The
# document that *specifies* the facet is named `documentation-changelog.md` and
# shows the same section headings, the same `Propagates to` example, and the
# same field names — testing on `endswith(".changelog.md")` reads that
# specification as a ledger full of obligations.
def _is_changelog_ledger(path: Path) -> bool:
    return path.stem.endswith(".changelog")

# A rejected alternative's home is the `Considered and not done` section of a
# changelog entry, and whether a body holds such a record is deliberately not
# checked here. It is not a question about text: `documentation-changelog.md` is
# the document that specifies the field, so it carries a section by that name in
# its own body, and the specification of where records go differs from a record
# only in what the text is for. Any threshold that separates them — heading
# depth, a bullet beside the heading, the file's name — fires on the project's
# own governing document or misses a record written the other way, and a check
# that stands permanently red on a correct file is one a reader learns to skip.
# The hazard the rule addresses is real and named at
# documentation-explanation.md -> Relevance discipline; it is answered by
# writing the record in the changelog, not by a pattern.


def undischarged_propagations(paths: list[Path]) -> list[tuple[Path, int, str]]:
    """Every `Propagates to` entry left `Pending`, as (file, line, report).

    Changelog files only, since that is where the field is defined. Returns
    rather than raises: a `Pending` entry is correct content of the file that
    holds it, so this is a work-list and not a defect, and a caller that counts
    defects must not count these.
    """
    found: list[tuple[Path, int, str]] = []
    for path in paths:
        if path.suffix.lower() != ".md" or not _is_changelog_ledger(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        visible = without_code(text)
        for match in _PROPAGATION_OPEN.finditer(visible):
            line = visible[: match.start()].count("\n") + 1
            artifact = match.group(0).lstrip(" \t-*").rstrip()
            found.append((path, line, f"{path.name} {line}: {artifact} — not yet done"))
    return found
