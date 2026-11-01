#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.record_key import ID_FIELD, START_DATE_FIELD, RecordKey
from modules.knowledge.content.primitive.record_key_set import RecordKeySet
from modules.computer.software.primitive.project_name import ProjectName
from modules.computer.software.primitive.project_path import ProjectPath

class PlanKey(RecordKeySet):
    ID = ID_FIELD
    TITLE = RecordKey('title', 'TITLE')
    START_DATE = START_DATE_FIELD
    PROJECT = RecordKey('project', f'the git top-level of the folder {ProjectName.FLAG} or {ProjectPath.FLAG} names, else that folder')
    PARENT = RecordKey('parent', 'ID of the task this one came from, with --parent')
    CONVERSATION = RecordKey('conversation', 'the id of the first task of the conversation, with --parent')
    PRIORITY = RecordKey('priority', 'N, with --priority')
    LABELS = RecordKey('labels', 'a block, one `- KIND: WORD` line a label, with --label KIND=WORD: the words that link this task to others, as many as it needs and none it does not', 'Labels')
    DEPENDS_ON = RecordKey('depends_on', 'ID, ID, ...: the tasks that must be Complete before this one can start, each an id or project/id; while one is not, this task is Blocked')
