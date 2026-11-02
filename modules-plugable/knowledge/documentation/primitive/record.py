#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.Label_Status import Label_Status
from machine.plugable_import import load as plugable_load
Label_DocumentKind = plugable_load('knowledge.documentation.labels.Label_DocumentKind').Label_DocumentKind
Label_Explanation = plugable_load('knowledge.documentation.explanation.labels.Label_Explanation').Label_Explanation
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Label_Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Label_Report').Label_Report
Label_Handoff = plugable_load('knowledge.documentation.handoff.labels.Label_Handoff').Label_Handoff
Label_Research = plugable_load('knowledge.documentation.research.labels.Label_Research').Label_Research
from importlib import import_module
from dataclasses import dataclass
from pathlib import Path
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
from modules.knowledge.content.primitive.record_key import RecordKey
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
        return Label_Status.for_document(self.kind)

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
