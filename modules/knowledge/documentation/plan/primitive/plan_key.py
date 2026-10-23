#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/plan_key.py — the front-matter keys of a task plan, declared once.

[Documentation — Plan](../plan.md) names the keys a plan's front matter holds;
they are a closed set, so they are code and are written here and nowhere else
([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
`record.PLAN` is the plan's record built from them, and `task_plan` reads
and writes by them.
"""
from __future__ import annotations
from modules.knowledge.documentation.primitive.record_key import ID_FIELD, START_DATE_FIELD, RecordKey
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath

class PlanKey(RecordKey):
    ID = ID_FIELD
    TITLE = ('title', 'TITLE')
    STATUS = ('status', 'where the task stands, one of the Status words `memar task --help` gives')
    START_DATE = START_DATE_FIELD
    PROJECT = ('project', f'the git top-level of the folder {ProjectName.FLAG} or {ProjectPath.FLAG} names, else that folder')
    PARENT = ('parent', 'ID of the task this one came from, with --parent')
    CONVERSATION = ('conversation', 'the id of the first task of the conversation, with --parent')
    PRIORITY = ('priority', 'N, with --priority')
    LABELS = ('labels', 'a block, one `- KIND: WORD` line a label, with --label KIND=WORD: the words that link this task to others, as many as it needs and none it does not', 'Labels')
    DEPENDS_ON = ('depends_on', 'ID, ID, ...: the tasks that must be Complete before this one can start, each an id or project/id; while one is not, this task is Blocked')
