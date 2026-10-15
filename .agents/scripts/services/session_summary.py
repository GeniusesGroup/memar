#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_summary.py — one session in a few lines, for the owner who reviews it.

The owner reviewing a day's sessions reads what each came to, not its folder.
A session's own words for that are its report's Result, the part that says what
the work produced; a report that has none yet says what ran instead. The
summary is those first lines, cut to a width a terminal shows, and nothing
else: the report and the plan remain the record, and the review prints where
they are. A session whose report says nothing under either part has no summary
and says so, rather than leaving the owner to wonder whether it was lost.
"""
from __future__ import annotations

from pathlib import Path

from services.session_report import REPORT_NAME, report_part

RESULT_HEADING = "Result"
RAN_HEADING = "What ran"
SUMMARY_LINES = 3
LINE_WIDTH = 160


def summary_lines(folder: Path) -> list[str]:
    """The lines that say what FOLDER's session came to: `result:` and its first lines, else `ran:`, else `no summary`."""
    for label, heading in (("result", RESULT_HEADING), ("ran", RAN_HEADING)):
        lines = [line.strip() for line in report_part(folder, heading)][:SUMMARY_LINES]
        if lines:
            cut = [line if len(line) <= LINE_WIDTH else line[: LINE_WIDTH - 1] + "…" for line in lines]
            return [f"{label}: {cut[0]}", *cut[1:]]
    return [f"no summary: {REPORT_NAME} has no {RESULT_HEADING} or {RAN_HEADING} text"]
