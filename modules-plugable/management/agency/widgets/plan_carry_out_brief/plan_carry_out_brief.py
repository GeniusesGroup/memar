#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.console import fail
_m_storage = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage')
_m_folder = import_module('modules-plugable.management.task.services.folder')
from modules.computer.software.primitive.project_name import ProjectName
from modules.computer.software.primitive.project_path import ProjectPath
_m_compose = import_module('modules-plugable.management.agency.widgets.context_compose.context_compose')
START_COMMAND = _m_compose.START_COMMAND
from bundles.memar_adaptor.cli.call_names import call_of_module
PLAN_BRIEF_COMMAND = 'get-task-plan-carry-out-brief'
INIT_CALL = call_of_module(
    'modules-plugable.management.agency.widgets.context_compose.context_compose',
    START_COMMAND,
)
_m_status_face = import_module('modules-plugable.knowledge.label.status.services.status_of_thing')
SET_STATUS_LINE = f"memar {call_of_module(_m_status_face.__name__, 'set')} ID WORD --project NAME"


class _Storage:
    """One place durable state is reached until the memory/record adapter binds."""

    def is_task(self, task_id: str) -> bool:
        return _m_storage.is_task_folder(task_id) or _m_folder.project_folder_of(task_id) is not None

    def has_plan(self, task_id: str) -> bool:
        if _m_storage.has_plan(task_id):
            return True
        found = _m_folder.project_folder_of(task_id)
        return found is not None and _m_storage.has_plan(found)


_storage = _Storage()


class PlanCarryOutBrief:

    def __init__(self, storage: _Storage | None=None) -> None:
        self.storage = storage or _storage

    def text_of(self, task_id: str) -> str:
        return f'Your task is task {task_id}. Run `memar {INIT_CALL} --task-id {task_id}` first, before anything else, and follow what it prints. Where Memar\'s MCP tools are listed, call the tool `{INIT_CALL}` with the same arguments instead of running the command.'

    def print(self, task_id: str) -> None:
        store = self.storage
        if not store.is_task(task_id) or not store.has_plan(task_id):
            fail(f'no task to hand over in {task_id}: it has no plan on its timeline. Open it with `memar task_ensure --title T --parent ID {ProjectName.FLAG} {ProjectName.METAVAR}` (or `{ProjectPath.FLAG} {ProjectPath.METAVAR}`), ID the task handing it over, and post its plan with `memar conversation_post --kind plan` first')
        print(self.text_of(task_id))


def brief_text(task_id: str) -> str:
    return PlanCarryOutBrief().text_of(task_id)


def get_task_plan_carry_out_brief(task_id: str) -> None:
    PlanCarryOutBrief().print(task_id)


def task_plan_carry_out_brief(task_id: str) -> None:
    get_task_plan_carry_out_brief(task_id)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_plan_carry_out_brief,
        name=PLAN_BRIEF_COMMAND,
        summary="print the text that hands a task's plan to a sub-agent to carry out",
        description=f"Print the text that hands the task ID to a sub-agent to carry out its plan,\nwith ID filled in, ready to paste: the same text `ensure --parent` prints after\nits other lines. It tells the sub-agent to run `memar {INIT_CALL} --task-id ID`\nfirst. The task itself is not in it; it is in the task's latest plan content,\nwhich the delegating task posts before handing the text over, adding nothing to it.\n\nStart a new sub-agent rather than resume a long one. Sub-agents run one at a time unless\nthe owner asks otherwise, and any that run at once write disjoint files, or a shared one only\nthrough `memar content_write`. A delegated step is done only when its report content exists:\na sub-agent that could only return text hands back its report, and you post it as kind report\nand set its Status with `{SET_STATUS_LINE}`, marking what you could not.",
        takes=('task_id',),
        help={'task_id': 'the task whose plan is handed over'},
    ),
)
