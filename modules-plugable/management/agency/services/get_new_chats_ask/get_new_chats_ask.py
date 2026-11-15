#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_ask = import_module('modules-plugable.management.agency.widgets.new_chats_ask.new_chats_ask')
NEW_CHATS_COMMAND = _m_ask.NEW_CHATS_COMMAND
INTRO = _m_ask.INTRO
brief_text = _m_ask.brief_text
chats_text = _m_ask.chats_text
own_task_blocking = _m_ask.own_task_blocking
get_new_chats_ask = _m_ask.get_new_chats_ask
NewChatsAsk = _m_ask.NewChatsAsk
PlanKey = _m_ask.PlanKey
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId


def new_chats_ask(task_ids: tuple[str, ...], /, *, task_id: str | None = None, blocking: tuple[str, ...] | None = None) -> None:
    get_new_chats_ask(list(task_ids), list(blocking or ()), task_id)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        new_chats_ask,
        name=NEW_CHATS_COMMAND,
        summary='print the message that asks the owner to run tasks each in a completely new chat',
        description=f"Print the message that asks the owner to run each task ID in a completely\nnew chat, ready to show: for each its title, priority, the first sentence of\nits Why, and the text that hands it over (the one `get-task-plan-carry-out-brief`\nprints). A task the asking chat cannot go on without is marked blocks, the others\nindependent, to run in parallel. The chat's own task, given with {TaskId.FLAG}, says\nwhich: those in its {PlanKey.DEPENDS_ON.written}. --blocking marks more by hand. Writes nothing.\n\nWhere your agent app has a tool that starts a chat, start one per task and hand it only\nthe text `get-task-plan-carry-out-brief` prints; where it has none, show this message and\nsay in one line that you cannot start a chat. You cannot learn that another chat ended: ask\nthe owner to say when each blocking one is done, meanwhile do only the work no waiting\ntask touches, and end your turn when none is left. An independent task is written\nwhole, opened with no --parent, its chat started independent and not as your child session\n(where your app has the choice, so that none of its messages come back to you: each costs), and then left: its exchanges with the owner and its end are not\nyours to follow; two that change the same files are listed one after the other. Say how many chats you opened.\n\nWork your chat needs that cannot be specified exactly to an agent, because it needs\nback-and-forth with the owner, is neither done nor delegated by your chat: set your plan\nBlocked on its task, open its chat for the owner, say in one message which chat to go\nto and what it must produce, and stop until the owner says it is done.\n\nComposition is owned by agency (`New_Chats_Ask`); this verb is the stable command face.",
        help={'task_ids': 'the tasks to run, one chat each', 'task_id': "the asking chat's own task: each ID in its plan's dependencies is marked as blocking", 'blocking': 'a task the asking chat waits for, in addition'},
    ),
)
