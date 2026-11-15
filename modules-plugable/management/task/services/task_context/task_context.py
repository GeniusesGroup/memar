#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
"""Thin re-export: act-context composition lives under content/normative_references.

Agency widgets and `memar agency_get_task_init_context` may keep this import path until
those aggregators are rehomed; the owner of the composition is
`modules.knowledge.content.services.act_context`.
"""
from __future__ import annotations
from modules.knowledge.content.services.act_context import *  # noqa: F403
from modules.knowledge.content.services import act_context as _act

__all__ = [name for name in dir(_act) if not name.startswith('_')]
