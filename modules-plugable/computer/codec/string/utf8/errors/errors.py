#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_edit = import_module('modules.knowledge.text.errors.edit')


class UTF8_Error_NotUtf8(_m_edit.Text_Error_Edit_NotUtf8):
    pass


class UTF8_Error_NamedTextNotUtf8(_m_edit.Text_Error_Edit_NamedTextNotUtf8):
    pass
