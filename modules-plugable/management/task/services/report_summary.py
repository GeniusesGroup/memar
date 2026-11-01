#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
Result = import_module('modules-plugable.knowledge.documentation.report.primitive.result').Result
WhatRan = import_module('modules-plugable.knowledge.documentation.report.primitive.what_ran').WhatRan
from pathlib import Path
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
report_part = _m_report_file.report_part
RESULT_HEADING = Result.heading
RAN_HEADING = WhatRan.heading
SUMMARY_LINES = 3
LINE_WIDTH = 160

def summary_lines(folder: Path) -> list[str]:
    for label, heading in (('result', RESULT_HEADING), ('ran', RAN_HEADING)):
        lines = [line.strip() for line in report_part(folder, heading)][:SUMMARY_LINES]
        if lines:
            cut = [line if len(line) <= LINE_WIDTH else line[:LINE_WIDTH - 1] + '…' for line in lines]
            return [f'{label}: {cut[0]}', *cut[1:]]
    return [f'no summary: {REPORT_NAME} has no {RESULT_HEADING} or {RAN_HEADING} text']
