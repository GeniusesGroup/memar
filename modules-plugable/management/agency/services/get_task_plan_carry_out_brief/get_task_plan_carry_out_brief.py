#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from bundles.memar_adaptor.cli.call_names import call_of_module
_m_status_face = import_module('modules-plugable.knowledge.label.status.services.status_of_thing')
SET_STATUS_LINE = f"memar {call_of_module(_m_status_face.__name__, 'set')} ID WORD --project NAME"
_m_brief = import_module('modules-plugable.management.agency.widgets.plan_carry_out_brief.plan_carry_out_brief')
PLAN_BRIEF_COMMAND = _m_brief.PLAN_BRIEF_COMMAND
START_COMMAND = _m_brief.START_COMMAND
brief_text = _m_brief.brief_text
get_task_plan_carry_out_brief = _m_brief.get_task_plan_carry_out_brief
PlanCarryOutBrief = _m_brief.PlanCarryOutBrief
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
INIT_CALL = call_of_module(
    'modules-plugable.management.agency.services.get_task_init_context.get_task_init_context',
    START_COMMAND,
)


def task_plan_carry_out_brief(task_id: str) -> None:
    get_task_plan_carry_out_brief(task_id)


declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_plan_carry_out_brief,
        name=PLAN_BRIEF_COMMAND,
        summary="print the text that hands a task's plan to a sub-agent to carry out",
        description=f"Print the text that hands the task ID to a sub-agent to carry out its plan,\nwith ID filled in, ready to paste: the same text `ensure --parent` prints after\nits other lines. It tells the sub-agent to run `memar {INIT_CALL} --task-id ID`\nfirst. The task itself is not in it; it is in the task's latest plan content,\nwhich the delegating task posts before handing the text over, adding nothing to it.\n\nStart a new sub-agent rather than resume a long one. Sub-agents run one at a time unless\nthe owner asks otherwise, and any that run at once write disjoint files, or a shared one only\nthrough `memar content_write`. A delegated step is done only when its report content exists:\na sub-agent that could only return text hands back its report, and you post it as kind report\nand set its Status with `{SET_STATUS_LINE}`, marking what you could not.\n\nComposition is owned by agency (`Plan_Carry_Out_Brief`); this verb is the stable command face.",
        takes=('task_id',),
        help={'task_id': 'the task whose plan is handed over'},
    ),
)
