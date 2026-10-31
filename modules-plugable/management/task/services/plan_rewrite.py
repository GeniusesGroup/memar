#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_task_files = import_module('modules-plugable.management.task.services.task_files')
rewrite = _m_task_files.rewrite
key_of = _m_task_files.key_of
line_end = _m_task_files.line_end
