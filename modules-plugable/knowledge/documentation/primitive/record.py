#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from dataclasses import dataclass
from pathlib import Path
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
from modules.knowledge.content.primitive.record_key import RecordKey
from modules.knowledge.label.services.status_words import document_kinds, DOCUMENT_KIND_WORDS, Label_Plan, Label_Report, Label_Explanation, Label_Handoff, Label_Research, statuses, statuses_for, status_keys, status_listing, read_status, status_definitions, STATUS_LABEL, STATUS_WORDS
_m_report_key = import_module('modules-plugable.knowledge.documentation.report.primitive.report_key')
ReportKey = _m_report_key.ReportKey
from modules.knowledge.content.primitive.catalog import Catalog
_m_decisions_needed = import_module('modules-plugable.knowledge.documentation.report.primitive.decisions_needed')
DecisionsNeeded = _m_decisions_needed.DecisionsNeeded
HAND_BACK_MAX_LINES = DecisionsNeeded.max_lines
PLAN_PARTS = Catalog(Path(__file__).resolve().parent.parent / 'plan' / 'primitive', 'plan-part')
REPORT_PARTS = Catalog(Path(__file__).resolve().parent.parent / 'report' / 'primitive', 'report-part')

@dataclass(frozen=True)
class Record:
    file_name: str
    kind: type
    keys: tuple[RecordKey, ...]
    parts: tuple[str, ...]
    heading: str
    hand_back_part: str | None = None
    hand_back_max_lines: int | None = None

    @property
    def statuses(self) -> tuple[type, ...]:
        return statuses_for(self.kind)

    def current(self, front: dict[str, str]) -> dict[str, str]:
        read = dict(front)
        for key in self.keys:
            if key.key not in read:
                earlier = next((name for name in key.earlier if name in read), None)
                if earlier is not None:
                    read[key.key] = read[earlier]
        return read

    def outline(self) -> str:
        front = [f'{key.written}: {key.description}' for key in self.keys]
        return '\n'.join(['---', *front, '---', f'# {self.heading}', '', *(f'## {part}' for part in self.parts)]) + '\n'
PLAN = Record('plan.md', Label_Plan, tuple(PlanKey), PLAN_PARTS.headings(), 'TITLE')
REPORT = Record('report.md', Label_Report, tuple(ReportKey), tuple(part.heading for part in REPORT_PARTS if 'hand-back' not in part.labels), 'Report', hand_back_part=DecisionsNeeded.heading, hand_back_max_lines=HAND_BACK_MAX_LINES)
